# Host configuration

*Last updated: 2026-06-22*

> All host wiring — DI registration, configuration binding, middleware, startup — lives in the host's `Api/Configurations/` composition root, sourced only from the SDK or the host itself.
> Purpose — one place to read everything a service is wired with; no hidden, self-registering config buried in a layer, service, or model.
> Use case — reach for this whenever you add a setting, a service registration, or a startup step to a backend host.

## Configuration source

- configuration enters from exactly two places: the **SDK** (its public `Add*` / `Use*` extensions — `AddApiDefaults`, `AddDatabaseBespokeMigrations`, `AddDataSourceConnectionFactory`) or the **host itself** (`HostConfiguration` + its extensions).
- non-host projects — the application, domain, infrastructure, and persistence [layers](../layers/layers.md), plus models — **never** bind or register configuration: no `services.Configure<T>()`, no `AddOptions<T>()`, no `IConfiguration` reads, no self-registering `IServiceCollection` extension methods.
- a layer that needs a setting takes it as a **method parameter** the host passes in (`AddPersistence(this IServiceCollection services, IConfiguration configuration)`) — it does not reach into config on its own.
- this kills **hidden config methods** — a registration buried in an infra/persistence project that the host calls blind; every wire-up must be readable from the host's `Configure` chain alone.
- the SDK is the only allowed non-host source because its surface is a published, reviewed contract (see [startup-defaults.md](startup-defaults.md)); a product layer is not — if layers keep needing the same block, extract it to the SDK first.

## Location

- `{Service}/Api/Configurations/HostConfiguration.cs` — slim orchestrator
- `{Service}/Api/Configurations/HostConfiguration.Extensions.cs` — all extension methods

## Program.cs

**Fixed shape** — four statements and a test marker, identical in every service. It is not pristine in the sense of calling nothing; it calls the two `Configure` entry points, and everything else lives behind them.

```csharp
using {Brand}.{Service}.Configurations;

// Build and configure the host.
var builder = WebApplication.CreateBuilder(args);
builder.Configure();

// Build and configure the app.
var app = builder.Build();
app.Configure();

// Run.
app.Run();

public partial class Program;
```

- must carry exactly these **three comments**, one per statement group — the file is a fixed shape, so the comments never drift.
- must leave `public partial class Program;` undocumented — it exists so `WebApplicationFactory<Program>` resolves the host in integration tests, and an XML doc on it says nothing.
- must keep every **detail** out — DI registration, middleware order, migrations, seeding, warm-up, startup logs all live behind `builder.Configure()` / `app.Configure()`.
- must go **async all the way** when any startup work is async — `Configure(WebApplication)` becomes `ConfigureAsync`, and `Program.cs` awaits it. Never block with `.GetAwaiter().GetResult()` ([§ Async startup](#async-startup)).
- must not grow a fourth statement. A new startup concern is a new call inside `Configure`, never a new line here.

## HostConfiguration

Static class with two `Configure` overloads — one for `WebApplicationBuilder`, one for `WebApplication`. No DI logic inline — just chains extension methods in order.

```csharp
/// <summary>Extends the host builder and the web application for startup wiring.</summary>
public static partial class HostConfiguration
{
    /// <summary>Configures the application builder (services).</summary>
    /// <param name="builder">The web application builder to configure.</param>
    /// <returns>The same <paramref name="builder"/> for chaining.</returns>
    public static WebApplicationBuilder Configure(this WebApplicationBuilder builder)
    {
        builder.AddApiDefaults(o => o.ServiceName = "{service}");   // SDK boot floor first

        builder
            .AddSettings()
            .AddPersistence()
            .AddApplicationServices();   // product seams — no trailing comments; method names self-document

        return builder;
    }

    /// <summary>Runs startup tasks, then configures middleware and endpoints.</summary>
    /// <param name="app">The built web application to configure.</param>
    /// <returns>The same <paramref name="app"/> for chaining.</returns>
    public static WebApplication Configure(this WebApplication app) { ... }
}
```

- the class summary and the two `Configure` summaries above are **locked** — identical across every app, don't reword per app.

## HostConfigurationExtensions

Static class with extension methods on `WebApplicationBuilder`. Each method registers a logical group of services. Methods are called in order by `HostConfiguration.Configure()`.

| Method | Purpose |
|---|---|
| `AddEnvironmentOverrides()` | Maps env vars to config keys (overrides appsettings) |
| `AddSettings()` | Binds `IOptions<T>` for all settings classes + DB setup |
| `AddIntegrations()` | Registers typed `HttpClient`s for external APIs |
| `AddApplicationServices()` | Registers application-layer services (interfaces → implementations) |
| `AddPipelines()` | Registers pipeline nodes, orchestrators, registry, executor, schedulers |
| `AddSchedulers()` | Registers `IHostedService` background schedulers |
| `AddObservers()` | Registers pipeline event observers (e.g. SignalR notifier) |
| `AddMediator()` | Registers mediator + scans assembly for query/command handlers |
| `AddControllers()` | Configures MVC controllers + JSON serialization |
| `AddSignalR()` | Adds SignalR hub services |
| `AddCors()` | Configures CORS from settings |

## Async startup [REQUIRED]

**Never block on async work.** `.GetAwaiter().GetResult()`, `.Result`, and `.Wait()` are banned in host configuration and everywhere else.

- must make the chain async instead — an async startup task makes `Configure(WebApplication)` into `ConfigureAsync`, and `Program.cs` awaits it. That is one `await`, and the problem is gone.
- top-level statements have been async since C# 7.1, so the entry point costs nothing to convert.

```csharp
// Build and configure the app.
var app = builder.Build();
await app.ConfigureAsync();
```

**Why it is banned even where it looks safe.** ASP.NET Core has no `SynchronizationContext`, so the classic deadlock does not fire, and startup runs before the server accepts traffic, so thread-pool starvation has nothing to starve. The ban is not about those:

- the idiom **spreads** — it reads as sanctioned, and the copy that lands in a request path is where the deadlock and the starvation are real.
- it **hides the shape** — a method that is async is async; making its caller pretend otherwise costs a reader the fact.
- the alternative is **one keyword**. A rule that costs `await` and buys a whole failure class never being introduced is not a trade.

## Domain registration

Layers (`Application`, `Infrastructure`, `Persistence`) ship **no** `DependencyInjection.cs` and **no** `Add*(this IServiceCollection)` — the host owns the registrations, and it groups them by domain rather than by layer.

**One registration method per domain.** Not per layer — a domain owns its whole vertical: its services, its settings, its EF configuration, its options. `Persistence` gets one method because storage *is* a domain, the same way `Identity` is; it splits only once it grows sub-domains of its own.

```csharp
builder
    .AddSettings()
    .AddPersistence()
    .AddCodeServices()
    .AddApplicationServices()
    .AddIdentity()
    .AddAuth()
    .AddBilling()
    .AddControllers();
```

- must name the method for the **domain** — `AddBilling()`, `AddIdentity()`, never `AddApplicationLayer()`.
- must register a domain's every concern in its own method — splitting its services from its settings puts one subject in two places.
- must keep the chain in dependency order, settings first, delivery surface last.
- may split a domain into several methods once it carries sub-domains; until then one method is the honest shape.

Two consequences to handle when collapsing a layer's registrations into the host: Two consequences to handle when collapsing a layer into the host:

- **Assembly scans** (mediator handlers, FluentValidation validators) anchor on a **public marker type in the scanned layer** — `typeof(IApplicationMarker).Assembly` — never the parameterless overload: called from the host, `Assembly.GetCallingAssembly()` resolves to the *host* assembly, not the layer (see [mediator](../domains/messaging/mediator.md)). Add one empty `public interface I{Layer}Marker;` to each scanned layer.
- **Internal adapters** (EF stores, typed clients) stay `internal` — the host registers them by concrete type, so grant it visibility with `<InternalsVisibleTo Include="{Host}" />` in the layer's `.csproj`. Don't widen them to `public` just to wire them.

Startup tasks (DB init, seeding, warm-up) move host-side too — into `Configure(WebApplication)` or an extension it calls, never into `Program.cs` ([§ Program.cs](#programcs) — the entry point holds four statements and never grows a fifth). An async task makes the whole chain async ([§ Async startup](#async-startup)).

## Documentation

- the class + the two `Configure` overloads use the **locked** summaries shown above (don't reword per app).
- each private `Add*` extension gets a one-liner `<summary>` starting with **"Registers"** (or "Configures"). No `<remarks>` on host wiring.
- the `Configure` chain carries **no trailing per-method comments** — the method names self-document. Inline comments only where a step's *why* isn't obvious (imperative one-liner, per [documentation](../../lla/notation/documentation/documentation.md)).

## Rules

- **service-registration `Add*` extensions live only in `Configurations/`** — never in a layer (persistence, infrastructure, codes, …). The host calls the SDK's `Add*` directly and inlines the product glue; a layer never ships its own `AddXyz(this IServiceCollection)`. (A multi-host app duplicates the few glue lines per host — that is the accepted cost of host-owned wiring.)
- all configuration is wired **only** in the host, sourced from the SDK or the host itself — never a layer/service/model (see Configuration source).
- `Program.cs` holds a **fixed four-statement shape** with its three comments ([§ Program.cs](#programcs)). Every detail — DI, middleware, migrations, logs — lives behind `builder.Configure()` / `app.Configure()`.
- `HostConfiguration.Configure()` chains extension methods — no inline DI logic
- Each extension method in `HostConfigurationExtensions` groups related registrations
- Return `WebApplicationBuilder` for chaining

## Built-in `builder` extensions

> Composition-phase surface that ships in the `Microsoft.AspNetCore.App` shared framework — reachable with **no `PackageReference`**. Verified against .NET 10 (`10.0.8`).

- check here **before** adding a package or hand-rolling host glue — the framework already covers most wiring.
- grouped by the property the method hangs off; alphabetical inside each group.
- out of scope because they need their own package: `AddOpenApi()` / `MapOpenApi()`, EF Core, Swashbuckle, Serilog.

### `builder.Services`

| Method | Purpose |
|---|---|
| `Add()` | Appends a prebuilt `ServiceDescriptor` to the collection |
| `AddAntiforgery()` | Antiforgery token generation and validation |
| `AddAuthentication()` | Authentication services and the scheme registry |
| `AddAuthenticationCore()` | Scheme handling only, without the hosting defaults |
| `AddAuthorization()` | Policy registry plus the ASP.NET Core evaluator |
| `AddAuthorizationBuilder()` | Fluent builder for declaring named policies |
| `AddAuthorizationCore()` | Policy services without the HTTP-side evaluator |
| `AddAuthorizationPolicyEvaluator()` | Evaluator that runs policies against an endpoint |
| `AddCascadingAuthenticationState()` | Flows auth state to Blazor as a cascading value |
| `AddCascadingValue()` | Root-level cascading value for Blazor components |
| `AddCertificateForwarding()` | Rebuilds a client cert from a proxy-set header |
| `AddConnections()` | Low-level connection handling behind SignalR transports |
| `AddControllers()` | MVC controllers, no views or pages |
| `AddControllersWithViews()` | MVC controllers plus Razor view rendering |
| `AddCookiePolicy()` | Consent tracking and cookie-attribute policy |
| `AddCors()` | CORS services and the named-policy registry |
| `AddDataProtection()` | Key ring encrypting cookies, tokens, and payloads |
| `AddDirectoryBrowser()` | Services backing `UseDirectoryBrowser()` |
| `AddDistributedMemoryCache()` | `IDistributedCache` over process memory — single node |
| `AddEndpointsApiExplorer()` | API metadata for minimal-API endpoints |
| `AddExceptionHandler<T>()` | An `IExceptionHandler` for `UseExceptionHandler()` |
| `AddHealthChecks()` | Health-check service plus a per-probe builder |
| `AddHostFiltering()` | Allow-list of `Host` header values the server answers |
| `AddHostedService<T>()` | Background service run for the host's lifetime |
| `AddHsts()` | Options for the `Strict-Transport-Security` header |
| `AddHttpClient()` | `IHttpClientFactory` plus named and typed clients |
| `AddHttpContextAccessor()` | Ambient `IHttpContextAccessor` for non-request code |
| `AddHttpLogging()` | Selects which request/response fields get logged |
| `AddHttpLoggingInterceptor<T>()` | Per-request hook tuning what HTTP logging records |
| `AddHttpsRedirection()` | Target port and status code for HTTPS redirects |
| `AddIdentity<TUser,TRole>()` | Full Identity stack with cookies and roles |
| `AddIdentityApiEndpoints<TUser>()` | Identity services shaped for `MapIdentityApi()` |
| `AddIdentityCore<TUser>()` | User management only — no cookies, no sign-in manager |
| `AddKeyedScoped()` | Scoped registration resolved by a service key |
| `AddKeyedSingleton()` | Singleton registration resolved by a service key |
| `AddKeyedTransient()` | Transient registration resolved by a service key |
| `AddLocalization()` | `IStringLocalizer` and resource-file lookup |
| `AddLogging()` | Logging factory and provider registration |
| `AddMemoryCache()` | In-process `IMemoryCache` |
| `AddMetrics()` | `IMeterFactory` and the metrics pipeline |
| `AddMvc()` | Full MVC — controllers, views, Razor Pages |
| `AddMvcCore()` | MVC primitives only, no formatters or views |
| `AddOptions()` | Options infrastructure behind `IOptions<T>` |
| `AddOptionsWithValidateOnStart<T>()` | Binds options and fails at startup, not first resolve |
| `AddOutputCache()` | Server-side response cache with tag-based eviction |
| `AddProblemDetails()` | RFC 9457 error-body writer used by the framework |
| `AddRateLimiter()` | Rate-limit policies consumed by `UseRateLimiter()` |
| `AddRazorComponents()` | Blazor server-side rendering services |
| `AddRazorPages()` | Razor Pages routing and page-model services |
| `AddRequestDecompression()` | Decompresses request bodies by `Content-Encoding` |
| `AddRequestLocalization()` | Culture selection for `UseRequestLocalization()` |
| `AddRequestTimeouts()` | Named and default per-request timeout policies |
| `AddResponseCaching()` | Legacy `Cache-Control`-driven response cache |
| `AddResponseCompression()` | Brotli and gzip response-compression providers |
| `AddRouting()` | Endpoint routing, matching, and URL generation |
| `AddRoutingCore()` | Routing without the default constraint set |
| `AddScoped()` | One instance per request scope |
| `AddServerSideBlazor()` | Blazor Server circuits over SignalR |
| `AddSession()` | Session state over the distributed cache |
| `AddSignalR()` | SignalR hubs, protocols, and dispatcher |
| `AddSignalRCore()` | SignalR without the default JSON protocol |
| `AddSingleton()` | One instance for the application lifetime |
| `AddSupplyValueFromFormProvider()` | Binds form values to `[SupplyParameterFromForm]` |
| `AddSupplyValueFromPersistentComponentStateProvider()` | Restores persisted Blazor component state |
| `AddSupplyValueFromQueryProvider()` | Binds query-string values to Blazor parameters |
| `AddTransient()` | A new instance on every resolve |
| `AddValidation()` | Minimal-API DataAnnotations validation — new in .NET 10 |
| `AddW3CLogging()` | W3C-format access log written to disk |
| `AddWebEncoders()` | HTML, JavaScript, and URL encoders |
| `AddWebSockets()` | WebSocket keep-alive and allowed-origin options |
| `Configure<T>()` | Binds an options class from a delegate or config section |
| `ConfigureAll<T>()` | Applies one delegate to every named options instance |
| `ConfigureApplicationCookie()` | Tunes the Identity application cookie |
| `ConfigureExternalCookie()` | Tunes the Identity external-login cookie |
| `ConfigureHttpClientDefaults()` | Defaults applied to every factory-created client |
| `ConfigureHttpJsonOptions()` | JSON options for minimal APIs and `Results.Json` |
| `ConfigureOptions<T>()` | Registers a type that configures options |

### `builder.Configuration`

| Method | Purpose |
|---|---|
| `Add()` | Appends a prebuilt `IConfigurationSource` |
| `AddCommandLine()` | Reads `--key=value` args, with optional switch mappings |
| `AddConfiguration()` | Chains another `IConfiguration` in as a source |
| `AddEnvironmentVariables()` | Reads env vars, optionally filtered by prefix |
| `AddInMemoryCollection()` | In-memory key/value pairs — tests and defaults |
| `AddIniFile()` | INI file source, optional and reload-on-change |
| `AddIniStream()` | INI source read from an open stream |
| `AddJsonFile()` | JSON file source, optional and reload-on-change |
| `AddJsonStream()` | JSON source read from an open stream |
| `AddKeyPerFile()` | Directory of files, filename = key — Docker secrets |
| `AddUserSecrets()` | Development-only secret store kept outside the repo |
| `AddXmlFile()` | XML file source, optional and reload-on-change |
| `AddXmlStream()` | XML source read from an open stream |

### `builder.Logging`

| Method | Purpose |
|---|---|
| `AddConfiguration()` | Binds levels and filters from a configuration section |
| `AddConsole()` | Console provider using the default formatter |
| `AddConsoleFormatter<F,O>()` | Registers a custom console output formatter |
| `AddDebug()` | Writes through `Debug.WriteLine` |
| `AddEventLog()` | Windows Event Log provider — Windows only |
| `AddEventSourceLogger()` | EventSource provider consumed by `dotnet-trace` |
| `AddFilter()` | Minimum level for a category or a provider |
| `AddJsonConsole()` | Console output as structured JSON lines |
| `AddProvider()` | Registers an arbitrary `ILoggerProvider` |
| `AddSimpleConsole()` | Single-line console formatter, colour optional |
| `AddSystemdConsole()` | Console formatter with systemd severity prefixes |
| `AddTraceSource()` | Routes logs to `System.Diagnostics` trace listeners |
| `Configure()` | Sets `LoggerFactoryOptions` — activity tracking |

### `builder.Metrics`

| Method | Purpose |
|---|---|
| `AddConfiguration()` | Binds meter enable/disable rules from configuration |
| `AddDebugConsole()` | Writes metric values to the console — debugging only |
| `AddListener()` | Registers an `IMetricsListener` sink |
| `ClearListeners()` | Removes every listener registered so far |
| `DisableMetrics()` | Disables a meter or instrument by name |
| `EnableMetrics()` | Enables a meter or instrument by name |

### `builder.Host`

- legacy generic-host shim — prefer `builder.Services` / `builder.Configuration` / `builder.Logging`.
- `WebApplicationBuilder` has already fixed some of these decisions, so a few are blocked outright.

| Method | Purpose |
|---|---|
| `ConfigureAppConfiguration()` | Adds config sources — prefer `builder.Configuration` |
| `ConfigureContainer<T>()` | Configures a third-party DI container builder |
| `ConfigureDefaults()` | Applies generic-host defaults — already applied |
| `ConfigureHostConfiguration()` | Sources read before app configuration binds |
| `ConfigureHostOptions()` | Shutdown timeout, background-service error policy |
| `ConfigureLogging()` | Adds log providers — prefer `builder.Logging` |
| `ConfigureMetrics()` | Configures metrics — prefer `builder.Metrics` |
| `ConfigureServices()` | Registers services — prefer `builder.Services` |
| `ConfigureSlimWebHost()` | Trimmed web-host wiring used by slim builders |
| `ConfigureWebHost()` | Blocked — analyzer error `ASP0008` |
| `ConfigureWebHostDefaults()` | Blocked — throws `NotSupportedException` |
| `RunConsoleAsync()` | Builds and runs the host — terminal, not wiring |
| `UseConsoleLifetime()` | Ctrl+C and SIGTERM shutdown handling |
| `UseContentRoot()` | Sets the content root path |
| `UseDefaultServiceProvider()` | Toggles scope and build-time DI validation |
| `UseEnvironment()` | Blocked — throws `NotSupportedException` |
| `UseServiceProviderFactory<T>()` | Swaps in a third-party DI container |

### `builder.WebHost`

| Method | Purpose |
|---|---|
| `CaptureStartupErrors()` | Shows an error page instead of failing to start |
| `Configure()` | Blocked — analyzer error `ASP0009` |
| `ConfigureAppConfiguration()` | Adds config sources — prefer `builder.Configuration` |
| `ConfigureKestrel()` | Limits, endpoints, and HTTP protocols for Kestrel |
| `ConfigureLogging()` | Adds log providers — prefer `builder.Logging` |
| `ConfigureServices()` | Registers services — prefer `builder.Services` |
| `PreferHostingUrls()` | Host URLs win over server-configured addresses |
| `SuppressStatusMessages()` | Silences the "Now listening on…" startup lines |
| `UseConfiguration()` | Seeds web-host settings from an `IConfiguration` |
| `UseContentRoot()` | Sets the content root path |
| `UseDefaultServiceProvider()` | Toggles scope and build-time DI validation |
| `UseEnvironment()` | Sets the environment name |
| `UseHttpSys()` | HTTP.sys server instead of Kestrel — Windows only |
| `UseIIS()` | In-process IIS hosting — Windows only |
| `UseIISIntegration()` | Out-of-process IIS reverse-proxy hosting |
| `UseKestrel()` | Kestrel with the full default feature set |
| `UseKestrelCore()` | Kestrel stripped to its core, for trimmed apps |
| `UseKestrelHttpsConfiguration()` | Re-adds HTTPS support on top of `UseKestrelCore()` |
| `UseNamedPipes()` | Named-pipe transport for Kestrel — Windows only |
| `UseQuic()` | QUIC transport backing HTTP/3 |
| `UseServer()` | Plugs in a custom `IServer` implementation |
| `UseSetting()` | Sets one raw web-host setting by key |
| `UseShutdownTimeout()` | Grace period for shutdown before abort |
| `UseSockets()` | Default socket transport for Kestrel |
| `UseStartup<T>()` | Blocked — analyzer error `ASP0010` |
| `UseStaticWebAssets()` | Serves static assets contributed by referenced packages |
| `UseUrls()` | Addresses the server binds to |
| `UseWebRoot()` | Blocked — throws `NotSupportedException` |

## Built-in `app` extensions

> Every `IApplicationBuilder` / `WebApplication` `Use*` and `Map*` method in the shared framework — no `PackageReference`.

- `Order` is the pipeline slot: **lower runs first**, equal numbers are interchangeable.
- `any` — position carries no constraint, it runs where you place it. `end` — after routing and authorization.
- `WebApplication` inserts `UseRouting()` and `UseEndpoints()` for you; call them explicitly only to place middleware between them.

| Method | Order | Purpose |
|---|---|---|
| `UseForwardedHeaders()` | 1 | Applies proxy headers before anything reads scheme or IP |
| `UseCertificateForwarding()` | 1 | Rebuilds the client cert from a proxy header |
| `UseHostFiltering()` | 1 | Rejects requests whose `Host` header is not allow-listed |
| `UsePathBase()` | 1 | Strips a path prefix so routing sees app-relative paths |
| `UseExceptionHandler()` | 2 | Catches downstream exceptions, re-executes an error path |
| `UseDeveloperExceptionPage()` | 2 | Renders the exception and stack trace — development only |
| `UseStatusCodePages()` | 3 | Adds a body to bare error status codes |
| `UseStatusCodePagesWithRedirects()` | 3 | Redirects the client to an error page |
| `UseStatusCodePagesWithReExecute()` | 3 | Re-runs the pipeline on an error path, keeping the status |
| `UseHsts()` | 4 | Emits `Strict-Transport-Security` — production only |
| `UseHttpsRedirection()` | 5 | Redirects HTTP requests to the HTTPS endpoint |
| `UseHttpLogging()` | 6 | Logs configured request and response fields |
| `UseW3CLogging()` | 6 | Writes a W3C-format access log to disk |
| `UseResponseCompression()` | 7 | Compresses responses; must precede anything writing a body |
| `UseRequestDecompression()` | 7 | Decompresses bodies before anything reads them |
| `UseHttpMethodOverride()` | 8 | Rewrites the verb from `X-Http-Method-Override` |
| `UseRewriter()` | 8 | Applies URL rewrite and redirect rules before routing |
| `UseRequestLocalization()` | 9 | Sets request culture before culture-sensitive middleware |
| `UseDefaultFiles()` | 10 | Rewrites directory requests to `index.html` |
| `UseStaticFiles()` | 11 | Serves files from the web root, short-circuiting the rest |
| `UseDirectoryBrowser()` | 12 | Renders a browsable directory listing |
| `UseFileServer()` | 12 | Combines default files, static files, and browsing |
| `UseCookiePolicy()` | 13 | Enforces consent and cookie attributes before auth |
| `UseWebSockets()` | 14 | Accepts WebSocket upgrade requests |
| `UseRouting()` | 15 | Matches the endpoint; everything below reads its metadata |
| `UseCors()` | 16 | Applies a CORS policy after routing, before auth |
| `UseRateLimiter()` | 17 | Enforces rate-limit policies from endpoint metadata |
| `UseRequestTimeouts()` | 17 | Applies per-request timeout policies from metadata |
| `UseAuthentication()` | 18 | Resolves the caller identity onto `HttpContext.User` |
| `UseAuthorization()` | 19 | Enforces endpoint policies; requires authentication first |
| `UseSession()` | 20 | Loads and saves session state around the request |
| `UseAntiforgery()` | 21 | Validates antiforgery tokens on unsafe verbs |
| `UseOutputCache()` | 22 | Serves and stores cached responses by policy |
| `UseResponseCaching()` | 22 | Legacy `Cache-Control`-driven response cache |
| `UseEndpoints()` | 23 | Executes the matched endpoint — implicit on `WebApplication` |
| `Use()` | any | Inline middleware delegate at this position |
| `UseMiddleware<T>()` | any | Class-based middleware at this position |
| `UseWhen()` | any | Branches on a predicate, then rejoins the pipeline |
| `MapWhen()` | any | Branches on a predicate and never rejoins |
| `Map()` | any | Branches by path prefix and never rejoins |
| `Run()` | any | Terminal delegate — nothing after it runs |
| `UseHealthChecks()` | any | Terminal health endpoint; prefer `MapHealthChecks()` |
| `UseWelcomePage()` | any | Terminal placeholder page — development only |
| `UseMvc()` | legacy | Pre-endpoint-routing MVC; use `MapControllers()` |
| `UseMvcWithDefaultRoute()` | legacy | Legacy MVC wired to the default route |
| `UseRouter()` | legacy | Legacy `IRouter` routing; superseded by `UseRouting()` |
| `Map()` | end | Maps a route pattern to a handler for any verb |
| `MapGet()` | end | Maps a `GET` route to a handler |
| `MapPost()` | end | Maps a `POST` route to a handler |
| `MapPut()` | end | Maps a `PUT` route to a handler |
| `MapDelete()` | end | Maps a `DELETE` route to a handler |
| `MapPatch()` | end | Maps a `PATCH` route to a handler |
| `MapMethods()` | end | Maps a route for an explicit set of verbs |
| `MapGroup()` | end | Route group sharing a prefix, filters, and metadata |
| `MapControllers()` | end | Maps attribute-routed controller actions |
| `MapControllerRoute()` | end | Maps a named conventional controller route |
| `MapDefaultControllerRoute()` | end | Maps `{controller=Home}/{action=Index}/{id?}` |
| `MapAreaControllerRoute()` | end | Maps a conventional route scoped to an MVC area |
| `MapDynamicControllerRoute<T>()` | end | Route whose controller is chosen at request time |
| `MapRazorPages()` | end | Maps discovered Razor Pages |
| `MapDynamicPageRoute<T>()` | end | Razor Page route resolved at request time |
| `MapRazorComponents<T>()` | end | Maps Blazor component endpoints and render modes |
| `MapBlazorHub()` | end | SignalR hub backing Blazor Server circuits |
| `MapHub<T>()` | end | Maps a SignalR hub to a path |
| `MapConnectionHandler<T>()` | end | Maps a persistent-connection handler to a path |
| `MapConnections()` | end | Maps the low-level connection endpoint |
| `MapHealthChecks()` | end | Health probe as a routable endpoint |
| `MapIdentityApi<TUser>()` | end | Register, login, and token endpoints for Identity |
| `MapStaticAssets()` | end | Fingerprinted, precompressed static assets |
| `MapShortCircuit()` | end | Returns a status immediately for matching prefixes |
| `MapFallback()` | end | Catch-all endpoint — register last |
| `MapFallbackToFile()` | end | Serves an SPA entry file for unmatched routes |
| `MapFallbackToController()` | end | Falls back to a controller action |
| `MapFallbackToPage()` | end | Falls back to a Razor Page |
| `MapFallbackToAreaController()` | end | Falls back to a controller action in an area |
| `MapFallbackToAreaPage()` | end | Falls back to a Razor Page in an area |

## Documentation

- must leave `Program.cs` undocumented — its four statements are the shape.
