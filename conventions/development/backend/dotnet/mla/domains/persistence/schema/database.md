# Database

*Last updated: 2026-08-15*

> Schema-first DB rules — column constraints, Postgres/Npgsql type mappings, and how EF Core maps over a SQL-owned schema (it never owns DDL).
> Purpose — one source of truth for the schema (the SQL) so EF config can't silently drift; integer-unit storage sidesteps `NUMERIC` precision bugs.
> Use case — reach for it before writing any model, migration, query, or EF configuration that touches a table.

## Schema-first rule

Before writing any code that touches database tables (models, migrations, queries):

1. Read the canonical schema for the repo — for Sql-strategy products that is `{Repo}.Persistence/Migrations/NNN-name/Apply.sql`, the owned
   `CREATE TABLE` truth (folder layout, ordinals, apply/rollback pairing live in [bespoke-migrations.md](../sql/bespoke-migrations.md)).
2. Read the data dictionary if one exists — field reference, allowed values, who sets each column.
3. Cross-check the DB ↔ C# mapping doc if one exists — column ↔ property mapping, known pitfalls.

- Never assume column names or types — verify against the `Apply.sql` files first.
- Applies to: C# models, SQL migrations, Dapper queries, EF Core configurations, filter logic.

---

## EF's role

The schema is owned by SQL (`Migrations/NNN-name/Apply.sql`). EF Core maps C# types over that schema — it never creates, alters, or seeds it.

- Never call `Database.EnsureCreated()` (or `Migrate()` / EF migrations). The runner (`IMigrationRunnerService.ApplyPendingAsync`, see
  [bespoke-migrations.md](../sql/bespoke-migrations.md)) owns DDL; EF only reads/writes rows.
- Strip all migration-only config from `IEntityTypeConfiguration<T>` — keep only config that changes *runtime* behavior (what EF queries, tracks,
  materializes). The waste-rule table below is the cut list.
- A wrong EF config here is silent: it can't fail a migration (there are none), it just produces wrong SQL or missed change-tracking.

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
  `IKeyedEntity<TId>` directly (see [entities.md](../../../constructs/data/entity.md)). Both live in the SDK's `Data.Abstractions`.

---

## Type mappings (Postgres / Npgsql)

| C# | Postgres | Notes |
|---|---|---|
| `Guid` | `uuid` | EF Core generates client-side |
| `DateTime` / `DateTimeOffset` | `timestamptz` | Always `timestamptz`, never `timestamp` |
| `DateOnly` | `date` | Needs a Dapper handler for raw queries — see [data-access.md](../../../constructs/behavior/repository.md) |
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

## DbContext

### Base class

Every product DbContext inherits `AppDbContextBase` (`Data.EntityFrameworkCore`), not raw `DbContext`. The base wires SDK conventions and increments
`IVersioned` tokens on save.

- Override `OnModelCreating(ModelBuilder)` and call `base.OnModelCreating(modelBuilder)` first — the base runs
  `ApplyConfigurationsFromAssembly(GetType().Assembly)` then `ApplyConventions()` (soft-delete query filter + `IVersioned` concurrency token, via
  `EntityModelConventions.ApplyConventions`). Your override adds nothing about columns or DDL — only runtime mapping (relationships, conversions,
  `Ignore`).
- Extra model conventions (value converters, default precision) go in `ConfigureConventionsCore(ModelConfigurationBuilder)` — the base seam invoked
  from `ConfigureConventions`. Do NOT override `ConfigureConventions` directly.

```csharp
/// <summary>The application database context.</summary>
public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : AppDbContextBase(options)
{
    public DbSet<ListingEntity> Listings => Set<ListingEntity>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder); // SDK conventions + assembly configs FIRST
        modelBuilder.ApplyNpgsqlConventions(); // xmin token for IHasXmin entities
    }
}
```

---

### Registration

- Register via `AddEntityFrameworkCore<TContext>` (`EntityFrameworkCoreServiceCollectionExtensions`) — never raw `AddDbContext` /
  `AddDbContextPool`. The helper applies pooling (default on) and auto-enables `EnableSensitiveDataLogging` / `EnableDetailedErrors` in Development;
  override via the
  `Action<EntityFrameworkCoreOptions>` overload (`UsePooling`, `PoolSize`, `NoTrackingByDefault`, …).
- Provider setup goes inside the `configureProvider` callback via `UseNpgsqlConventional` (or `UseSqlServerConventional`), which presets
  `EnableRetryOnFailure(maxRetryCount: 6)` + `CommandTimeout(30)`.
- Connection string comes from `DatabaseOptions.ConnectionString`, bound via `AddDatabaseOptions` (`Database` config section by default).
- A shared `NpgsqlDataSource` is registered once via `AddNpgsqlDataSource` (`PostgresServiceCollectionExtensions`) — built from
  `DatabaseOptions.ConnectionString`, consumed by both EF Core and Dapper, and the place enums attach (`MapEnums` — see [enums](../../../../lla/components/enums.md)).

```csharp
services.AddDatabaseOptions(configuration);
services.AddNpgsqlDataSource(b => b.MapEnums(assemblies: typeof(AppDbContext).Assembly));
services.AddEntityFrameworkCore<AppDbContext>((sp, builder) =>
    builder
        .UseNpgsqlConventional(sp.GetRequiredService<NpgsqlDataSource>())
        .UseSnakeCaseNamingConvention());
```

---

## EF Core entity type configurations

### Location

- `{Repo}.Persistence/Configurations/{Name}Configuration.cs` — one `IEntityTypeConfiguration<T>` per entity.
- Multiple configs may share a file when entities are tightly coupled (e.g. `ChannelEntityConfiguration` + `ChannelSourceEntityConfiguration`) — but
  [code-organization.md](../../../../lla/notation/style/style.md)'s file-per-type rule still says split by default; merge only when very tightly coupled.
- All configs are picked up by the base's `ApplyConfigurationsFromAssembly`.

---

### What to configure (runtime effect)

| Pattern | Why it's needed |
|---|---|
| `.ToTable()` | EF must know which table to query |
| `.HasKey()` | Change tracking, identity resolution, key comparisons |
| `.HasOne()` / `.HasMany()` | Navigation — `.Include()`, in-memory cascade |
| `.HasForeignKey()` | Tells EF which property is the FK |
| `.OnDelete()` | EF in-memory cascade behavior |
| `.HasConversion()` | Value conversion at read/write (rare — PG enums handled globally) |
| `.HasColumnType("jsonb")` | Npgsql needs this to serialize JSONB columns |
| `.HasJsonConversion<T>()` | JSON-mapped CLR property (see JSON columns below) |
| `.Ignore()` | Excludes computed / non-persisted properties |

---

### What NOT to configure (migration-only = dead code in schema-first repos)

The schema lives in `Apply.sql`. Anything that only emits or constrains DDL is dead weight — it can't fail (no migrations run), it just rots.

| Pattern | Why it's waste |
|---|---|
| `.IsRequired()` | NRT already tells EF nullability: `string` = required, `string?` = optional |
| `.HasMaxLength()` | EF doesn't validate string length at runtime; the DB enforces |
| `.HasColumnName()` | Redundant when `UseSnakeCaseNamingConvention()` is on (see below) |
| `.HasIndex()` | Migration-only; the index lives in `Apply.sql` |
| `.HasFilter()` | Partial-index predicate — migration-only |
| `.HasDatabaseName()` | Custom index name — migration-only |
| `.HasPrecision()` | Not needed when numeric columns use integer types |

> Note: if you're NOT schema-first and EF generates migrations, all of these are valid. The waste rule applies only when the schema is SQL-owned (the
> Sql-strategy default — [bespoke-migrations.md](../sql/bespoke-migrations.md)).

---

### snake_case naming

Turn on `UseSnakeCaseNamingConvention()` on the `DbContextOptionsBuilder` (SDK naming-conventions package — see `NamingConventionsExtensions`;
`UseLowerCaseNamingConvention` / `UseCamelCaseNamingConvention` / `UseUpperSnakeCaseNamingConvention` also available). This maps every CLR member to
its snake_case column globally — do NOT restate it per property with `.HasColumnName()` (reinforces the waste rule above).

---

### JSON columns

- Map a complex CLR property to a JSON column with `.HasJsonConversion<T>()` (`JsonPropertyBuilderExtensions`). It wires both the
  `JsonValueConverter<T>` (serialize on write / deserialize on read) and the required `JsonValueComparer<T>`.
- The comparer is mandatory: EF's snapshot/change-tracking misses mutations on JSON reference types without it.
- Pair with the provider column type: `.HasColumnType("jsonb")` on Postgres (`nvarchar(max)` on SqlServer).

```csharp
builder
    .Property(e => e.Metadata)
    .HasColumnType("jsonb")
    .HasJsonConversion();
```

---

### Enum mapping (Postgres)

Do NOT use `.HasConversion()` per property — enums are registered globally at the Npgsql data-source level via `MapEnums` (driver-level C#↔PG enum
mapping). Full details in [enums](../../../../lla/components/enums.md).

---

### Audit & soft-delete

Cross-cutting timestamps/actors (`ICreationAuditable`, `IModificationAuditable`) and soft-delete (`ISoftDeletable`) are handled by SDK interceptors,
not per-config — entity contracts and what each marker stamps live in [entities.md](../../../constructs/data/entity.md):

- `AuditInterceptor` — register via `AddEfCoreAuditInterceptor()` (use the `<TAccessor>` overload to populate `CreatedBy` / `UpdatedBy` on the
  `…AuditableBy<TUserId>` variants), wire with `UseAuditInterceptor(sp)`.
- `SoftDeleteInterceptor` — register via `AddEfCoreSoftDeleteFilter()`, wire with `UseSoftDeleteInterceptor(sp)`; the `IsDeleted` query filter is
  applied automatically by `ApplyConventions` in `AppDbContextBase`.

---

### Concurrency tokens

Optimistic-concurrency markers map via provider conventions called from `OnModelCreating` (after `base`):

| Marker | Provider | Token | Applied by |
|---|---|---|---|
| `IVersioned` | any | `uint Version` (bumped in `SaveChanges`) | `EntityModelConventions.ApplyConventions` (auto via base) |
| `IHasXmin` | Postgres | system `xmin` column (`xid`) | `ApplyNpgsqlConventions()` |
| `IRowVersioned` | SqlServer | `byte[] RowVersion` (`rowversion`) | `ApplySqlServerConventions()` |

- `IVersioned` is provider-agnostic and needs no extra call.
- For native tokens, call `ApplyNpgsqlConventions()` / `ApplySqlServerConventions()` once in `OnModelCreating`.

---

### Section order inside a configuration

Organize in this order, separated by lightweight comment headers (see [code-organization.md](../../../../lla/notation/style/style.md)):

1. Table + Key — `.ToTable()`, `.HasKey()`.
2. Column type overrides — `.HasColumnType("jsonb")` etc.
3. Conversions — `.HasConversion()` / `.HasJsonConversion<T>()` for the rare cases.
4. Relationships — `.HasOne()`, `.HasMany()`, `.HasForeignKey()`, `.OnDelete()`.

---

### Chaining

Always chain on new lines, even for a single method call:

```csharp
builder
    .ToTable(ListingEntity.TableName);

builder
    .HasKey(e => e.Id);

// ── Relationships ──

builder
    .HasOne(e => e.OlxRawListing)
    .WithOne(e => e.Listing)
    .HasForeignKey<ListingEntity>(e => e.OlxRawListingId);

builder
    .HasMany(e => e.Images)
    .WithOne(e => e.Listing)
    .HasForeignKey(e => e.ListingId)
    .OnDelete(DeleteBehavior.Cascade);
```

---

### Documentation

Single `/// <summary>` one-liner starting with "Configures" — per [summary](../../../../lla/notation/documentation/summary.md) starter table. No `<remarks>`.

```csharp
/// <summary>Configures the listings table mapping and relationships.</summary>
public sealed class ListingEntityConfiguration : IEntityTypeConfiguration<ListingEntity> { }
```

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
