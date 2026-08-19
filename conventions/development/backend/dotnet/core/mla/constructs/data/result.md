# Results

*Last updated: 2026-08-18*

> The carrier an operation returns — a typed success or an `AppError`, never both.
> Purpose — a caller reads the outcome from the type, so nothing depends on an exception being thrown or not.
> Use case — any method whose failure a caller must handle; the contract itself is
> [platform](../../../../shapes/service/platform/responses/results.md).

## Location

### Folder
- must sit in a `Models/` folder under the domain that returns it.

### File
- must give it its own file, named for the type →
  [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Represents**, and name the operation's outcome.
- must not describe the success and failure arms separately — the union is the shape.

```csharp
// ✅ names the outcome
/// <summary>Represents the outcome of loading every channel.</summary>
// ❌ narrates the arms, which the type already carries
/// <summary>Represents either a list of channels or an error.</summary>
```

### Construct
- must declare a `sealed record` — a result is its values →
  [constructs](../../../lla/constructs/constructs.md) § *Data components*.
- must declare `{ get; init; }` — a result is built at the point it is returned.
- must not carry an HTTP status; `AppErrorType` is transport-agnostic and maps at the edge.
- must carry a [model](model.md), an entity, a value object or a primitive — never a [dto](dto.md).

```csharp
// ✅
public sealed record ChannelGetAllResult
// ❌ a status on the result binds the domain to a transport
public sealed record ChannelGetAllResult { public required int StatusCode { get; init; } }
```

### Type name
- must suffix with `Result`, prefixed by the operation — `ChannelGetAllResult`.
