# Ef mapping

*Last updated: 2026-08-18*

> How EF maps over a schema it does not own — the context, the configurations, and what never to configure.
> Purpose — schema-first means EF materializes rows; a mapping that drifts from the applied SQL is the bug.
> Use case — adding a `DbContext`, writing an `IEntityTypeConfiguration<T>`, or wiring an interceptor.

## EF's role

SQL owns the schema (`Migrations/NNN-name/Apply.sql`).
EF Core maps C# types over it, and never creates, alters or seeds it.

- must never call `Database.EnsureCreated()`, `Migrate()`, or EF migrations.
  - the runner owns DDL — `IMigrationRunnerService.ApplyPendingAsync`, see
    [bespoke-migrations.md](../../migrations/sql/bespoke-migrations.md). EF only reads/writes rows.
- must strip all migration-only config from `IEntityTypeConfiguration<T>`.
  - keep only config that changes *runtime* behavior — what EF queries, tracks, materializes.
  - the waste-rule table below is the cut list.
- a wrong EF config here is silent — it can't fail a migration, there are none.
  - it produces wrong SQL or missed change-tracking instead.

---

## DbContext

### Base class

- must inherit `AppDbContextBase` (`Data.EntityFrameworkCore`) on every product DbContext, never raw `DbContext`.
  - the base wires SDK conventions and increments `IVersioned` tokens on save.
- must override `OnModelCreating(ModelBuilder)` and call `base.OnModelCreating(modelBuilder)` first.
  - the base runs `ApplyConfigurationsFromAssembly(GetType().Assembly)` then `ApplyConventions()`.
  - `ApplyConventions()` adds the soft-delete query filter + `IVersioned` concurrency token,
    via `EntityModelConventions.ApplyConventions`.
  - the override adds nothing about columns or DDL — only runtime mapping (relationships, conversions, `Ignore`).
- must put extra model conventions in `ConfigureConventionsCore(ModelConfigurationBuilder)`.
  - value converters, default precision.
  - it is the base seam invoked from `ConfigureConventions`.
  - must NOT override `ConfigureConventions` directly.

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

- must register via `AddEntityFrameworkCore<TContext>` (`EntityFrameworkCoreServiceCollectionExtensions`).
  - never raw `AddDbContext` / `AddDbContextPool`.
  - the helper applies pooling, default on.
  - it auto-enables `EnableSensitiveDataLogging` / `EnableDetailedErrors` in Development.
  - override via the `Action<EntityFrameworkCoreOptions>` overload.
    - `UsePooling`, `PoolSize`, `NoTrackingByDefault`, ….
- must put provider setup inside the `configureProvider` callback.
  - via `UseNpgsqlConventional` or `UseSqlServerConventional`.
  - both preset `EnableRetryOnFailure(maxRetryCount: 6)` + `CommandTimeout(30)`.
- must take the connection string from `DatabaseOptions.ConnectionString`, bound via `AddDatabaseOptions`.
  - the `Database` config section by default.
- must register one shared `NpgsqlDataSource` via `AddNpgsqlDataSource` (`PostgresServiceCollectionExtensions`).
  - built from `DatabaseOptions.ConnectionString`, consumed by both EF Core and Dapper.
  - enums attach there — `MapEnums`, see [postgres](../../database/postgres/postgres.md) § *Enum column mapping*.

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
- may share one file across configs when the entities are tightly coupled.
  - e.g. `ChannelEntityConfiguration` + `ChannelSourceEntityConfiguration`.
  - the file-per-type rule still says split by default —
    [code-organization.md](../../../../../lla/notation/style/style.md).
  - merge only when very tightly coupled.
- the base's `ApplyConfigurationsFromAssembly` picks up all configs.

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

The schema lives in `Apply.sql`. Anything that only emits or constrains DDL is dead weight —
it can't fail, no migrations run, and it rots.

| Pattern | Why it's waste |
|---|---|
| `.IsRequired()` | NRT already tells EF nullability: `string` = required, `string?` = optional |
| `.HasMaxLength()` | EF doesn't validate string length at runtime; the DB enforces |
| `.HasColumnName()` | Redundant when `UseSnakeCaseNamingConvention()` is on (see below) |
| `.HasIndex()` | Migration-only; the index lives in `Apply.sql` |
| `.HasFilter()` | Partial-index predicate — migration-only |
| `.HasDatabaseName()` | Custom index name — migration-only |
| `.HasPrecision()` | Not needed when numeric columns use integer types |

> All of these are valid when you are NOT schema-first and EF generates migrations.
> The waste rule applies only when the schema is SQL-owned — the Sql-strategy default,
> [bespoke-migrations.md](../../migrations/sql/bespoke-migrations.md).

---

### snake_case naming

- must turn on `UseSnakeCaseNamingConvention()` on the `DbContextOptionsBuilder`.
  - SDK naming-conventions package, see `NamingConventionsExtensions`.
  - `UseLowerCaseNamingConvention` / `UseCamelCaseNamingConvention` /
    `UseUpperSnakeCaseNamingConvention` also available.
  - it maps every CLR member to its snake_case column globally.
- must NOT restate it per property with `.HasColumnName()` — reinforces the waste rule above.

---

### JSON columns

- must map a complex CLR property to a JSON column with `.HasJsonConversion<T>()` (`JsonPropertyBuilderExtensions`).
  - it wires `JsonValueConverter<T>` — serialize on write, deserialize on read.
  - it also wires the required `JsonValueComparer<T>`.
- the comparer is mandatory — without it EF's snapshot/change-tracking misses mutations on JSON reference types.
- must pair with the provider column type — `.HasColumnType("jsonb")` on Postgres, `nvarchar(max)` on SqlServer.

```csharp
builder
    .Property(e => e.Metadata)
    .HasColumnType("jsonb")
    .HasJsonConversion();
```

---

### Enum mapping (Postgres)

- must NOT use `.HasConversion()` per property.
- must register enums globally at the Npgsql data-source level via `MapEnums` — driver-level C#↔PG enum mapping.
- full details in [postgres](../../database/postgres/postgres.md) § *Enum column mapping*.

---

### Audit & soft-delete

SDK interceptors handle cross-cutting timestamps/actors (`ICreationAuditable`, `IModificationAuditable`) and soft-delete
(`ISoftDeletable`), never per-config. Entity contracts and what each marker stamps live in
[entities.md](../../../../constructs/data/entity.md):

- `AuditInterceptor` — register via `AddEfCoreAuditInterceptor()`, wire with `UseAuditInterceptor(sp)`.
  - use the `<TAccessor>` overload to populate `CreatedBy` / `UpdatedBy` on the `…AuditableBy<TUserId>` variants.
- `SoftDeleteInterceptor` — register via `AddEfCoreSoftDeleteFilter()`, wire with `UseSoftDeleteInterceptor(sp)`.
  - `ApplyConventions` in `AppDbContextBase` applies the `IsDeleted` query filter automatically.

---

### Concurrency tokens

Optimistic-concurrency markers map via provider conventions called from `OnModelCreating` (after `base`):

| Marker | Provider | Token | Applied by |
|---|---|---|---|
| `IVersioned` | any | `uint Version` (bumped in `SaveChanges`) | `EntityModelConventions.ApplyConventions` (via base) |
| `IHasXmin` | Postgres | system `xmin` column (`xid`) | `ApplyNpgsqlConventions()` |
| `IRowVersioned` | SqlServer | `byte[] RowVersion` (`rowversion`) | `ApplySqlServerConventions()` |

- `IVersioned` is provider-agnostic and needs no extra call.
- must call `ApplyNpgsqlConventions()` / `ApplySqlServerConventions()` once in `OnModelCreating` for a native token.

---

### Section order inside a configuration

- must organize in this order, separated by lightweight comment headers
  ([code-organization.md](../../../../../lla/notation/style/style.md)):

1. Table + Key — `.ToTable()`, `.HasKey()`.
2. Column type overrides — `.HasColumnType("jsonb")` etc.
3. Conversions — `.HasConversion()` / `.HasJsonConversion<T>()` for the rare cases.
4. Relationships — `.HasOne()`, `.HasMany()`, `.HasForeignKey()`, `.OnDelete()`.

---

### Chaining

- must chain on new lines, even for a single method call:

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

- must carry a single `/// <summary>` one-liner starting with "Configures" — per the
  [summary](../../../../../lla/notation/documentation/summary.md) starter table.
- must not add `<remarks>`.

```csharp
/// <summary>Configures the listings table mapping and relationships.</summary>
public sealed class ListingEntityConfiguration : IEntityTypeConfiguration<ListingEntity> { }
```

---
