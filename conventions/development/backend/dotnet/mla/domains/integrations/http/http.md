# Http

*Last updated: 2026-08-16*

> How an outbound HTTP call is registered, made resilient, and layered with cross-cutting handlers.
> Purpose — one managed path per call means no socket exhaustion, no stale DNS, and no hand-rolled Polly.
> Use case — registering a [client](../../../constructs/behavior/client.md), or tuning what its pipeline does.

## Registration

- must register every client through `IHttpClientFactory` — never `new HttpClient()`.
- must prefer `AddRefitApiClient<TApi>` for a new client; it bundles base address, SDK JSON and resilience.
- must use `AddResilientClient<TClient>` for a plain typed client, or its named overload for a factory-resolved one.
- must chain `.AddSdkResilience(...)` onto a manual `AddHttpClient<T>()` — a bare registration is non-conformant.
- must override Refit JSON at the preset layer, never by passing a hand-built `RefitSettings`.

```csharp
// ✅ Refit, the default for a new client
builder.Services.AddRefitApiClient<IBillingApi>("https://billing.internal");
// ✅ manual registration, resilience chained on
builder.Services.AddHttpClient<TelegramClient>(c => c.BaseAddress = new Uri("https://api.telegram.org/"))
    .AddSdkResilience();
```

---

## Resilience

`AddSdkResilience` wraps a client in retry → circuit breaker → per-attempt timeout, inside a total-request timeout.
It tunes `IHttpClientBuilder.AddStandardResilienceHandler(...)` through `HttpResilienceOptions`.

- must tune through `HttpResilienceOptions`, never a custom `DelegatingHandler` or a Polly policy.
- must keep `AttemptTimeout` shorter than `TotalRequestTimeout`.
- must keep `CircuitBreakerSamplingDuration` at least twice `AttemptTimeout`.

| Option | Default | Meaning |
|---|---|---|
| `MaxRetryAttempts` | `3` | retries after the first try |
| `AttemptTimeout` | `10s` | per-attempt timeout |
| `TotalRequestTimeout` | `30s` | budget for the whole logical request |
| `CircuitBreakerSamplingDuration` | `30s` | failure-rate window |
| `CircuitBreakerFailureRatio` | `0.1` | trip threshold |

Tracing is wired by the observability package — every call through the pipeline is instrumented, no per-client setup.

---

## Cross-cutting handlers

Chain these onto the same `IHttpClientBuilder`, after the registration helper. Each carries its own options type.

- OAuth2 client-credentials bearer, cached → `OAuth2ClientCredentialsHttpClientBuilderExtensions`
- mutual TLS with a client certificate → `MutualTlsHttpClientBuilderExtensions`
- request hedging, parallel attempts → `HttpHedgingBuilderExtensions`
- inbound → outbound header propagation → `HeaderPropagationServiceCollectionExtensions`

---

## Errors

- must let an HTTP error bubble out of the client — the caller translates it.
- must not catch `HttpRequestException` inside the client; the context is lost with it.
- must not retry inside the client — retry belongs to the pipeline.
- must deserialize a provider's typed error body into a model, returning a result or throwing a typed exception.
