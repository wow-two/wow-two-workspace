# Api requests

*Last updated: 2026-08-18*

> The presentation-layer body a client sends, bound by one controller action.
> Purpose — the `Api` qualifier is what tells the wire body apart from the application message it maps to.
> Use case — every endpoint that accepts a body.

## Location

### Folder
- must sit in the `Requests/` folder of the API project, never in `Application/`.

### File
- must give each request its own file, holding its edge-mapping extensions class beside it.

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Represents**, and name the body it carries.
- must carry no `<remarks>` — a request body directs the consumer to nothing.

```csharp
// ✅ names the action's body
/// <summary>Represents the create-namespace request body.</summary>
// ❌ names the type instead of the body
/// <summary>Represents an api request.</summary>
```

### Construct
- must declare a `public sealed record`.

### Type name
- must be named `{Verb}{Noun}ApiRequest`, verb-first — it exists for one controller action.
- must take the entity as the noun, or the domain when the action spans more than one entity.
- must carry `Api` — never a bare `Request`, and never `Dto`, which is the payload's suffix.

```csharp
// ✅
public sealed record NamespaceCreateApiRequest
// ❌ bare `Request`, so the layer is unreadable from the name
public sealed record CreateNamespaceRequest
```
