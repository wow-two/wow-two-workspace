# Json

*Last updated: 2026-08-18*

> One type's persisted JSON seam — the options it stores with, and the pair that reads and writes it.
> Purpose — a stored representation outlives the model, so its serializer settings belong beside it, not at the host.
> Use case — a column, a file or a cache entry holding one type as JSON;
> the API wire contract is the [api domain's](../domains/api/api-messages.md).

## Location

### Folder
- must sit beside the type it persists, in that type's own folder.

### File
- must give each seam its own file, named for the type it serializes.

---

## Declaration

### Type doc

#### [Summary](../../lla/notation/documentation/summary.md)
- must start with **Serializes**, and name the type it persists.
- must state the storage it is written for when more than one exists — a column, a cache entry, a file.

```csharp
// ✅ names the type and where the bytes land
/// <summary>Serializes code content for its jsonb column.</summary>
// ❌ names the format, which the suffix already carries
/// <summary>Serializes to JSON.</summary>
```

### Construct
- must declare a `static class` — the seam holds options and two methods, never state.
- must hold its `JsonSerializerOptions` as a single `static readonly` instance, built once.
- must not reuse the host's API options — the wire contract and the stored contract change on different schedules.

### Type name
- must suffix with `Json`, prefixed by the type it persists — `CodeContentJson`, `CodeRuleJson`.
- must name the format rather than the operation; the type is already in the prefix.
- must reach for [serialization](../platform/responses/serialization.md) instead when the contract is the HTTP wire.

```csharp
// ✅
public static class CodeContentJson
// ❌ names the operation, so a second method has nowhere to go
public static class CodeContentSerializer
```
