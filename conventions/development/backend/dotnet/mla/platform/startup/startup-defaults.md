# Startup defaults

*Last updated: 2026-06-13*

> The boot floor every API host starts from — what `AddApiDefaults()` and `UseApiDefaults()` fold in.
> Purpose — a new service inherits the whole pipeline instead of re-listing it and missing one.
> Use case — creating a host, or turning one folded-in concern off.

A production-shaped API host boots through the paired SDK calls `AddApiDefaults()` / `UseApiDefaults()`
— never a hand-rolled per-area `Add*` / `Use*` set.

## The two calls

The boot floor is two lines. Everything between them is per-app (auth, mediator, data).

```csharp
using WoW.Two.Sdk.Backend.Beta;

var builder = WebApplication.CreateBuilder(args);
builder.AddApiDefaults();

// auth + mediator + data go HERE — explicit, after AddApiDefaults, before Build()

var app = builder.Build();
app.UseApiDefaults();

// auth middleware + your endpoints go HERE — after UseApiDefaults

app.Run();
```

- `AddApiDefaults(this WebApplicationBuilder, Action<ApiDefaultsOptions>? configure = null)` — registers
  the P1 service baseline; returns the builder for chaining.
- `UseApiDefaults(this WebApplication)` — adds the matching middleware pipeline, maps the OpenAPI + health
  endpoints, returns the app.
- both live in `src/Meta/ApiDefaultsExtensions.cs`; root namespace `WoW.Two.Sdk.Backend.Beta`, so one
  `using` lights it up.
- pristine `Program.cs` still applies ([host configuration](host-configuration.md)).
- a product wrapping these in `HostConfiguration` calls `AddApiDefaults` / `UseApiDefaults` from the two
  `Configure` extensions, and nothing per-area.

---

## Folded in

`AddApiDefaults` composes these (each its own per-area extension — never call one yourself):

| Concern | Add-side symbol | Use-side symbol |
|---|---|---|
| Logging | `UseSerilogConventional` (on `builder.Host`) | — |
| Time | `AddTimeProviders` | — |
| Tracing | `AddOpenTelemetryTracing` | — |
| Metrics | `AddOpenTelemetryMetrics` | — |
| OTLP export | `AddOtlpExporters` | — |
| Health | `AddHealthChecksBuilder` | `MapHealthChecks(options.HealthEndpointPath)` |
| Proxy-aware hosting | `AddProxyAwareHosting` | `UseProxyAwareHosting` |
| Secure headers | — | `UseOwaspSecureHeaders` |
| OpenAPI | `AddOpenApiDefaults` | `MapOpenApiEndpoint` |
| ProblemDetails | `AddTraceAwareProblemDetails` | — |
| Exception handling | `AddAppExceptionHandling` | — |
| Rate limit | `AddPerIpSlidingWindowRateLimit` | `UseRateLimiter` |
| Output cache | `AddDefaultOutputCache` | `UseOutputCache` |
| Compression | `AddBrotliGzipCompression` | `UseResponseCompression` |
| CORS | `AddDefaultCorsPolicy` (origins given) | `UseCors` (origins given) |
| Validators | `AddFluentValidatorsFromAssemblies` (assemblies given) | — |

---

## Tuning — flip flags, don't re-compose

Tune via `ApiDefaultsOptions` (`src/Meta/ApiDefaultsOptions.cs`). Every concern defaults **on** — flip a
flag off rather than drop `AddApiDefaults` and re-list the per-area extensions by hand.

```csharp
builder.AddApiDefaults(o =>
{
    o.ServiceName = "smart-qr";                            // OTel service name (default: app name)
    o.ValidatorAssemblies.Add(typeof(Program).Assembly);   // empty ⇒ validators skipped
    o.CorsOrigins.Add("https://app.example.com");          // empty ⇒ CORS not registered
    o.EnableRateLimiting = false;                          // off-flag, not a removed call
    o.ExposeOpenApi = false;                               // hide the OpenAPI endpoint in prod
});
```

| `ApiDefaultsOptions` member | Type | Default | Effect when changed |
|---|---|---|---|
| `ServiceName` | `string?` | host app name | OTel resource service name |
| `ValidatorAssemblies` | `IList<Assembly>` | empty | non-empty ⇒ `AddFluentValidatorsFromAssemblies` runs |
| `CorsOrigins` | `IList<string>` | empty | non-empty ⇒ `AddDefaultCorsPolicy` + `UseCors` |
| `EnableOtlpExporters` | `bool` | `true` | gates `AddOtlpExporters` |
| `EnableRateLimiting` | `bool` | `true` | gates `AddPerIpSlidingWindowRateLimit` + `UseRateLimiter` |
| `EnableOutputCache` | `bool` | `true` | gates `AddDefaultOutputCache` + `UseOutputCache` |
| `EnableResponseCompression` | `bool` | `true` | gates `AddBrotliGzipCompression` + `UseResponseCompression` |
| `ExposeOpenApi` | `bool` | `true` | gates `MapOpenApiEndpoint` |
| `HealthEndpointPath` | `string` | `/health` | path passed to `MapHealthChecks` |

---

## Explicit additions

Auth, mediator, and data are **deliberately excluded** — they need per-app keys, assemblies, and connection strings.

- must register auth / mediator / data between `AddApiDefaults` and `Build()`.
- must add auth middleware and map endpoints **after** `UseApiDefaults`, so the forwarded-headers /
  secure-headers / CORS pipeline is already in place.

---

## Rules

- must boot a production-shaped API host with `AddApiDefaults` + `UseApiDefaults`.
- must not hand-assemble an `Add*` / `Use*` list instead.
- must change behavior through `ApiDefaultsOptions` flags only.
- must not bypass the bundle to call a folded-in per-area extension directly.
- must keep auth + mediator + data out of the bundle, added explicitly — mediator / data before
  `Build()`, auth middleware after `UseApiDefaults`.
- must raise a need for finer control than the flags expose — extend `ApiDefaultsOptions`, never fork
  the wiring per product.

---

## Neighbours

- [host configuration](host-configuration.md) — pristine `Program.cs` + the `HostConfiguration` split
  wrapping these calls
- [clean architecture](../../architecture/clean/clean.md) — the layer set
- `src/Meta/Meta.md` (in `wow-two-sdk.backend.beta`) — boot-floor quickstart + per-area composition
  escape hatch
