# Repositories

*Last updated: 2026-08-18*

> The type that reads and persists rows — data in, data out, and nothing else.
> Purpose — one named seam per entity's storage, so a query has a home and a caller has one thing to inject.
> Use case — any read or write against the database; how it reaches the store is
> the [provider's](../../domains/persistence/persistence.md).

## Location

### Folder
- must sit in a `Repositories/` folder under the subdomain whose entity it stores.
- must split reads from writes by **folder** when a repository grows — `Queries/`, `Commands/`.

### File
- must give each repository, query or command class its own file, named for the type.

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Accesses**, whichever direction the class runs in.
- must name the rows it reaches, never the SQL it runs.
- must carry `<remarks>` only when a multi-method command class needs a directive.

```csharp
// ✅ names the rows
/// <summary>Accesses OLX external listings that have not been enriched yet.</summary>
// ❌ names the mechanism, which changes without the contract changing
/// <summary>Accesses listings using a Dapper query with a join.</summary>
```

### Construct
- must declare a `sealed class` with a primary constructor taking its connection or context.
- must use a block body `{ }` from the start — a query gains a filter, a projection, a log line
  ([style](../../../lla/notation/style/style.md) § *The body*).

### Type name
- must suffix with `Repository`, prefixed by the rows it reaches — `OlxListingsRepository`.
- must not suffix a class `Query` / `Command` — those name a [dispatched message](../data/application-request.md).
- must return a `Result` — a read can miss and a write can conflict.

```csharp
// ✅
public sealed class OlxListingsRepository(IDbConnectionFactory connectionFactory)
// ❌ `Query` names a mediator message, so the same word carries two roles
public sealed class UnenrichedListingsQuery
```
