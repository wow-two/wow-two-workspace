# Clients

*Last updated: 2026-08-15*

> External HTTP/API integration classes that wrap a single provider's API; one client per provider, no business logic inside.
> Purpose — every outbound call rides one `IHttpClientFactory`-managed, resilience-wrapped path, so no socket exhaustion, stale DNS, or hand-rolled Polly.
> Use case — reach for a client whenever a service calls a third-party or sibling REST/SDK endpoint (Telegram, billing, maps, GitHub).

---

## Location

Clients live in integration folders grouped by provider:

- Common (shared across services) → `{Repo}.Common/Integrations/{Provider}/` — e.g. `TelegramClient`
- Service-specific → `{Service}/Infrastructure/Integrations/{Provider}/` — e.g. `LocationApiClient`

---

## Modeling

### Class shape

- **Non-static** class
- **`HttpClient`** injected via primary constructor (typed `HttpClient` pattern) — or provider-specific SDK type when wrapping an SDK
- **Sealed** unless inheritance is needed
- **Naming** — suffix with `Client`, prefixed with provider name

### Lifetime

Every outbound client is a typed/named `HttpClient` managed by `IHttpClientFactory` — **never** a manually-`new`'d `HttpClient` (socket
exhaustion + no DNS refresh). Two paths, both ending in the SDK resilience pipeline:

- **SDK helper (preferred)** — register via `AddResilientClient<T>` / `AddRefitApiClient<TApi>`; the pipeline is applied for you (see
  [Resilience](#resilience-mandatory)).
- **Manual `AddHttpClient<T>()`** — only when you need configuration the helpers don't expose. You **must** chain `.AddSdkResilience(...)` yourself.

```csharp
builder.Services.AddHttpClient<TelegramClient>(c =>
{
    c.BaseAddress = new Uri("https://api.telegram.org/");
    c.DefaultRequestHeaders.Add("Accept", "application/json");
})
.AddSdkResilience();   // ← required; bare AddHttpClient is non-conformant
```

### Configuration

- Settings injected via `IOptions<TSettings>` — base URL, API key, timeout
- Settings type follows [settings.md](settings.md) rules — `sealed record`, `init`-only
- Never hard-code base URLs or credentials in the client

---

## Resilience (mandatory)

> **Transport resilience is the client's, degradation is the broker's** ([brokers.md](broker.md) § *Resilience is the client's*). Retry,
> timeout, and circuit-breaking answer to the channel, so they bind here; what the app does once the retries are exhausted is the broker's
> call. HTTP below is the worked example, not the boundary — a client over a vendor SDK owes the same guarantee through that SDK's own knobs.

> **Rule:** every outbound `HttpClient` carries the SDK resilience pipeline. Either register via `AddResilientClient<T>` / `AddRefitApiClient<TApi>`
> (which apply it), or chain `AddSdkResilience(...)` onto a manual `AddHttpClient<T>()`. **Never ship a bare `HttpClient`**, and **never** hand-roll Polly
> handlers — tune through `HttpResilienceOptions` instead.

SDK source: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/http/`.

### What the pipeline does

`AddSdkResilience` (in `HttpResilienceBuilderExtensions`) wraps the client in one standard handler — retry → circuit breaker → per-attempt timeout, all
inside a total-request timeout. It is a thin tuning layer over `IHttpClientBuilder.AddStandardResilienceHandler(...)` from
`Microsoft.Extensions.Http.Resilience` (Polly v8), driven entirely by `HttpResilienceOptions`:

```csharp
public static IHttpClientBuilder AddSdkResilience(
    this IHttpClientBuilder builder,
    Action<HttpResilienceOptions>? configure = null)
```

### Registration helpers

Prefer these over raw `AddHttpClient` — they bundle base address + resilience (and, for Refit, SDK JSON) into one call. All return `IHttpClientBuilder`, so
you can chain further (`.AddSdkResilience(...)` is already applied; add auth/header handlers after).

- `AddRefitApiClient<TApi>` (`RefitClientServiceCollectionExtensions`) — declarative Refit interface clients (**default for new clients**)
- `AddResilientClient<TClient>` (`TypedClientServiceCollectionExtensions`) — plain typed-client class (constructor-injected `HttpClient`, no Refit)
- `AddResilientClient(name, …)` (`TypedClientServiceCollectionExtensions`) — named client resolved via `IHttpClientFactory.CreateClient(name)`

```csharp
// Refit (default) — wires SDK JSON (JsonOptionsPresets.Default) + base address + resilience
builder.Services.AddRefitApiClient<IBillingApi>("https://billing.internal");

// Plain typed client — base address + resilience
builder.Services.AddResilientClient<WeatherClient>(new Uri("https://weather.example.com"));

// Named client
builder.Services.AddResilientClient("github", new Uri("https://api.github.com"));
```

Both `AddRefitApiClient<TApi>` and `AddResilientClient<TClient>` take optional `configureResilience` and `configureClient` delegates:

```csharp
builder.Services.AddRefitApiClient<IBillingApi>(
    "https://billing.internal",
    configureResilience: r => { r.MaxRetryAttempts = 5; r.TotalRequestTimeout = TimeSpan.FromSeconds(60); },
    configureClient: c => c.DefaultRequestHeaders.Add("X-Tenant", "acme"));
```

`AddRefitApiClient<TApi>` builds its `RefitSettings` from `CreateDefaultRefitSettings()` — `SystemTextJsonContentSerializer` over
`JsonOptionsPresets.Default`. Don't pass a hand-built `RefitSettings`; override JSON at the preset layer.

### Tuning — `HttpResilienceOptions`

Adjust via the `configureResilience` / `configure` delegate. Do **not** add a custom `DelegatingHandler` or Polly policy to change these behaviors.

| Option | Default | Meaning |
|---|---|---|
| `MaxRetryAttempts` | `3` | retries after the first try |
| `AttemptTimeout` | `10s` | per-attempt timeout (must be shorter than `TotalRequestTimeout`) |
| `TotalRequestTimeout` | `30s` | budget for the whole logical request incl. retries |
| `CircuitBreakerSamplingDuration` | `30s` | failure-rate window (must be ≥ 2× `AttemptTimeout`) |
| `CircuitBreakerFailureRatio` | `0.1` | trip threshold (10% failures in the window) |

OTel `HttpClient` instrumentation is wired by the observability package, so every call through the pipeline is traced automatically — no per-client tracing
setup.

### Cross-cutting handlers (beyond resilience)

These layer onto the same `IHttpClientBuilder`; chain after the registration helper. Each has its own options type — don't reinvent.

- OAuth2 client-credentials bearer token (cached) → `OAuth2ClientCredentialsHttpClientBuilderExtensions` · `OAuth2ClientCredentialsOptions`
- Mutual TLS (client cert) → `MutualTlsHttpClientBuilderExtensions` · `MutualTlsOptions`
- Request hedging (parallel attempts) → `HttpHedgingBuilderExtensions` · `HttpHedgingOptions`
- Inbound→outbound header propagation → `HeaderPropagationServiceCollectionExtensions` (`AddConventionalHeaderPropagation` + per-client `AddPropagatedHeaders`)

---

## Naming

| Pattern | When | Example |
|---|---|---|
| `{Provider}Client` | Single-provider HTTP wrapper | `TelegramClient`, `ClaudeClient` |
| `{Provider}{Domain}Client` | Multi-domain provider with separate clients | `GoogleMapsClient`, `GooglePlacesClient` |
| `{Provider}ApiClient` | Generic wrapper around a provider's REST API | `LocationApiClient` |
| `I{Provider}Api` | Refit interface (declarative client) | `IBillingApi`, `IGitHubApi` |

---

## Documentation

Per the starter table in [documentation/summary.md](../../lla/documentation/summary.md):

### Client class

- `/// <summary>` starts with **Connects** — a `Client` speaks the provider's model, so it *connects to* the provider's API
- a `Broker` (the app-side seam, speaking our model) starts with **Integrates** — see [component-names.md](components.md) § *`Client` vs `Broker` — whose model does it speak*
- `/// <remarks>` only when a caller needs a directive, a spec reference, or a non-obvious constraint ([remarks.md](../../lla/documentation/remarks.md) § *What it carries*)

```csharp
/// <summary>Connects to the Telegram Bot API for messages and topics.</summary>
/// <remarks>
/// Uses raw HTTP — no Telegram.Bot NuGet dependency.
/// Bot token and chat ID configured via TelegramSettings.
/// </remarks>
public sealed class TelegramClient(HttpClient http, IOptions<TelegramSettings> settings)
{
    public Task SendMessageAsync(...) { ... }
}
```

### Method docs

- `/// <summary>` one-liner — verb start (`Sends`, `Gets`, `Posts`, `Uploads`)

---

## Error handling

- HTTP errors bubble up — let the calling service handle / translate
- Don't catch `HttpRequestException` inside the client (loses context)
- Provider-specific error responses get deserialized to a typed model — return Result or throw a typed exception
- Don't catch-and-retry inside the client — retries/circuit-breaking are the resilience pipeline's job (`HttpResilienceOptions`), not the client's. Service
  naming + DI lifetime live in [services.md](service.md); outbound-HTTP quickstart in
  `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/http/Core/Core.md`
