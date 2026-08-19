# Application requests

*Last updated: 2026-08-18*

> The in-process message a caller dispatches — a `Query`, a `Command` or an `Event`.
> Purpose — a caller names the work it wants without naming who does it.
> Use case — every use case reachable from a controller, a handler, or a hosted service.

## Location

### Folder
- must sit in a `Queries/`, `Commands/` or `Events/` folder under the domain that owns the use case.

### File
- must give it its own file, named for the type →
  [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete message with **Represents**, and name the action it asks for.
- must start a marker interface with **Defines**.

#### [Type params](../../../lla/notation/documentation/typeparams.md)
- must carry a `<typeparam>` for the result a marker is generic over.

```csharp
// ✅ the marker defines, the message asks
/// <summary>Defines a query that returns <typeparamref name="TResult"/>.</summary>
/// <summary>Represents a query to get every channel.</summary>
// ❌ Represents claims a value the marker carries nothing of
/// <summary>Represents a query returning a result.</summary>
```

### Construct
- must declare a `sealed record` — a message is its inputs.
- must not reference an [api request](api-request.md) — the dependency points one way.
- must declare `{ get; init; }` — a message is built once and never written again.
- member shape (`required`, non-nullable) →
  [constructs](../../../lla/constructs/constructs.md) § *Data components*.

### Type name
- must suffix with `Query`, `Command` or `Event`.
- must read `{Domain}{Action}{Kind}`, domain-first and singular — `CodeGetByIdQuery`.

```csharp
// ✅
public sealed record CodeGetByIdQuery : IQuery<AppResult<CodeDto>>
// ❌ verb-first reads like an endpoint, and these are searched by domain
public sealed record GetCodeByIdQuery
```
