# Dapper

*Last updated: 2026-08-18*

> Reaching the database through a connection and hand-written SQL.
> Purpose — a query the author wrote is a query the author can read; no expression tree stands between the two.
> Use case — any read or write that is not going through the EF change tracker.

## Table names

An entity read through hand-written SQL declares its own table name.

- must implement `IHasTableName` — a `static abstract string TableName { get; }`.
- must give the name in storage casing — snake_case for Postgres.
- must treat that member as the single source of truth for SQL and table-name resolution.

```csharp
// ✅
public sealed record OrderLineItemEntity : IKeyedEntity<Guid>, IHasTableName
{
    public static string TableName => "order_line_items";
}
```

---

## Connections

> **Inject `IDbConnectionFactory` — never a raw `DbConnection` or connection string.**
> It is the repo's single connection-factory abstraction, and isolates the connection-string lookup to one place
> (`IDbConnectionFactory`, `src/Data/Abstractions/IDbConnectionFactory.cs`).

- **Open one fresh connection per operation**, at the start of each method.
  - `await using var conn = await connectionFactory.CreateOpenAsync(ct);`
- the factory hands back an already-opened `DbConnection`.
  - `ValueTask<DbConnection> CreateOpenAsync(CancellationToken)`.
- must never cache, reuse, or share one across operations.
- `Create()` returns a *closed* connection, caller opens + disposes; prefer `CreateOpenAsync(ct)` in app code.

### Registration

Register the factory **once** at startup (`ConnectionFactoryServiceCollectionExtensions`, `src/Data/Abstractions/`).
Pick one:

- `AddDataSourceConnectionFactory()` — **default**; backed by a registered `DbDataSource`, e.g. `NpgsqlDataSource`.
  - resolves to `DataSourceConnectionFactory` (singleton).
  - pooling, enum mapping etc. are configured on the data source.
- `AddDbConnectionFactory<TFactory>()` — backed by a custom `IDbConnectionFactory` you supply (singleton).
  - use for a provider without a `DbDataSource`, or bespoke connection construction.

```csharp
services.AddNpgsqlDataSource(connectionString); // registers a DbDataSource
services.AddDataSourceConnectionFactory();       // → IDbConnectionFactory
services.AddDapperConventions();                 // global mappings + handlers (idempotent)
```

---

## Conventions (global, once)

`AddDapperConventions()` (`DapperServiceCollectionExtensions`, `src/Data/Dapper/`) is **idempotent**, guarded by
`Interlocked.Exchange`, and wires the process-wide Dapper conventions:

- snake_case column → PascalCase property mapping (`DefaultTypeMap.MatchNamesWithUnderscores = true`)
- `DateOnlyTypeHandler` — `DATE` ↔ `DateOnly`
- `ListTypeHandler<string>` — `TEXT[]` ↔ `List<string>`

Call it once at startup, or rely on the `AddDapperRepository<…>` / `AddDataSourceConnectionFactory` paths that call it
for you. Register additional list handlers at startup via `SqlMapper.AddTypeHandler`:

```csharp
SqlMapper.AddTypeHandler(new ListTypeHandler<int>());
SqlMapper.AddTypeHandler(new ListTypeHandler<Guid>());
```

> Enum-as-text columns: use `AddEnumTypeHandler<TEnum>(CaseStyle.Snake)`, which registers `EnumTypeHandler<TEnum>` —
> see [Enum-as-text columns](#enum-as-text-columns) and [postgres](../../database/postgres/postgres.md) § *Enum column mapping*.

---

## Generic CRUD — `DapperRepository<TEntity, TId>`

- must depend on `IRepository<TEntity, TId>` (read+write) or `IReadRepository<TEntity, TId>` (read-only).
  - for straightforward single-table read/CRUD.
- must let `DapperRepository<TEntity, TId>` generate the SQL.
  - never hand-roll `SELECT *` / `INSERT` / `UPDATE` / `DELETE`.

### Entity requirements

- `TEntity` must declare **both** `IKeyedEntity<TId>` (exposes `Id`) **and** `IHasTableName`.
  - `IHasTableName` supplies the static abstract `TableName`.
- `TId` must be `notnull, IEquatable<TId>`.

```csharp
public sealed record OlxListingEntity : IKeyedEntity<Guid>, IHasTableName
{
    public static string TableName => "olx_listings";   // storage casing (snake_case)
    public Guid Id { get; init; }
    public string Title { get; set; } = "";
    public DateTimeOffset? EnrichedAt { get; set; }
}
```

- column set = **every public instance property with a getter *and* setter**, mapped via `SqlNaming.ColumnCase`.
- the Id column is `nameof(IKeyedEntity<TId>.Id)`.

### Store-generated columns

- must override the protected `ExcludedOnInsert` / `ExcludedOnUpdate`.
  - omits identity / computed / store-generated columns.
- defaults: `ExcludedOnInsert` = none; `ExcludedOnUpdate` = `Id`.

```csharp
public sealed class OlxListingsRepository(IDbConnectionFactory connectionFactory)
    : DapperRepository<OlxListingEntity, Guid>(connectionFactory)
{
    // DB fills these via DEFAULT / trigger — never in the INSERT/UPDATE column list
    protected override IReadOnlyCollection<string> ExcludedOnInsert =>
        [nameof(OlxListingEntity.CreatedAt)];

    protected override IReadOnlyCollection<string> ExcludedOnUpdate =>
        [nameof(OlxListingEntity.Id), nameof(OlxListingEntity.CreatedAt)];
}
```

- all members are `virtual` — override `GetByIdAsync`, `CreateAsync`, etc. for bespoke SQL while inheriting the rest.

### Registration

`AddDapperRepository` (`DapperRepositoryServiceCollectionExtensions`, `src/Data/Dapper/Repositories/`) registers the
implementation under **both** `IRepository<,>` and `IReadRepository<,>`, and calls `AddDapperConventions()` for you
(Scoped by default):

```csharp
// generic repo
services.AddDapperRepository<OlxListingEntity, Guid>();

// concrete subclass (custom queries / excluded cols)
services.AddDapperRepository<OlxListingsRepository, OlxListingEntity, Guid>();
```

---

## SQL conventions

For hand-written queries and commands.

- **Table references** — `SqlNaming.Table<TEntity>()`, or `SqlNaming.Table<TEntity>("o")` for an aliased reference.
  - requires `TEntity : IHasTableName`.
  - define a class-level constant: `private static readonly string Table = SqlNaming.Table<OlxListingEntity>();`.
- **Column names** — `SqlNaming.Col("EnrichedAt")` → `enriched_at`, default `CaseStyle.Snake`.
  - aliased: `SqlNaming.Col("EnrichedAt", "l")` → `l.enriched_at`.
  - strongly-typed: `SqlNaming.Col<OlxListingEntity>(x => x.EnrichedAt)`.
  - hard-coded snake_case is fine for simple single-table queries.
  - use `SqlNaming.Col` for dynamic WHERE clauses or aliased joins.
- **Parameters** — `SqlNaming.ParRef("Limit")` → `@limit`, a placeholder, default `CaseStyle.Camel`.
  - `SqlNaming.Par("Limit")` → bare `limit`, for `DynamicParameters.Add`.
  - strongly-typed: `SqlNaming.ParRef<OlxListingEntity>(x => x.Id)`.
  - pass values via an anonymous object or `DynamicParameters`.
- **Casing is global** — defaults columns `Snake`, params `Camel`.
  - override **once at startup** via `SqlNaming.ColumnCase` / `SqlNaming.ParameterCase` if a schema differs.
  - never per-call.
- **Raw strings** — follow the raw-string rules in
  [code-organization.md](../../../../../lla/notation/style/style.md); opening `"""` on its own line.
- **Wrap every call** in `new CommandDefinition(sql, parameters, cancellationToken: ct)`.
  - never `QueryAsync(sql, parameters)` without it — it loses the CT.

```csharp
public sealed class UnenrichedListingsRepository(IDbConnectionFactory connectionFactory)
{
    private static readonly string Table = SqlNaming.Table<OlxListingEntity>();

    public async Task<int> GetCountAsync(CancellationToken ct = default)
    {
        await using var conn = await connectionFactory.CreateOpenAsync(ct);

        var sql =
            $"""
             SELECT COUNT(*)::INTEGER
             FROM {Table}
             WHERE enriched_at IS NULL
             """;

        return await conn.ExecuteScalarAsync<int>(
            new CommandDefinition(sql, cancellationToken: ct));
    }
}
```

> **Stale-helper fix:** `Tab<T>()` / `Col()` do not exist. The helpers are static members on `SqlNaming` —
> `SqlNaming.Table<T>` / `SqlNaming.Col` / `SqlNaming.Col<T>` / `SqlNaming.Par` / `SqlNaming.ParRef`.
> `Table<T>` requires `IHasTableName`.

### DI registration (query/command classes)

- must use a Scoped lifetime — it shares request-scoped connection state.
- must register it in the persistence registration extension.

---

## Reusable SQL fragments

For queries with shared WHERE logic across count + batch methods, extract into a `static readonly string`:

```csharp
private static readonly string WhereClause =
    $"""
     FROM {Table} rl
     WHERE rl.enriched_at IS NOT NULL
       AND NOT EXISTS (...)
     """;

public Task<int> GetCountAsync(CancellationToken ct) =>
    conn.ExecuteScalarAsync<int>($"SELECT COUNT(*)::INTEGER {WhereClause}");

public Task<List<T>> GetBatchAsync(CancellationToken ct) =>
    conn.QueryAsync<T>($"""
     SELECT rl.id, rl.title, ...
     {WhereClause}
     ORDER BY rl.scraped_at ASC
     LIMIT @limit
     """);
```

> `const string` cannot use string interpolation — use `static readonly string` when a fragment references the
> `SqlNaming.Table<T>()` / `SqlNaming.Col(...)` helpers.

---

## Type handlers

`AddDapperConventions()` registers the default handlers (see [Conventions](#conventions-global-once)):

- `DateOnlyTypeHandler` — `DATE` ↔ `DateOnly`
- `ListTypeHandler<string>` — `TEXT[]` ↔ `List<string>`
- snake_case → PascalCase property mapping

Additional list handlers (`List<int>`, `List<Guid>`) → register at startup via
`SqlMapper.AddTypeHandler(new ListTypeHandler<int>())`.

### Enum-as-text columns

When a column stores an enum as text (the portable default), register a string-backed handler once at startup:

```csharp
services.AddEnumTypeHandler<OrderStatus>();              // default CaseStyle.Snake → "in_progress"
services.AddEnumTypeHandler<OrderStatus>(CaseStyle.Camel);
```

- `AddEnumTypeHandler<TEnum>` (constraint `TEnum : struct, Enum`) registers `EnumTypeHandler<TEnum>`.
  - writes emit the chosen `CaseStyle`; reads are case-insensitive.
- must use Npgsql's driver-level `MapEnum` instead for Postgres **native** enum types.
  - see [postgres](../../database/postgres/postgres.md) § *Enum column mapping*.

---

## No query abstraction

- must not use `IQueryable`, the Specification pattern, or an expression-tree query builder.
- reads are generic-CRUD methods on `IReadRepository<,>` — `GetByIdAsync`, `GetAllAsync`, `ExistsAsync`, `CountAsync`.
- reads are otherwise hand-written SQL in a repository, split into `Queries/` and `Commands/` folders once it grows.
- must compose filtering in SQL, never in C# query objects.

---
