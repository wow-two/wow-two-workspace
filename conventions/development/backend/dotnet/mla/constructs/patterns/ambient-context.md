# Ambient context

*Last updated: 2026-08-16*

> A per-request value flowing with the async context, readable without being passed down the call chain.
> Purpose — reach a request fact from a singleton the request never constructed — an EF interceptor, a query filter.
> Use case — reach here only when the reader cannot take the value as a parameter or a constructor dependency.

## Shape

- must back the context with `AsyncLocal<T>` behind an interface, registered as a singleton whose value is
  per-request — `ITenantContext` / `AmbientTenantContext` (`src/Tenancy/Core/`).
- must split read from write — a consumer takes the read interface, and only the resolving middleware takes the
  settable one (`ISettableTenantContext`).
- must set the value at exactly one place, in middleware, and clear it when the scope ends.
- must give the unset case a defined meaning on the read side — `HasTenant`, `TenantId` nullable, never a throw.
- must not expose the context through a `static` accessor; it is injected like anything else.

```csharp
// ✅ read-only interface injected, AsyncLocal behind it, one writer
public interface ITenantContext
{
    string? TenantId { get; }
    bool HasTenant { get; }
}
```

---

## Use

- must reach for it only where a **singleton** must read a request fact — a query filter, a save interceptor.
- must reach for it for a cross-cutting fact with no owner in the domain — tenant, correlation id.
- must prefer a scoped service whenever the reader is itself scoped; scoped injection is the plain answer.

---

## Limits

- must not use ambient context for **time** — `TimeProvider` is injected, and a static clock is banned
  ([time](../../components/time.md)).
- must not use it for the **actor** — caller context is sourced at the edge and rides the application request; a
  handler never reads `ICurrentUser` or `HttpContext` ([api context building](../../domains/api/api-context-building.md)).
- must not use it to carry a business input; an input a handler needs is a property on the message
  ([handler](../behavior/handler.md)).
- must not read it from a `BackgroundService` — there is no request, so the value is whatever the last one left.
- must not add a second ambient context without the coining gate; each one is a hidden parameter every reader inherits.

---

## Components

- [time](../../components/time.md) — the ambient value we explicitly refuse.
- [api context building](../../domains/api/api-context-building.md) — how the actor reaches a handler instead.
- [service locator](service-locator.md) — the sibling anti-pattern: hidden dependency rather than hidden value.
- [entity](../data/entity.md) — the tenant trait the ambient context populates.
