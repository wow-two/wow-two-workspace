# Request models

*Last updated: 2026-08-15*

> **API request** — the presentation-layer body a client sends, named `{Verb}{Noun}ApiRequest`; a controller binds it and maps it to its **application request** (the mediator `Command` / `Query` — see [mediator.md](../domains/messaging/mediator.md)).
> Both are requests — the `Api` / `Application` qualifier tells the layers apart.

## Request shape

### Documentation

#### Summary

- [Summary doc block conventions](../../lla/documentation/summary.md)
- keyword - `Represents the {verb}-{noun} request body.`, e.g. `Represents the create-code request body.`

#### Remarks

- omit — a request model is a plain body DTO; there's nothing to direct the consumer to

### Declaration

- must be a `public sealed record`
- must be named `{Verb}{Noun}ApiRequest`, **verb-first** — `CreateCodeApiRequest`, `UpdateCodeApiRequest`. An api request exists for one controller action, so it reads like the action it binds to; the **application request** is the noun-first one, because those are searched by domain ([mediator.md](../domains/messaging/mediator.md) § *The application request*)
- the **noun** is the entity, or the **domain / subdomain** when the action isn't scoped to one entity (a multi-entity create/update) - not forced to a single entity
- must **merge** create + update into one `{Noun}CreateUpdateApiRequest` - the id rides the route, not the body, so the two bodies are identical; split into `{Noun}Create` / `{Noun}Update` only once they diverge
- `Api` marks the presentation layer - never bare `Request` or `Dto` (the response suffix)
- must live in the API project under `Requests/` - never in `Application/`

### Members

- **body-only** - only what the client sends; never the actor, source IP, route id, or a server timestamp (those are caller context, merged in the mapping)
- `required` on every non-nullable property; each carries a `Gets {what}.` summary (property doc rule → [documentation/summary.md](../../lla/documentation/summary.md))
- **nested body models take `*Dto`, not `*ApiRequest`** - only the top-level endpoint body is an `*ApiRequest` (a form-bind request); a nested `CodeStyleDto` / `CodeRuleDto` is a data shape. A request-specific nested `*Dto` lives in the API project + maps to its application model; otherwise reference the shared `*Dto`
- no validation attributes - business validation is the application request's, in the pipeline ([validation.md](validator.md))

### Examples

#### Good

```csharp
/// <summary>Represents the create-namespace request body.</summary>
public sealed record NamespaceCreateApiRequest
{
    /// <summary>Gets the namespace slug.</summary>
    public required string Slug { get; init; }

    /// <summary>Gets the namespace display name.</summary>
    public required string Name { get; init; }
}
```

#### Bad

```csharp
// ❌ actor on the body (server-set) · bare `Request` name · mutable class · no member docs
public class CreateNamespaceRequest
{
    public Guid Actor { get; set; }
    public string Slug { get; set; }
    public string Name { get; set; }
}
```

---

## Mapping

The application request is built **at the edge** by an extension method co-located with the api request (same file — not a separate mapper class). It merges the caller context + route ids the body can't carry.

- one `static` extensions class per request, in the request's file - `{Request}Extensions`
- method named by the target's role - `ToCommand(...)` / `ToQuery(...)`
- class summary starts with **Extends** - `Extends <see cref="{Request}"/> for application-request mapping.` ([documentation/summary.md](../../lla/documentation/summary.md) § *Extension classes*)
- method summary refs the target via `cref` - `Maps the request to its <see cref="{Command|Query}"/>.`
- pass caller context + route ids explicitly - `request.ToCommand(callerContext, id)`; never read them in the handler
- the application request **never references the api request** - the dependency points one way (api request → application request)
- the mapping method **builds + returns** the application request — block body, not `=>` ([members.md](../../lla/members.md))
- the controller binds the api request, then maps at the edge — `request.ToCommand(callerContext, id)` → send ([controllers.md](controller.md))

#### Good

```csharp
/// <summary>Extends <see cref="NamespaceCreateApiRequest"/> for application-request mapping.</summary>
public static class NamespaceCreateApiRequestExtensions
{
    /// <summary>Maps the request to its <see cref="NamespaceCreateCommand"/>.</summary>
    public static NamespaceCreateCommand ToCommand(this NamespaceCreateApiRequest request, string actor)
    {
        return new NamespaceCreateCommand(request.Slug, request.Name, actor);
    }
}
```

#### Bad

```csharp
// ❌ a separate mapper class far from the request · reads the actor instead of taking it as a param
public sealed class RequestMapper(ICurrentUser user)
{
    public CreateNamespaceCommand Map(CreateNamespaceApiRequest request) => new(request.Slug, request.Name, user.Id);
}
```
