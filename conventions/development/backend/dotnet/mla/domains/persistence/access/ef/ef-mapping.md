# Ef mapping

*Last updated: 2026-08-18*

> How EF maps over a schema it does not own — the context, the configurations, and what never to configure.
> Purpose — schema-first means EF materializes rows; a mapping that drifts from the applied SQL is the bug.
> Use case — adding a `DbContext`, writing an `IEntityTypeConfiguration<T>`, or wiring an interceptor.

## EF's role

The schema is owned by SQL (`Migrations/NNN-name/Apply.sql`). EF Core maps C# types over that schema — it never creates, alters, or seeds it.

- Never call `Database.EnsureCreated()` (or `Migrate()` / EF migrations). The runner (`IMigrationRunnerService.ApplyPendingAsync`, see
  [bespoke-migrations.md](../../migrations/sql/bespoke-migrations.md)) owns DDL; EF only reads/writes rows.
- Strip all migration-only config from `IEntityTypeConfiguration<T>` — keep only config that changes *runtime* behavior (what EF queries, tracks,
  materializes). The waste-rule table below is the cut list.
- A wrong EF config here is silent: it can't fail a migration (there are none), it just produces wrong SQL or missed change-tracking.

---

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
  `DatabaseOptions.ConnectionString`, consumed by both EF Core and Dapper, and the place enums attach (`MapEnums` — see [enums](../../../../components/enums.md)).

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
  [code-organization.md](../../../../../lla/notation/style/style.md)'s file-per-type rule still says split by default; merge only when very tightly coupled.
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
> Sql-strategy default — [bespoke-migrations.md](../../migrations/sql/bespoke-migrations.md)).

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
mapping). Full details in [enums](../../../../components/enums.md).

---

### Audit & soft-delete

Cross-cutting timestamps/actors (`ICreationAuditable`, `IModificationAuditable`) and soft-delete (`ISoftDeletable`) are handled by SDK interceptors,
not per-config — entity contracts and what each marker stamps live in [entities.md](../../../../constructs/data/entity.md):

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

Organize in this order, separated by lightweight comment headers (see [code-organization.md](../../../../../lla/notation/style/style.md)):

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

Single `/// <summary>` one-liner starting with "Configures" — per [summary](../../../../../lla/notation/documentation/summary.md) starter table. No `<remarks>`.

```csharp
/// <summary>Configures the listings table mapping and relationships.</summary>
public sealed class ListingEntityConfiguration : IEntityTypeConfiguration<ListingEntity> { }
```

---
