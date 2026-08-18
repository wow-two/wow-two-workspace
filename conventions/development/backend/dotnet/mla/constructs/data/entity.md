# Entities

*Last updated: 2026-08-18*

> The type that owns a row and its identity.
> Purpose — the domain model stays ORM-free, so one model serves EF interceptors and hand-written SQL alike.
> Use case — any persisted type; a shape stored inside a row is a [value object](value-object.md).

## Location

### Folder
- must sit in an `Entities/` folder under the subdomain that owns it.

### File
- must give each entity its own file, named for the type.

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Represents**, and name what the row stands for in the domain.
- must not name the table — the mapping is the persistence layer's, not the model's.

```csharp
// ✅ names the thing, not the storage
/// <summary>Represents an external listing channel.</summary>
// ❌ names the table, which the model does not own
/// <summary>Represents a row of the channels table.</summary>
```

### Construct
- must declare a `sealed record`.
- must reference no ORM type; the domain assembly stays provider-free.
- must implement the keyed contract → [entity contracts](../../domains/persistence/schema/entity-contracts.md).
- member shape (`{ get; init; }`, positional) →
  [constructs](../../../lla/constructs/constructs.md) § *Data components*.

```csharp
// ✅
public sealed record ChannelEntity : IKeyedEntity<Guid>
// ❌ a positional record fixes the member order into every call site
public sealed record ChannelEntity(Guid Id, string Slug);
```

### Type name
- must suffix with `Entity`, singular — `ChannelEntity`, `ListingEntity`.
