# Naming

*Last updated: 2026-08-15*

> What — cross-cutting naming for backend types, members, and extension methods — the symbol name, not its file,
> namespace, or project.
> Purpose — the name says what a thing *does*; the brand lives in the package, never inside the code it ships.
> Use case — reach for it whenever you name a class, method, extension, or a bool-returning member.

## No brand / product prefix

- a **type, member, or extension-method** name carries **no product / brand prefix**
- `MigrateDatabaseAsync` not `MigrateSmartQrDatabaseAsync` · `DatabaseContext` not `SmartQrDbContext`
- **project / package names keep the brand** — `SmartQr.Api`, `WoW.Two.Sdk.Backend.Beta`; the carve-out is the
  name that identifies the *assembly*, not the code inside it
- every symbol under `SmartQr.*` is already smart-qr's; the prefix tells a reader nothing the namespace doesn't

---

## Registration and extension-method naming

For a library that ships `IServiceCollection` / host extensions (the SDK pattern). § *No brand / product prefix*
applies in full: the *package* carries the brand, the *method* carries the meaning.

- **extension class** — on `IServiceCollection`, name `<Area>ServiceCollectionExtensions` (Microsoft's pattern)
  - on any other type, `<Target>Extensions` or `<Area><Target>Extensions` — `TimeProviderExtensions`,
    `LoggingBuilderExtensions`, `EndpointConventionBuilderExtensions`
- **registration methods carry NO brand prefix** — describe what the call registers, not who built the wrapper
  - `AddJwtBearerAuthentication` not `AddWowTwoJwt` · `AddOpenTelemetryTracing` not `AddWowTwoTracing`
- **acid test** — if you'd want to add `// these are wow-two's defaults`, the name is wrong; bake the meaning in
  so a reader who never heard of wow-two knows what it does

- `Add<Concrete>` — `AddJwtBearerAuthentication`, `AddOpenTelemetryTracing` · scheme / system-specific registration
- `Add<Default><Thing>` — `AddDefaultCorsPolicy`, `AddDefaultOutputCache` · pre-set policy / configuration
- `Add<Specific><Thing>` — `AddPerIpSlidingWindowRateLimit`, `AddBrotliGzipCompression` · picks one strategy of many
- `Use<Concrete>` — `UseOwaspSecureHeaders`, `UseSerilogConventional` · pipeline middleware
- `Map<Endpoint>` — `MapOpenApiEndpoint` · endpoint routing
- `Add<Lib>FromAssemblies` — `AddFluentValidatorsFromAssemblies` · assembly-scanning registration

- **stable consumer-visible identifiers stay brand-free** — cookie names (`.app.auth`), policy names (`"default"`)
  may collide with consumer-defined names; never bake `wow-two` in
- **exception — `ActivitySource` / `Meter` names DO use the brand**: `WoW.Two.<Area>`, so trace / metric filtering
  works across services. The one place the brand belongs inside the code.

### What earns an `Extensions` class

`Extensions` names **behaviour that does not belong on a model and needs no dependency.** Logic that operates on a
model, has nowhere to live on it, and needs nothing injected is an extension.

- **the dependency test decides it** — needs a repository, broker, client, context, options bag, or any I/O → it is
  a `Service`, `Repository`, `Broker`, whatever the role is. Needs nothing → `Extensions`.
- **every layer has them** — `Domain` · `Application` · `Infrastructure` · `Api` · `Persistence` each own their
  extensions. Not a tier between models and services.
- **it extends a domain, meaning a vector of the application** — identity, codes, billing, users — not the `Domain`
  project. The word names the subject, never the folder.
  - `ContentEncodingExtensions` extends the *codes* domain and lives in `Domain`
  - `HostConfigurationExtensions` extends *hosting* and lives in `Api`
- **it does not have to extend one type** — a coherent body of logic over a domain is one `Extensions` class, even
  when it touches several models or none.
- **the receiver may be a `this` parameter or a plain argument**
  - `this` when the method reads better discovered from the type — `content.ToPayload()`
  - a plain argument when the receiver is a BCL primitive — `"abc".EscapeWifi()` would offer a WiFi method on
    every string in the solution
- **never `Helper` / `Utils` / `Common`** — they name the absence of a role. Dependency-free behaviour over a domain
  is `Extensions`; a single transform is a `Mapper`; a holder of values is `Constants`.

### `using static` is banned

- **never `using static`** on an extensions class or any other type — it strips the class name off the call site,
  so `Clean(value)` no longer says which extension it came from.
- call through the class — `ContentEncodingExtensions.Clean(value)` — or make it a real extension method so the
  receiver carries the origin: `content.ToPayload()`.
- bare function calls read as another language — C# puts the owning type in the call for readability.

---

## Predicates — `Is` / `Has` / `Can`

- a **bool-returning** method or property starts with `Is` / `Has` / `Can` (or `Should` / `Was` by tense), never `Be`
- `IsAbsoluteHttpUrl` not `BeAbsoluteHttpUrl` · `HasPendingChanges` · `CanRetry`
- `Be*` is FluentValidation slang (`.Must(BeValid)`) — it reads as an assertion, not a state query; keep it out of
  method names even when the method backs a `.Must(...)`

---

## Acronyms

- **Acronyms are always PascalCase, never all-caps** — `Id` not `ID`, `Api` not `API`, `Sql`, `Http`, `Json`, `Ui`.
- First letter capital, rest lowercase, **even when it distorts an established acronym**.
- Applies to type / namespace / folder / member names.
- Governs *all-caps runs* only — a mixed-case proper name (`OAuth`, `SendGrid`, `MailKit`) is unaffected.
- Canonical for the whole ecosystem — the backend-beta SDK follows it too (`docs/architecture/package-layout.md`).

---

## Banned

- **Hungarian notation** — `m_`, `s_`, a leading `_` on anything but a private field.
- **`Helper` · `Util` · `Utils` · `Common` · `Manager` suffixes** — banned outright, public or internal
  - they name the absence of a role, and an internal type needs a role as much as a public one
  - [components](../../../mla/components/components.md) § *Banned*
- **`using static`** — see § *`using static` is banned* above.

---

## Specific naming lives by area

- which **suffix** names which **role** (one per role, `Store`→`Repository`, banned junk-drawer, new-suffix gate)
  → [components](../../../mla/components/components.md)
- service / client / factory → [services](../../../mla/constructs/behavior/service.md)
- query / command / handler → [mediator](../../../mla/domains/messaging/mediator/mediator.md)
- entity / settings / DTO → [constructs](../../constructs/constructs.md)
