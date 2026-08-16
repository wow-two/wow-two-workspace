# Brokers

*Last updated: 2026-08-15*

> The app-side seam over an external dependency — a payment provider, a blob store, a third-party API. A `Broker` speaks **our** model;
> the `Client` beneath it speaks the provider's ([clients.md](client.md)).
> Purpose — one place the app names an outside capability in its own vocabulary, so a provider swap does not reach past this type.
> Use case — reach for a broker when the app needs a capability rather than an endpoint: *charge a card*, *store a file*, *resolve a place*.

---

## Broker and Client — peers, not a hierarchy

A `Broker` usually sits **on top of** a `Client`, and neither owns the other. Each carries its own logic, and the seam between them is the
model translation:

- a `Broker` does not set the client's models, URLs, headers, or wire shape — those are the provider's, and the `Client` owns them.
- a `Client` does not set the broker's caching, degradation, or vocabulary — those are ours, and the `Broker` owns them.
- a `Broker` **may call client methods to feed its own policy** — reading a cache TTL off a provider response is the broker deciding, with
  the client's data.

A `Broker` with no `Client` under it is legal: an in-process SDK (blob storage, a vendor library) needs no HTTP wrapper.

| | `Broker` | `Client` |
|---|---|---|
| Speaks | our model | the provider's model |
| Names | a capability (`ChargeAsync`) | an endpoint (`PostPaymentIntentAsync`) |
| Owns | caching, degradation, translation | URLs, DTOs, headers, transport resilience |
| Swappable | the provider behind it | never — it *is* one provider |

---

## Resilience is the client's; degradation is the broker's

Retry, timeout, and circuit-breaking are **transport** facts — a 503, a socket timeout, a 429. Only the type that knows the channel can
configure them, so the pipeline binds to the `Client` ([clients.md](client.md) § *Resilience (mandatory)*). HTTP is that section's worked
example, not the boundary of the rule: a broker over an in-process SDK has no transport of its own to protect.

What the app does **after** the retries are exhausted is a different decision, and it is ours:

- must place the degradation policy on the `Broker` — serve stale cache, return an empty result, or surface a failure.
- must not hand-roll retry inside a `Broker` — that is the client's pipeline leaking upward, and it multiplies the attempts.
- must state the degradation in the broker's `<remarks>` when a caller has to act on it — *"returns the last cached rate when the provider is
  unreachable"* is a directive, not trivia.

---

## Naming and documentation

- `{Capability}{Provider}Broker` or `{Provider}{Capability}Broker` — `StripeBillingBroker`
  (`smart-qr-poc/…/SmartQr.Infrastructure/Billing/Services/`).
- `/// <summary>` starts with **Integrates** — `Integrates the Stripe payment provider.`
  ([documentation/summary.md](../../lla/documentation/summary.md)).
- one interface per broker, named for the capability (`IBillingBroker`), so the provider name lives only in the implementation.

---

## Open — not yet settled

Deliberately unwritten; decide these against a second real broker rather than inventing them now:

- class shape — constructor injection depth, whether a broker may hold state.
- lifetime — scoped vs singleton, and what that implies for its cache.
- configuration — whether a broker binds its own `Settings` section or reads the client's.

---

## See also

- [clients.md](client.md) — the provider-facing half, and the resilience pipeline
- [component-names.md](components.md) § *`Client` vs `Broker`* — which model the type speaks
- [documentation/summary.md](../../lla/documentation/summary.md) — the `Integrates` starter
