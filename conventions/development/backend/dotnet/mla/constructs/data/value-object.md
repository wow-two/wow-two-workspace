# Value objects

*Last updated: 2026-08-18*

> A type whose identity is its values, stored inside an entity's row instead of owning one.
> Purpose — the suffix is what separates a type that owns a row from one that rides inside one.
> Use case — a content block, a routing rule, an amount; anything an entity persists whole.

## Location

### Folder
- must sit in the `Models/` folder of the entity that stores it.

### File
- must give each value object its own file, named for the type.

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Represents**.
- must name what the values mean together, never how they are stored.

```csharp
// ✅ names the thing the values add up to
/// <summary>Represents the credentials of a Wi-Fi network.</summary>
// ❌ names the storage shape, which the type does not own
/// <summary>Represents the JSON payload of Wi-Fi fields.</summary>
```

### Construct
- must declare a `sealed record` — identity is the values, so value equality is the correct claim.
- must declare no key — a type carrying its own identity is an [entity](entity.md).

```csharp
// ✅
public sealed record WifiContentValueObject
// ❌ a key claims a row the type does not own
public sealed record WifiContentValueObject { public required Guid Id { get; init; } }
```

### Type name
- must suffix with `ValueObject` — `WifiContentValueObject`, `CodeRuleValueObject`.
- must reach for `Entity` instead when the type owns a row.
