# Prototype

*Last updated: 2026-08-16*

> A new value derived from an existing one by copying it and changing the parts that differ.
> Purpose — keep a variant close to its source without a constructor that repeats every unchanged member.
> Use case — reach here when one value differs from another in a member or two.

## Shape

- must use the `record` `with` expression — the language owns this pattern.
- must not implement `ICloneable`, and must not call `MemberwiseClone` — neither states what the copy depth is.
- must not write a `Clone()` method on a model; `with` already produces the copy, typed.
- must treat the copy as **shallow** — a referenced collection is shared, so hold collections as immutable types.

```csharp
// ✅ the variant names only what differs
var preview = spec with { Logo = null, Size = PreviewSize };

// ❌ an untyped copy of unstated depth
var preview = (StyleSpec)spec.Clone();
```

---

## Use

- must reach for `with` to derive a request, a spec or a settings value for one call.
- must reach for it in tests to vary one field off a shared fixture value.
- may reach for it inside a `Mapper` performing a `T → T` transform ([mapper](../behavior/mapper.md)).

---

## Limits

- must not copy an `Entity` with `with` — an entity is identified by its key, and a copy claims the same identity
  ([entity](../data/entity.md)).
- must not use `with` to skip validation a constructor enforces; the copy re-runs no `init` guard on unchanged members.
- must not build a deep clone by hand — a value needing one is carrying mutable state it should not own.

---

## Components

- [entity](../data/entity.md) — the one model kind `with` must not copy.
- [mapper](../behavior/mapper.md) — where a `T → T` derivation belongs when it is more than one member.
- [constructs](../../../lla/constructs/constructs.md) — `record` rules, and what a copy costs.
