# Circuit breaker

*Last updated: 2026-08-16*

> A guard that stops calling a failing dependency for a while, instead of retrying into it.
> Purpose — keep one sick dependency from consuming the caller's threads and turning into an outage of our own.
> Use case — reach here whenever code leaves the process — an HTTP call, a broker publish, a vendor SDK.

## Shape

- must take retry, breaker and timeout from **one** pipeline attached to the `Client`, never hand-rolled —
  `AddSdkResilience` over `HttpResilienceOptions` ([http](../../domains/integrations/http/http.md) § *Resilience*).
- must register a client through a helper that already applies it — `AddRefitApiClient<TApi>` or
  `AddResilientClient<TClient>`; a bare `HttpClient` never ships.
- must keep the order retry → circuit breaker → per-attempt timeout, inside one total-request timeout — tuning is
  through options, not by reordering handlers.
- must retry only what is safe to repeat — a read, or a write carrying an idempotency key
  ([mediator](../../domains/messaging/mediator/mediator.md) § *Pipeline behaviors*).
- must place the **degradation** decision on the `Broker` — what the app does once retries are exhausted is ours
  ([broker](../behavior/broker.md)).
- must use `IRetryPolicy` / `IEventResiliencePipeline` on the messaging side (`src/Messaging/Reliability/`), not the
  HTTP pipeline; the transports differ.

```csharp
// ✅ one pipeline, tuned through options
builder.Services.AddRefitApiClient<IBillingApi>("https://billing.internal");
builder.Services.AddResilientClient<WeatherClient>(new Uri("https://weather.example.com"));
```

---

## Use

- must reach for the pipeline on every outbound call, including a call to a sibling service we own.
- must reach for a shorter breaker window on a hot path, where a stuck call costs a request thread.
- must reach for a stale-cache fallback on the broker when the capability degrades better than it fails.

---

## Limits

- must not wrap a retry around a call that is already retried — nested policies multiply the attempt count.
- must not retry a `4xx`; a rejected request is rejected again, and a `429` is a wait, not a retry.
- must not retry inside a `Broker`, a `Handler`, or a `catch` block — the pipeline owns the attempts.
- must not breaker-protect an in-process call; a local failure is a bug, and hiding it delays the fix.
- must not tune Polly directly — every knob is on `HttpResilienceOptions`.

---

## Components

- [client](../behavior/client.md) — where the pipeline binds, and the registration helpers.
- [broker](../behavior/broker.md) — the degradation policy, and why it is not the client's.
- [decorators](decorators.md) — the pattern a hand-rolled retry imitates, and why it must not.
- [problem details](../../../../shapes/service/platform/responses/problem-details.md) — how an exhausted call reaches the caller.
