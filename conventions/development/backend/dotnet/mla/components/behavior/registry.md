# Registries

*Last updated: 2026-08-16*

> A type that owns a set of key-to-type bindings and answers lookups against it.
> Purpose — hold what callers registered at composition time, and fail loudly when the set is incomplete.
> Use case — reach here when a discriminator, a slug or an enum member must resolve to a type.

## Location

### Folder
- must sit beside the types it binds, in the layer that composes them.

### File
- must give each registry its own file, named for the type.

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Binds**.
- must name the key and what it resolves to.

```csharp
// ✅ key and target
/// <summary>Binds each content variant to its discriminator.</summary>
// ❌ Holds is the const field's starter, and names no key
/// <summary>Holds the content variants.</summary>
```

### Type name
- must suffix with `Registry`.

## Content

### Member docs

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a lookup with **Gets**, and a registration with **Adds**.

#### [Exceptions](../../../lla/notation/documentation/exceptions.md)
- must document the throw for an unbound key — completeness is the registry's to enforce.

```csharp
// ✅ the incompleteness is the contract
/// <summary>Gets the type bound to the discriminator.</summary>
/// <param name="discriminator">The enum member to resolve.</param>
/// <exception cref="InvalidOperationException">No type is bound to the member.</exception>
```

### Members
- must accept registrations at composition time only, never after the first lookup.
- must throw when a key in the closed set has no binding — a silent miss hides a wiring fault.

```csharp
// ✅ the miss is loud
public Type Get(CodeContentType key) => _bindings.TryGetValue(key, out var type)
    ? type
    : throw new InvalidOperationException($"No type bound to {key}.");

// ❌ a null hides a wiring fault until the caller dereferences it
public Type? Get(CodeContentType key) => _bindings.GetValueOrDefault(key);
```

## See also

- [../components.md](../components.md) — `Registry` vs `Repository`
- [mapper.md](mapper.md) — the type handed its data
