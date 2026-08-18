# Postgres

*Last updated: 2026-08-18*

> What the Postgres engine fixes — its types, its enum forms, and the column conventions a schema follows.
> Purpose — the applied SQL owns the schema, so engine facts belong to the engine, not to whatever maps over it.
> Use case — choosing a column type, adding an enum, or naming a table.

Before writing any code that touches database tables (models, migrations, queries):

1. Read the canonical schema for the repo — for Sql-strategy products that is `{Repo}.Persistence/Migrations/NNN-name/Apply.sql`, the owned
   `CREATE TABLE` truth (folder layout, ordinals, apply/rollback pairing live in [bespoke-migrations.md](../../migrations/sql/bespoke-migrations.md)).
2. Read the data dictionary if one exists — field reference, allowed values, who sets each column.
3. Cross-check the DB ↔ C# mapping doc if one exists — column ↔ property mapping, known pitfalls.

- Never assume column names or types — verify against the `Apply.sql` files first.
- Applies to: C# models, SQL migrations, Dapper queries, EF Core configurations, filter logic.

---

## Column constraints

`NOT NULL` without `DEFAULT` for all new columns unless there's a valid reason for a default.

Valid reasons for `DEFAULT`:

- Primary keys (`DEFAULT gen_random_uuid()` — but see PK note below).
- Timestamps (`DEFAULT NOW()`) — unless the value must come from code (precision, exact calculated time).
- Trigger-created rows.

Everything else — booleans, enums, arrays, strings — must be set explicitly from code. Defaults mask missing values and introduce silent bugs when
pipelines evolve.

---

## Primary keys

- `Guid` for `Id` unless there's a valid reason (slug-based PK, composite PK).
- EF Core generates client-side via `Guid.NewGuid()` — do NOT add `DEFAULT gen_random_uuid()` on ID columns; the DB default never fires (EF always
  provides the value).
- Every persisted type implements the `IEntity` marker (empty); the `Guid Id` member comes from `IKeyedEntity<Guid>`. Keyed/custom-id entities use
  `IKeyedEntity<TId>` directly (see [entities.md](../../../../constructs/data/entity.md)). Both live in the SDK's `Data.Abstractions`.

---

## Type mappings (Postgres / Npgsql)

| C# | Postgres | Notes |
|---|---|---|
| `Guid` | `uuid` | EF Core generates client-side |
| `DateTime` / `DateTimeOffset` | `timestamptz` | Always `timestamptz`, never `timestamp` |
| `DateOnly` | `date` | Needs a Dapper handler for raw queries — see [data-access.md](../../../../constructs/behavior/repository.md) |
| `string` | `text` / `varchar(n)` | Prefer `text`; `varchar(n)` only when a hard limit is meaningful |
| `bool` | `boolean` | |
| `List<TEnum>` | `tenant_type[]` | Use the PG enum array type, not `TEXT[]` |
| `List<string>` | `TEXT[]` | Free-form: AI output, URLs, tags, unstructured text |
| `byte[]` | `bytea` | |
| `List<T>` | array type | EF Core handles native Npgsql array mapping for single-table columns |

---

## Numeric type conventions

Avoid `NUMERIC` / `DECIMAL` — store values as integers in the smallest meaningful unit.

| Data kind | DB type | C# | Unit | Example |
|---|---|---|---|---|
| Percentages / confidence | `SMALLINT` + `CHECK (0..100)` | `short` | 0–100 whole percent | `85` = 85% |
| Money (large amounts) | `BIGINT` | `long` | Whole amount, original currency | `3840000000` = 3.84B UZS |
| Money (micro / API costs) | `INTEGER` | `int` | Micro-USD (×1,000,000) | `123` = $0.000123 |
| Area | `INTEGER` | `int` | Square centimeters (cm²) | `750000` = 75.00 m² |
| Height / length | `SMALLINT` | `short` | Centimeters | `280` = 2.80 m |
| Counts / ordinals | `SMALLINT` | `short` | Natural unit | `3` = 3 rooms |

- No `NUMERIC` / `DECIMAL` anywhere — integer storage in the right unit covers every case.
- Consequence: no `.HasPrecision()` needed in EF Core configs.

---

## Enum column mapping

> **Standard:** native PostgreSQL enum types. Text columns are the fallback for non-PG providers (SqlServer / Sqlite) only — see *Text-column
> fallback*.

### Postgres (native enum types) — default

- **Storage** — PostgreSQL custom enum types (`CREATE TYPE listing_type AS ENUM (...)`).
- **C# ↔ PG case mapping** — PascalCase C# values map to snake_case PG labels (`ApartmentRent` ↔ `'apartment_rent'`).
- **Registration** — **one bulk call**, not per-enum, not per-property `.HasConversion()`. Call `MapEnums(CaseStyle.Snake, namespaceFilter,
  assemblies)` (`NpgsqlEnumMappingExtensions`) inside the `configure` delegate of `AddNpgsqlDataSource` (`PostgresServiceCollectionExtensions`).
- Npgsql requires enum mappings at the data-source (driver) level — `MapEnums` runs on the builder before `Build()`, scans the given assemblies, and
  registers every public non-nested enum that passes `namespaceFilter`.

```csharp
// Registration — once at startup
services.AddNpgsqlDataSource(builder =>
    builder.MapEnums(
        CaseStyle.Snake,
        ns => ns.StartsWith("Drydock.Domain"),
        typeof(ChannelType).Assembly));
```

**Why bulk, why a translator:**

- `MapEnums` derives the PG type name from the enum type name via `CaseConverter.ToCase(name, style)`.
- It routes both type and member names through a single `CaseStyleNameTranslator(style)` (an `INpgsqlNameTranslator`).
- Driver-level label mapping and any string-based mapping therefore agree *by construction* — they can't drift.
- No more listing each enum twice (`MapEnum<T>` on both `NpgsqlDataSourceBuilder` and `UseNpgsql`).
- **Per-enum PG type override** — pass the optional `pgTypeName` delegate to `MapEnums` (`Func<Type, string?>`; return `null` to keep the styled
  default).

---

### Text-column fallback (SqlServer / Sqlite)

- When the provider has no native enum types, store the enum as a **case-styled string** — reversibly, via the SDK converters.
- Never hand-roll `nameof(...).ToSnakeCase()` + `Enum.Parse`: that underscore-stripping pair is lossy on multi-word members. The SDK builds its
  reverse map from the enum's own members.
- **EF Core** — `EnumPropertyBuilderExtensions.HasEnumStringConversion<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
builder.Property(e => e.Status).HasEnumStringConversion();        // snake_case text column
```

- Applies `EnumCaseConverter<TEnum>` (a `ValueConverter<TEnum, string>`); reads are case-insensitive on the label, writes emit the configured style.
- **Dapper** — `DapperServiceCollectionExtensions.AddEnumTypeHandler<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
services.AddEnumTypeHandler<OrderStatus>();                       // registers EnumTypeHandler<OrderStatus>
```

- Both paths round-trip through `EnumNameConverter<TEnum>` (`ToLabel` / `Parse` / `TryParse`) — the single source of truth for label ↔ member,
  cached per `(enum, style)`.

> **Forward note:** a future text-enum-default mode (text as the standard, native PG opt-in) lands with the SQLite track. Until then, native PG
> enums are the standard and text columns are the non-PG fallback only.

