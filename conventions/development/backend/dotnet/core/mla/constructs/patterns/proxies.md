# Proxies

*Last updated: 2026-08-16*

> A stand-in that carries an interface's calls to a real implementation living somewhere else.
> Purpose — let a caller depend on a plain interface while the transport, the generation or the hook stays invisible.
> Use case — reach here when the implementation is generated or intercepted rather than written.

## Shape

- must take a proxy from a source that generates it — Refit for an HTTP API (`AddRefitApiClient<TApi>`,
  `src/Http/Refit/`), EF Core for a save-time interceptor (`AuditInterceptor`, `src/Data/EntityFrameworkCore/Audit/`).
- must declare the interface the proxy implements as ours, and keep it free of the generator's attributes where the
  generator allows it.
- must not hand-write a runtime proxy — no `DispatchProxy`, no IL emit, no dynamic-proxy package.
- must keep an interception hook single-purpose: one interceptor stamps audit fields, another applies soft delete
  (`SoftDeleteInterceptor`), never one doing both.

```csharp
// ✅ the interface is the contract, Refit generates the implementation
public interface IBillingApi
{
    [Post("/v1/payment-intents")]
    Task<PaymentIntentResponse> CreateIntentAsync(CreateIntentRequest request, CancellationToken cancellationToken);
}

builder.Services.AddRefitApiClient<IBillingApi>("https://billing.internal");
```

---

## Use

- must reach for a generated proxy for a typed HTTP client — it is the default over a hand-written one
  ([client](../behavior/client.md)).
- must reach for an EF interceptor when the behavior must fire for every save, whoever calls it.
- may reach for a lazy proxy only where the framework supplies it and the cost is measured.

---

## Limits

- must not use a proxy to hide a network call from the caller — an interface that can time out says so in its shape
  (`Async`, `CancellationToken`).
- must not enable EF lazy-loading proxies — an N+1 that fires from a property read is invisible at the call site.
- must not put business rules in an interceptor; an interceptor stamps and filters, a handler decides.
- must not proxy what a decorator already covers — a hand-written wrapper is readable, a generated one is not
  ([decorators](decorators.md)).

---

## Components

- [client](../behavior/client.md) — Refit registration, resilience, and the typed-client alternative.
- [entity](../data/entity.md) — the audit / soft-delete / tenant traits the interceptors act on.
- [decorators](decorators.md) — the hand-written wrapper, when the added behavior needs a name.
