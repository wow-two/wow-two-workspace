# Indexers

*Last updated: 2026-08-16*

> A property that takes a key, so a type reads like the collection it wraps.
> Purpose — let a caller reach an element by key without a method name repeating the type's own noun.
> Use case — reach here when a type wraps exactly one keyed set and the key is the whole selector.

## Location

### Folder
- must live in the file of the type it belongs to; an indexer has no folder of its own.

### File
- must sit with its type, never split into a partial.

## Declaration

### Type doc
- must document the enclosing type, not the indexer — the indexer is a member.

### Type name
- must be `this[…]`; C# fixes the name, so nothing is chosen here.

## Content

### Member docs

#### [Summary](../notation/documentation/summary.md)
- must start with **Gets**, **Gets or sets** or **Sets**, matching its accessors.
- must state what the key **selects**, never only what is returned.

#### [Params](../notation/documentation/params.md)
- must carry a `<param>` for the key.

#### [Returns](../notation/documentation/returns.md)
- must name the element and the case where the key matches nothing.

```csharp
// ✅ the key's role is visible
/// <summary>Gets the routing rule at the given order.</summary>
/// <param name="order">The rule's position in the evaluation chain.</param>
/// <returns>The rule at that order, or <c>null</c> when none is set.</returns>
public CodeRule? this[int order] => _rules.GetValueOrDefault(order);

// ❌ says nothing the signature does not
/// <summary>Gets the rule.</summary>
```

### Members
- must expose one indexer per type; a second key means the type wraps two sets.
- must not throw for a missing key when a nullable return can state the same thing.
- may use `=>` for the accessor that returns the element — a keyed lookup returns, and a lookup does not grow
  ([style](../notation/style/style.md) § *The body*).

## See also

- [components](components.md) — the self-sufficiency gate
- [summary](../notation/documentation/summary.md) — accessor starters
