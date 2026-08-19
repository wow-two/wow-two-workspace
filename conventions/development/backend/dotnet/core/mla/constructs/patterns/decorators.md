# Decorators

*Last updated: 2026-08-16*

> A type implementing an interface by wrapping one other implementation of it and adding a behavior around the call.
> Purpose — add caching, logging or auth to a collaborator without editing it and without a flag in its callers.
> Use case — reach here when every caller of one interface needs the same extra behavior.

## Shape

- must implement the interface it wraps and take that same interface through the constructor.
- must name the type for what it **adds**, then the wrapped type's noun — `Caching{Noun}Broker`,
  `Logging{Noun}Service`.
- must delegate every member, including the ones it does not change — a missing member is a silent behavior split.
- must be `sealed`, and must hold no state beyond what its added behavior needs.
- must register the decorator as the interface, resolving the inner implementation by its concrete type — we take no
  container-decoration package.

```csharp
// ✅ illustrative — the inner instance is a constructor parameter, and both registrations are explicit
services.AddSingleton<MaxMindGeoBroker>();
services.AddSingleton<IGeoBroker>(sp =>
    new CachingGeoBroker(sp.GetRequiredService<MaxMindGeoBroker>(), sp.GetRequiredService<ICache>()));
```

---

## Use

- must reach for a decorator when the added behavior is orthogonal — caching, metrics, an auth header.
- must reach for it at a framework seam that already decorates — `DelegatingHandler` on an `HttpClient`
  (`OAuth2ClientCredentialsHandler`, `src/Http/Auth/OAuth2ClientCredentials/`).
- must prefer a decorator over a boolean parameter that switches the same behavior inside the type.

---

## Limits

- must not decorate to add a **step of the same work** — an ordered N-step flow is a pipeline
  ([pipelines](pipelines.md)).
- must not hand-roll retry or circuit-breaking as a decorator — that pipeline is the `Client`'s
  ([circuit breaker](circuit-breaker.md)).
- must not stack more than two decorators on one interface; past that the wrapping order is invisible at the call site
  and belongs in a pipeline.
- must not let a decorator change the contract's semantics — a decorator that swallows a failure is a new
  implementation, not a wrapper.

---

## Components

- [pipelines](pipelines.md) — the N-step sibling, where order is declared once instead of nested.
- [broker](../behavior/broker.md) — the usual decoration target, and the owner of degradation policy.
- [proxies](proxies.md) — the generated stand-in; a decorator is written by hand and adds a named behavior.
- [host configuration](../../../../shapes/service/platform/startup/host-configuration.md) — where the two registrations live.
