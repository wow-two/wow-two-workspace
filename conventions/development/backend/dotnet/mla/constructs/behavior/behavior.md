# Behavior components

*Last updated: 2026-08-16*

> The component kinds whose identity is what they do.
> Purpose — one suffix per verb, so a name carries the responsibility rather than the shape.
> Use case — naming or declaring a type that acts rather than holds.

## The kinds

| Kind | Does |
|---|---|
| [service](service.md) | business logic and orchestration — the fallback when no narrower role fits |
| [repository](repository.md) | reads and persists rows |
| [client](client.md) | calls one external provider in its own vocabulary |
| [broker](broker.md) | presents our vocabulary over an external dependency |
| [adapter](adapter.md) | fits a third-party type to an interface we declared |
| [handler](handler.md) | receives one dispatched message |
| [controller](controller.md) | dispatches at the HTTP edge |
| [validator](validator.md) | validates one request |
| [mapper](mapper.md) | transforms an input it is handed |
| [registry](registry.md) | owns key → type bindings registered at composition |
| [policy](policy.md) | decides whether, when or how often another operation runs |
| [builder](builder.md) | accumulates one value, ending in `Build()` |
| [hosted service](hosted-service.md) | runs work off the request path |

---

## Shared rules

- must declare a `sealed class` — value equality is wrong on a type whose identity is what it does.
- must take collaborators through the constructor, never a service locator.
- must start the type summary with the role's own verb, and an interface over it with **Defines**.
