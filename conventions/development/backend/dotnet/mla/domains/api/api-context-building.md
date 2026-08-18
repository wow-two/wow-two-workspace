# API context building

*Last updated: 2026-06-17*

> How a controller sources **caller context** — the actor plus ambient request facts — for an
> application request: `ICurrentUser` first, `User` / `HttpContext` as the fallback.

## `ICurrentUser`

- `ICurrentUser` is the app's identity abstraction — resolves the request's actor (user id / guest id).
- must read the actor through `ICurrentUser`, never raw claims.
- must inject it into the controller only when an action needs the actor (a two-model request).
- a single-actor app may not need it.

---

## Fallbacks

- must read facts `ICurrentUser` omits — source IP, headers — off `User` (`ClaimsPrincipal`) / `HttpContext`.
- must not read these in a handler — caller context is sourced at the edge.
- the context rides the application request ([mediator](../../domains/messaging/mediator/mediator.md)).

---

## Usage

- must pass the sourced context explicitly into the mapping — `request.ToCommand(currentUser.Id)`
  ([api messages](../../domains/api/api-messages.md)).
- must guard a missing actor at the edge — `if (currentUser.Id is not { } userId) return Unauthorized();`
