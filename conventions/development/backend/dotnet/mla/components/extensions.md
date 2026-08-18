# Extensions

*Last updated: 2026-08-18*

> The static-logic tier over a domain's types.
> Purpose — keep dependency-free behaviour off the type it extends, without inventing a service for it.
> Use case — reach here for encoding, projection or registration logic that needs no collaborators.

## Location

### Folder
- must sit in an `Extensions/` folder beside the domain it extends.

### File
- must give each extensions class its own file, named for the type.

---

## Declaration

### Type doc

#### [Summary](../../lla/notation/documentation/summary.md)
- must start with **Extends**, then `<see cref>` the target, then `for {purpose}`.
- must name the purpose category, never the methods it holds.

```csharp
// ✅
/// <summary>Extends <see cref="WifiContentValueObject"/> for payload encoding.</summary>
// ❌ names the additions, which change with every method
/// <summary>Extends <see cref="WifiContentValueObject"/> with Encode and Parse.</summary>
```

### Construct
- must declare a `public static class`.

### Type name
- must be named `{Domain}Extensions`, after the domain the logic belongs to.
- must not name a type the domain does not answer to — an enum or an interface locks the class to one declaration.
- must name the target type only when the target **is** the domain — `ServiceCollectionExtensions`.
- must not carry an interface's `I` into the class name — the `I` belongs to the interface, and a class is not one.
- must narrow to `{Area}ServiceCollectionExtensions` for DI registration in a library
  ([naming](../../lla/notation/naming/naming.md) § *Registration and extension-method naming*).
- may name a **closed** family rather than one member.
  - a union's fixed variant list, never an open bag of related types.

```csharp
// ✅ the domain, and the closed family it covers
public static class WifiContentExtensions
// ❌ one target, so the first sibling method forces a rename
public static class WifiSsidEncodingExtensions
```

---

## Content

### Member docs

#### [Summary](../../lla/notation/documentation/summary.md)
- must start the `<summary>` with the method's own verb — `Adds`, `Maps`, `Encodes`.
- must carry a `<param>` for every parameter, the receiver included.
- must carry `<returns>` unless the method returns `void`, `Task` or `ValueTask`.
- must carry `<remarks>` only for a directive, a spec reference, or a constraint the signature hides.

```csharp
// ✅
/// <summary>Encodes the content as a WIFI URI payload.</summary>
/// <param name="content">The content to encode.</param>
/// <returns>The payload string.</returns>

// ❌ a parameter set that is complete or the doc is wrong
/// <summary>Encodes the content as a WIFI URI payload.</summary>
```

### Members
- must take the receiver as a `this` parameter or as a plain argument.
- must be reachable by its type name at the call site.
- may be `async` when the receiver's own work is asynchronous, returning `Task<T>` or `ValueTask<T>`.
- may use `=>` for a member that returns or delegates — extensions take no collaborators to accumulate
  ([style](../../lla/notation/style/style.md) § *The body*).
- must avoid a `Result` where it can — a `bool` from `TryX`, or an early return, says the same thing cheaper.
- must return a `Result` when neither fits, rather than throwing.
- may throw only from a method whose name says so — `XOrThrow`, `DoXAndThrow`.
- must produce its result from the receiver and its arguments alone — joining two collaborators makes it a `Service`.
- must declare a constant here while this class is its only caller — a second caller moves it to `Constants`.
- must order constants first, then methods.

```csharp
// ✅ the receiver and its own constant, nothing reached for
private const string PayloadShape = "WIFI:T:{0};S:{1};P:{2};;";

public static string ToPayload(this WifiContentValueObject content) =>
    string.Format(PayloadShape, content.Encryption, content.Ssid, content.Password);

// ❌ bridges two collaborators, so it is a Service
public static string ToPayload(this WifiContentValueObject content, IFormatBroker broker, IStyleClient client) =>
    broker.Render(content, client.GetTheme());
```


A family class owns the family's format constants too, keeping wire spellings out of the model.

---

## Registration naming

For a library that ships `IServiceCollection` / host extensions (the SDK pattern).
§ *No brand / product prefix* applies in full — the *package* carries the brand, the *method* the meaning.

- **extension class** — on `IServiceCollection`, name `<Area>ServiceCollectionExtensions` (Microsoft's pattern)
  - on any other type, `<Target>Extensions` or `<Area><Target>Extensions` — `TimeProviderExtensions`,
    `LoggingBuilderExtensions`, `EndpointConventionBuilderExtensions`
- **registration methods carry NO brand prefix** — describe what the call registers, not who built the wrapper
  - `AddJwtBearerAuthentication` not `AddWowTwoJwt` · `AddOpenTelemetryTracing` not `AddWowTwoTracing`
- **acid test** — if you'd want to add `// these are wow-two's defaults`, the name is wrong
  - bake the meaning in, so a reader who never heard of wow-two knows what it does

- `Add<Concrete>` — `AddJwtBearerAuthentication`, `AddOpenTelemetryTracing` · scheme / system-specific registration
- `Add<Default><Thing>` — `AddDefaultCorsPolicy`, `AddDefaultOutputCache` · pre-set policy / configuration
- `Add<Specific><Thing>` — `AddPerIpSlidingWindowRateLimit`, `AddBrotliGzipCompression` · picks one strategy of many
- `Use<Concrete>` — `UseOwaspSecureHeaders`, `UseSerilogConventional` · pipeline middleware
- `Map<Endpoint>` — `MapOpenApiEndpoint` · endpoint routing
- `Add<Lib>FromAssemblies` — `AddFluentValidatorsFromAssemblies` · assembly-scanning registration

- **stable consumer-visible identifiers stay brand-free** — cookie names (`.app.auth`), policy names (`"default"`)
  - they may collide with consumer-defined names; never bake `wow-two` in
- **exception — `ActivitySource` / `Meter` names DO use the brand**: `WoW.Two.<Area>`
  - trace / metric filtering then works across services — the one place the brand belongs inside the code

---

## What earns an `Extensions` class

`Extensions` names **behaviour that does not belong on a model and needs no dependency** —
logic over a model, with nowhere to live on it and nothing injected.

- **the dependency test decides it**
  - needs a repository, broker, client, context, options bag, or any I/O → `Service`, `Repository`, `Broker`
  - needs nothing → `Extensions`
- **every layer has them** — `Domain` · `Application` · `Infrastructure` · `Api` · `Persistence` each own theirs
  - never a tier between models and services
- **it extends a domain, a vector of the application** — identity, codes, billing, users
  - never the `Domain` project; the word names the subject, never the folder
  - `ContentEncodingExtensions` extends the *codes* domain and lives in `Domain`
  - `HostConfigurationExtensions` extends *hosting* and lives in `Api`
- **it does not have to extend one type**
  - a coherent body of logic over a domain is one `Extensions` class, touching several models or none
- **the receiver may be a `this` parameter or a plain argument**
  - `this` when the method reads better discovered from the type — `content.ToPayload()`
  - a plain argument when the receiver is a BCL primitive — `"abc".EscapeWifi()` would offer a WiFi method on
    every string in the solution
- **never `Helper` / `Utils` / `Common`** — they name the absence of a role
  - dependency-free behaviour over a domain is `Extensions`
  - a single transform is a `Mapper`; a holder of values is `Constants`
