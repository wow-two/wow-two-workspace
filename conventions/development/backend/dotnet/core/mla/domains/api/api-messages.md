# Api messages

*Last updated: 2026-08-19*

> The HTTP edge set — the body a client sends, the envelope it reads back, and the payload inside it.
> Purpose — the wire shape is a contract with a client, so it changes on the client's schedule, not the domain's.
> Use case — adding an endpoint, or changing what one accepts or returns.

## Request naming

Declaration and suffix → [api request](../../constructs/data/api-request.md). This adds only what the flow decides.

- must merge create and update into `{Noun}CreateUpdateApiRequest` — the id rides the route, so the bodies match.
- must split into `{Noun}Create` and `{Noun}Update` only once the two bodies diverge.

---

## Request sub-blocks

A body sub-block nested inside a request carries no verb of its own.

- must name a nested sub-block **noun-first**, so one block serves every action that embeds it.
- must keep a request-specific sub-block in the API project, and reference the shared shape otherwise.
- `StyleApiRequest` is shared across `PreviewCodeApiRequest`, `CreateCodeApiRequest` and `UpdateCodeApiRequest`.

---

## Request members

- must carry only what the client sends — never the actor, the source IP, a route id, or a server timestamp.
- must mark every non-nullable property `required`, each with a `Gets {what}.` summary.
- must leave validation to the application request's pipeline — no validation attributes on the body.

---

## Response

- must wrap a success in `ApiResponse<T>`, so the client always reads `.data`.
- must send an error as RFC 9457 ProblemDetails, never wrapped →
  [problem details](../../../../shapes/service/platform/responses/problem-details.md).
- must leave `204 No Content` and file streams unwrapped — there is no payload for `.data`.
- must build the success body through `ApiResponse<T>.Ok(data)` alone, in the success arm of `.Match`.
- must keep the envelope to its payload — no `message`, no `meta`; anything more belongs in the payload.

The envelope ships in the SDK; its shape is not restated here. The payload is a [dto](../../constructs/data/dto.md).

- must map the handler's [model](../../constructs/data/model.md) to a `Dto` in the controller, never below it.
- must keep `Dto` out of every layer under the edge — a service returns a model, and the edge projects it.

---

## Edge mapping

The application message is built at the edge by an extension method co-located with the api request, same file.

- must declare one `static` class per request, in the request's own file — `{Request}Extensions`.
- must name the method for the target's role — `ToCommand(...)`, `ToQuery(...)`.
- must pass caller context and route ids explicitly — `request.ToCommand(callerContext, id)`.
- must never read caller context inside a handler.
- must give the mapping method a block body — it builds and returns.

```csharp
// ✅ co-located, and the actor arrives as a parameter
/// <summary>Extends <see cref="NamespaceCreateApiRequest"/> for application-request mapping.</summary>
public static class NamespaceCreateApiRequestExtensions
{
    /// <summary>Maps the request to its <see cref="NamespaceCreateCommand"/>.</summary>
    public static NamespaceCreateCommand ToCommand(this NamespaceCreateApiRequest request, string actor)
    {
        return new NamespaceCreateCommand(request.Slug, request.Name, actor);
    }
}
// ❌ a separate mapper class, reading the actor instead of taking it
public sealed class RequestMapper(ICurrentUser user)
{
    public NamespaceCreateCommand Map(NamespaceCreateApiRequest request) => new(request.Slug, request.Name, user.Id);
}
```

---

---

## Nested sub-blocks

A body one action binds is an `ApiRequest`. A block nested inside it is not.

- must name a nested sub-block `{Noun}Dto`, whether it appears in a request, a response, or both.
- must keep `{Verb}{Noun}ApiRequest` for the top-level body alone — the suffix is verb-first, a sub-block
  has no verb of its own, and `StyleApiRequest` already fails that rule.
- must not read `Dto` here as a response-only word — `Dto` is the wire shape, and the wire runs both ways.
- must map a sub-block at the same edge as its parent: controller in, controller out.
