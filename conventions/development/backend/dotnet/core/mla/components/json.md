# Json

*Last updated: 2026-08-18*

> One type's persisted JSON seam — the options it stores with, and the pair that reads and writes it.
> Purpose — a stored representation outlives the model, so its serializer settings belong beside it, not at the host.
> Use case — a column, a file or a cache entry holding one type as JSON;
> the API wire contract is the [api domain's](../domains/api/api-messages.md).

> Defined at [json — the construct](../constructs/behavior/json.md); this doc carries every condition for using one.

## Location

Where it sits is part of what it is → [json](../constructs/behavior/json.md) § *Location*.

---

## Declaration

What it is, how it is declared and what it is called → [json](../constructs/behavior/json.md) § *Declaration*.

### Type doc

#### [Summary](../../lla/notation/documentation/summary.md)
- must state the storage it is written for when more than one exists — a column, a cache entry, a file.

```csharp
// ✅ names the type and where the bytes land
/// <summary>Serializes code content for its jsonb column.</summary>
// ❌ names the format, which the suffix already carries
/// <summary>Serializes to JSON.</summary>
```

---

## Content

### Members
- must expose exactly three members — `Options`, `Serialize`, `Deserialize`. A fourth means the seam is
  carrying logic that belongs to a [mapper](../constructs/behavior/mapper.md).
- must declare `Options` as `public static readonly`, built once at type load.
- must accept a nullable string on `Deserialize` and return `null` for a null or blank column — a missing
  document is absence, not a parse failure.
- must not expose the raw `JsonSerializer` call to callers; the seam is the only door to those bytes.
