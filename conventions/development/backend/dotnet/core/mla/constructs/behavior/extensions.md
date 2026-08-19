# Extensions

*Last updated: 2026-08-19*

> The static tier over a **domain**'s types — logic that needs no collaborator and owns no state.
> Purpose — behaviour that needs nothing injected does not earn a service, and does not belong on the type it acts on.
> Use case — encoding, projection, mapping-in-the-small, or registration logic over one domain's types.

## Location

### Folder
- must sit in an `Extensions/` folder under the domain it extends.

### File
- must give it its own file, named for the type →
  [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Extends**, and name the domain.
- must not name the receiver type — a class extends a domain, not one type.

```csharp
// ✅ names the domain
/// <summary>Extends the codes domain with content encoding.</summary>
// ❌ names one type, so a second receiver has nowhere to go
/// <summary>Extends CodeEntity.</summary>
```

### Construct
- must declare a `public static class` → [constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must take no collaborator — a method needing one belongs to a [service](service.md).
- must hold no mutable state.

### Type name
- must be named `{Domain}Extensions`, after the domain the logic belongs to.
- must not name the type it extends — `CodeExtensions` covers `CodeEntity` and `CodeModel` alike.
- must not name the layer — no `ApplicationExtensions`.

---

## Neighbours

- [extensions](../../components/extensions.md) — receivers, members, and the `TryX` ladder
- [service](service.md) — where the same logic goes once it needs a collaborator
