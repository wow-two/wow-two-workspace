# Naming

*Last updated: 2026-08-15*

> What — cross-cutting naming for backend types, members, and extension methods (the symbol name itself — not its file, namespace, or project).
> Purpose — the name says what a thing *does*; the brand lives in the package, never repeated inside the code it ships.
> Use case — reach for it whenever you name a class, method, extension, or a bool-returning member.

## No brand / product prefix

- a **type, member, or extension-method** name carries **no product / brand prefix** — the project and package already carry it, so repeating it inside is noise
- `MigrateDatabaseAsync` not `MigrateSmartQrDatabaseAsync` · `AddCors` not `AddSmartQrCors` · `DatabaseContext` not `SmartQrDbContext`
- **project / package names keep the brand** — `SmartQr.Api`, `WoW.Two.Sdk.Backend.Beta` — the carve-out is the name that identifies the *assembly*, not the code inside it
- every symbol under `SmartQr.*` is already smart-qr's; the prefix tells a reader nothing the namespace doesn't

---

## Registration and extension-method naming

For a library that ships `IServiceCollection` / host extensions (the SDK pattern). The `## No brand / product prefix` rule applies in full: the *package* carries the brand, the *method* carries the meaning.

- **extension class** — on `IServiceCollection`, name `<Area>ServiceCollectionExtensions` (Microsoft's pattern); on any other type, `<Target>Extensions` or `<Area><Target>Extensions` — `TimeProviderExtensions`, `LoggingBuilderExtensions`, `EndpointConventionBuilderExtensions`
- **registration methods carry NO brand prefix** — describe what the call concretely registers, not who built the wrapper — `AddJwtBearerAuthentication` not `AddWowTwoJwt`, `AddOpenTelemetryTracing` not `AddWowTwoTracing`
- **acid test** — if you'd want to add `// these are wow-two's defaults`, the name is wrong; bake the meaning in so a reader who never heard of wow-two knows what it does

| Pattern | Example | When |
|---|---|---|
| `Add<Concrete>` | `AddJwtBearerAuthentication`, `AddOpenTelemetryTracing` | scheme / system-specific registration |
| `Add<Default><Thing>` | `AddDefaultCorsPolicy`, `AddDefaultOutputCache` | pre-set policy / configuration |
| `Add<Specific><Thing>` | `AddPerIpSlidingWindowRateLimit`, `AddBrotliGzipCompression` | picks one strategy among many |
| `Use<Concrete>` | `UseOwaspSecureHeaders`, `UseSerilogConventional` | pipeline middleware |
| `Map<Endpoint>` | `MapOpenApiEndpoint` | endpoint routing |
| `Add<Lib>FromAssemblies` | `AddFluentValidatorsFromAssemblies` | assembly-scanning registration |

- **stable consumer-visible identifiers stay brand-free** — cookie names (`.app.auth`), policy names (`"default"`) need system-wide uniqueness and may collide with consumer-defined names; never bake `wow-two` in
- **exception — `ActivitySource` / `Meter` names DO use the brand**: `WoW.Two.<Area>` is an *intentional* prefix so trace / metric filtering works at scale across services; this is the one place the brand belongs inside the code

### What earns an `Extensions` class

`Extensions` names **behaviour that does not belong on a model and needs no dependency.** Models carry state, not behaviour, past the odd exception. So when logic operates on a model but has nowhere to live on it, and it needs nothing injected — it takes its parameters and computes — that is an extension.

- **the dependency test decides it.** Needs a repository, a broker, a client, a context, an options bag, or any I/O → it is a `Service`, a `Repository`, a `Broker`, whatever the role is. Needs nothing → `Extensions`.
- **every layer has them.** `Domain` · `Application` · `Infrastructure` · `Api` · `Persistence` each own their extensions. This is not a tier between models and services; the layered types are not only services.
- **it extends a domain, meaning a vector of the application** — identity, codes, billing, users — not the `Domain` project. `ContentEncodingExtensions` extends the *codes* domain and lives in the `Domain` project; `HostConfigurationExtensions` extends *hosting* and lives in `Api`. The word names the subject, never the folder.
- **it does not have to extend one type.** A coherent body of logic over a domain is one `Extensions` class, even when it touches several models or none.
- **the receiver may be a `this` parameter or a plain argument.** Use `this` when the method reads better discovered from the type — `content.ToPayload()`. Use a plain argument when the receiver is a BCL primitive, because `"abc".EscapeWifi()` would offer a WiFi method on every string in the solution.
- **never `Helper` / `Utils` / `Common`** — those name the absence of a role. Dependency-free behaviour over a domain is `Extensions`; a single transform is a `Mapper`; a holder of values is `Constants`.

### `using static` is banned

- **never `using static`** on an extensions class or any other type. It strips the class name off the call site, so `Clean(value)` no longer says which extension it came from — and a file importing two of them makes that unrecoverable without jumping to the definition.
- call through the class — `ContentEncodingExtensions.Clean(value)` — or make the method a real extension method so the receiver carries the origin: `content.ToPayload()`.
- bare function calls read as another language. C# puts the owning type in the call for a reason, and the reason is exactly this readability.

---

## Predicates — `Is` / `Has` / `Can`

- a **bool-returning** method or property starts with `Is` / `Has` / `Can` (or `Should` / `Was` when tense fits), never `Be`
- `IsAbsoluteHttpUrl` not `BeAbsoluteHttpUrl` · `HasPendingChanges` · `CanRetry`
- `Be*` is FluentValidation predicate slang (`.Must(BeValid)`) — it reads as an assertion, not a state query; keep it out of method names even when the method backs a `.Must(...)`

---

## Acronyms

- **Acronyms are always PascalCase, never all-caps** — `Id` not `ID`, `Ai` not `AI`, `Api` not `API`, `Sql`, `Http`, `Json`, `Io`, `Ui`, `Mqtt`, `Grpc`.
- First letter capital, rest lowercase, **even when it distorts an established acronym** — consistency over original styling.
- Applies to type / namespace / folder / member names.
- This governs *all-caps runs* only — a mixed-case proper name with no all-caps run (`OAuth`, `SendGrid`, `MailKit`) is unaffected.
- Canonical for the whole ecosystem — the backend-beta SDK follows this rule too (its package-id grammar in `docs/architecture/package-layout.md` notes the same case-sensitive-CI trap).

## Banned

- **Hungarian notation** — `m_`, `s_`, a leading `_` on anything but a private field.
- **`Helper` · `Util` · `Utils` · `Common` · `Manager` suffixes** — banned outright, public or internal. They name the absence of a role, and an internal type needs a role as much as a public one ([components](../../../mla/components/components.md) § *Banned*).
- **`using static`** — see § *`using static` is banned* above.

## Specific naming lives by area

- which **suffix** names which **role** (one per role — `Store`→`Repository`, banned junk-drawer, new-suffix gate) → [component-names.md](../../../mla/components/components.md)
- service / client / factory → [services.md](../../../mla/components/behavior/service.md) · query / command / handler → [mediator](../../../mla/domains/messaging/mediator.md) · entity / settings / DTO → [models.md](../../constructs/constructs.md)
