# Postgres

*Last updated: 2026-08-18*

> What the Postgres engine fixes — its types, its enum forms, and the column conventions a schema follows.
> Purpose — the applied SQL owns the schema, so engine facts belong to the engine, not to whatever maps over it.
> Use case — choosing a column type, adding an enum, or naming a table.

Before writing code that touches database tables — models, migrations, queries:

1. Read the repo's canonical schema — `{Repo}.Persistence/Migrations/NNN-name/Apply.sql` for Sql-strategy products,
   the owned `CREATE TABLE` truth. Folder layout, ordinals, apply/rollback pairing →
   [bespoke-migrations.md](../../migrations/sql/bespoke-migrations.md).
2. Read the data dictionary if one exists — field reference, allowed values, who sets each column.
3. Cross-check the DB ↔ C# mapping doc if one exists — column ↔ property mapping, known pitfalls.

- must never assume a column name or type — verify against the `Apply.sql` files first.
- applies to C# models, SQL migrations, Dapper queries, EF Core configurations, filter logic.

---

## Column constraints

- must declare every new column `NOT NULL` without `DEFAULT`, unless the default has a valid reason.

Valid reasons for `DEFAULT`:

- primary keys — `DEFAULT gen_random_uuid()`, but see *Primary keys* below.
- timestamps — `DEFAULT NOW()`, unless the value must come from code (precision, exact calculated time).
- trigger-created rows.

- must set everything else — booleans, enums, arrays, strings — explicitly from code.
  - a default masks a missing value and turns into a silent bug as pipelines evolve.

---

## Primary keys

- must use `Guid` for `Id` unless there is a valid reason — slug-based PK, composite PK.
- must not add `DEFAULT gen_random_uuid()` on an ID column — EF Core generates client-side via `Guid.NewGuid()`,
  so the DB default never fires.
- must implement the empty `IEntity` marker on every persisted type.
  - the `Guid Id` member comes from `IKeyedEntity<Guid>`.
- must use `IKeyedEntity<TId>` directly for a keyed / custom-id entity — see
  [entities.md](../../../../constructs/data/entity.md).
- both live in the SDK's `Data.Abstractions`.

---

## Type mappings (Postgres / Npgsql)

| C# | Postgres | Notes |
|---|---|---|
| `Guid` | `uuid` | EF Core generates client-side |
| `DateTime` / `DateTimeOffset` | `timestamptz` | Always `timestamptz`, never `timestamp` |
| `DateOnly` | `date` | Dapper handler in raw SQL — [data-access.md](../../../../constructs/behavior/repository.md) |
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

- must not use `NUMERIC` / `DECIMAL` anywhere — integer storage in the right unit covers every case.
- consequence: no `.HasPrecision()` needed in EF Core configs.

---

## Enum column mapping

> **Standard:** native PostgreSQL enum types.
> Text columns are the fallback for non-PG providers only — SqlServer / Sqlite, see *Text-column fallback*.

### Postgres (native enum types) — default

- **Storage** — PostgreSQL custom enum types (`CREATE TYPE listing_type AS ENUM (...)`).
- **C# ↔ PG case mapping** — PascalCase C# values map to snake_case PG labels.
  - `ApartmentRent` ↔ `'apartment_rent'`.
- **Registration** — **one bulk call**, never per-enum, never per-property `.HasConversion()`.
  - call `MapEnums(CaseStyle.Snake, namespaceFilter, assemblies)` (`NpgsqlEnumMappingExtensions`).
  - place it inside the `configure` delegate of `AddNpgsqlDataSource` (`PostgresServiceCollectionExtensions`).
- Npgsql requires enum mappings at the data-source (driver) level.
  - `MapEnums` runs on the builder before `Build()` and scans the given assemblies.
  - it registers every public non-nested enum that passes `namespaceFilter`.

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
- it routes both type and member names through one `CaseStyleNameTranslator(style)` (an `INpgsqlNameTranslator`).
- driver-level label mapping and any string-based mapping therefore agree *by construction* — they can't drift.
- no listing each enum twice (`MapEnum<T>` on both `NpgsqlDataSourceBuilder` and `UseNpgsql`).
- **Per-enum PG type override** — pass the optional `pgTypeName` delegate to `MapEnums` (`Func<Type, string?>`).
  - return `null` to keep the styled default.

---

### Text-column fallback (SqlServer / Sqlite)

- must store the enum as a **case-styled string** when the provider has no native enum types.
  - go through the SDK converters, which keep it reversible.
- must never hand-roll `nameof(...).ToSnakeCase()` + `Enum.Parse` — that pair is lossy on multi-word members.
  - the SDK builds its reverse map from the enum's own members.
- **EF Core** — `EnumPropertyBuilderExtensions.HasEnumStringConversion<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
builder.Property(e => e.Status).HasEnumStringConversion();        // snake_case text column
```

- applies `EnumCaseConverter<TEnum>`, a `ValueConverter<TEnum, string>`.
- reads are case-insensitive on the label; writes emit the configured style.
- **Dapper** — `DapperServiceCollectionExtensions.AddEnumTypeHandler<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
services.AddEnumTypeHandler<OrderStatus>();                       // registers EnumTypeHandler<OrderStatus>
```

- both paths round-trip through `EnumNameConverter<TEnum>` — `ToLabel` / `Parse` / `TryParse`.
  - it is the single source of truth for label ↔ member, cached per `(enum, style)`.

> **Forward note:** a future text-enum-default mode — text standard, native PG opt-in — lands with the SQLite track.
> Until then native PG enums are the standard, and text columns the non-PG fallback only.
