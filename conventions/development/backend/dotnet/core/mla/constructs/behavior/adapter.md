# Adapters

*Last updated: 2026-08-18*

> A third-party type fitted to an interface we declared, in-process.
> Purpose — keep a library's shape out of our call sites, so swapping it stays a registration change.
> Use case — a validation library, a cache handle, a feature-flag SDK; anything in-proc we did not design.

## Location

### Folder
- must sit in an `Adapters/` folder beside the interface it satisfies.

### File
- must give it its own file, named for the type →
  [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Adapts**, `<see cref>` the interface it satisfies, and name the library behind it.

```csharp
// ✅ both sides named
/// <summary>Adapts FluentValidation to <see cref="IValidator{T}"/>.</summary>
// ❌ names neither side, so the seam is invisible
/// <summary>Adapts the validation library.</summary>
```

### Construct
- must declare a `sealed class` implementing the interface it adapts to.

### Type name
- must suffix with `Adapter`, prefixed by the library — `FluentValidationAdapter<T>`.
- must reach for `Broker` instead when the dependency is out-of-process.
- must add nothing of its own — behavior beyond translation makes it a `Service`.

```csharp
// ✅
public sealed class HybridCacheRepository : ICacheBroker
// ❌ our own type needs no adapter; that is a `Mapper` or a `Service`
public sealed class CodeDtoAdapter
```
