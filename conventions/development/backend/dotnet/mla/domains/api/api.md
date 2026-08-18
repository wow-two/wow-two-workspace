# Api

*Last updated: 2026-08-16*

> The HTTP surface a service exposes — what a client may send, and what it reads back.
> Purpose — the wire is a contract with a client, so it changes on the client's schedule, not the domain's.
> Use case — adding an endpoint, or changing what one accepts or returns.

## Contract

- must bind one [api request](../../constructs/data/api-request.md) per action, and map it at the edge.
- must wrap a success in the envelope, and send an error as ProblemDetails → [api messages](api-messages.md).
- must keep caller context off the body — the edge merges it into the application message.
- must point the dependency api → application; an application message never references an api one.
- must hold no logic in the delivery type → [controller](../../constructs/behavior/controller.md).

---

## Action naming

- must name an action for the bare verb — the resource is implied by the controller.
- must add a suffix only to distinguish a variant or a nested resource — `CreateTimedToken`, `GetTokens`.

| HTTP + route | Action | Summary |
|---|---|---|
| `GET api/products` | `Get` | `Gets all {plural}.` |
| `GET api/products/{id}` | `GetById` | `Gets a {singular} by id.` |
| `POST api/products` | `Create` | `Creates a {singular}.` |
| `PUT api/products/{id}` | `UpdateById` | `Updates a {singular}.` |
| `DELETE api/products/{id}` | `DeleteById` | `Deletes a {singular}.` |

- must state the action in the summary, never the HTTP verb — `Sets the code's active state.`

---

## Action attributes

- must carry `[ProducesResponseType<ApiResponse<T>>(2xx)]` — the one typed success body.
- must carry `[ProducesResponseType(status)]` per failure it returns, with no payload type.
- may carry `[Consumes(mediaType)]` to constrain a non-JSON body.
- may carry `[Tags]`, `[EndpointSummary]` or `[EndpointDescription]` when the generated spec text needs help.

---

## Action content

- must return `Task<IActionResult>` unless the response is a stream.
- must use a block body from the start — an action binds, dispatches and maps, three steps minimum.
- must bind the payload through an [api request](../../constructs/data/api-request.md).
- must read the actor through `ICurrentUser` → [api context](api-context-building.md).
- must reach for `User` or `HttpContext` only for a fact `ICurrentUser` does not expose.
- must take a `CancellationToken` last, and pass it down.
- must build the application request through the request's own mapping method.
- must save the dispatch result to a local — never map, send and return on one line.
- must not catch, validate, orchestrate or hand-map.

---

## Response mapping

- must collapse the saved result with `.Match(onSuccess, onFailure)`.
- must take the failure status from the injected `IErrorHttpStatusCodeMapper`, never a literal.
- must map a failure through `Problem(...)` with context — never bare `NotFound()` or `BadRequest()`.

| Outcome | Return |
|---|---|
| list or single read | `Ok(ApiResponse<T>.Ok(dto))` |
| created, resource has an id | `CreatedAtAction(nameof(GetById), new { id }, ApiResponse<T>.Ok(dto))` |
| mutated, no body | `NoContent()` |
| binary or stream | `File(bytes, contentType)` |

- `CreatedAtAction` points at `nameof(GetById)` so the `Location` header round-trips to the read action.

```csharp
// ✅ local, then Match, then a mapped status
var result = await sender.SendAsync(command, ct);

return result.Match<IActionResult>(
    ok => CreatedAtAction(nameof(GetById), new { id = ok.Data.Product.Id },
        ApiResponse<ProductDto>.Ok(ok.Data.Product)),
    fail => Problem(detail: fail.Error.Message, statusCode: statusMapper.ToStatusCode(fail.Error)));
// ❌ try/catch at the edge, raw body, bare status
try { return Ok(await sender.SendAsync(command, ct)); }
catch (NotFoundException) { return NotFound(); }
```

---

## Providers

| Provider | Delivers through | Docs |
|---|---|---|
| MVC controllers | an attribute-routed `Controller` binding the body | [controller](../../constructs/behavior/controller.md) |
| minimal API | an endpoint delegate registered at composition | — |

- must pick one delivery style per service — two routing models over one surface hide which owns a path.
