# Component names

*Last updated: 2026-06-24*

> What — the canonical suffix→role vocabulary for backend types: one name per role, a type's suffix declares its responsibility (the
> `Store` vs `Repository` vs `Service` decision — not the brand/casing rules in [../code-style/naming.md](../code-style/naming.md)).
> Purpose — kill naming entropy: when three synonyms (`Store` / `Repository` / `Provider`) all mean "data access", a reader can't infer role from the
> name; one suffix per role lets the name carry the responsibility.
> Use case — reach for it whenever you name any backend type; check the keep-list before inventing a suffix, run the gate before adding a new one.

## How to use

- pick the suffix whose **role** matches what the type does — the suffix is a contract, not decoration.
- detail of *how* a role behaves lives in the cited authority, not here — this doc is the vocabulary, those are the rules.
- a synonym you were about to use → find it in **Folds**, use the canonical name instead.
- no existing suffix fits → run the **gate** (§ Adding a new suffix) before coining one.
- framework-named types (`Middleware` / `Filter` / `Interceptor`) are exempt — the framework owns the name.

---

## Keep-list — canonical suffixes

One suffix per role. Most are already law in another convention — that doc is the **authority**, this row is the index, not a restatement.
Detail (shape, docs, lifetime) stays in the authority; cite it, don't duplicate it.

| Suffix | Role | When | Authority |
|---|---|---|---|
| `Service` | business logic / orchestration / compute | default for "does work", no narrower role fits | `services.md` |
| `Client` | external single-provider call (out-of-proc) | wraps one third-party / sibling REST or SDK endpoint | `clients.md` |
| `Broker` | app-side seam over an external dependency | 3rd-party API, payment provider, file/blob store; `Client` may sit under it | `clients.md` |
| `Repository` | data access (rows in / rows out) | reads or persists against the DB | `services.md` · `data-access.md` |
| `Factory` | runtime instance creation | builds instances dynamically (per-key, per-request) | `services.md` |
| `Registry` | lookup of pre-registered items | resolves from a fixed set populated at startup | `services.md` |
| `Tracker` | in-proc mutable state | holds live state in memory, not DB I/O | `services.md` |
| `Extensions` | static / DI helper methods | `IServiceCollection` / host / target-type helpers | `naming.md` |
| `Handler` + `Command`/`Query`/`Event` | CQRS message + its handler | a dispatched use-case (read / write / fan-out) | `mediator.md` |
| `Validator` | input validation | `IValidator<T>` for a request | `validation.md` |
| `Controller` | HTTP delivery surface | thin dispatcher at the API edge | `controllers.md` |
| `Request` / `Response` | API edge body | client-facing `{Verb}{Noun}ApiRequest` / response envelope | `request-models.md` · `response-models.md` |
| `Dto` / `Entity` / `Result` | data carriers | projection / table-mapped row / operation outcome | `models.md` · `result-pattern.md` |
| `Settings` | config-section binding | binds an `appsettings.json` section via `IOptions<T>` | `settings.md` |
| `Options` | behavior knobs | tuning passed to a helper / pipeline, not bound from config | below |
| `DbContext` | EF Core unit-of-work | the EF context type | `database.md` |
| `Configuration` | EF entity mapping | an `IEntityTypeConfiguration<T>` | — |
| `Constants` | static definitions | a holder of `const` / `static readonly` values | `services.md` |
| `Mapper` | object→object transform | maps one shape to another (incl. AutoMapper) | — |
| `Pipeline` / `PipelineStep` | ordered multi-step flow | a pipeline + its individual ordered steps | — |
| `Middleware`/`Filter`/`Interceptor` | framework hook | framework-named — **exempt from the gate** | — |
| `Cipher`/`Hasher`/`Issuer`/`Authenticator` | crypto / auth primitive | a single cryptographic or auth operation | — |
| `Rasterizer` | vector→pixels | rasterizes a vector form to a bitmap | — |
| `Normalizer` | returns a canonicalized form | maps an input to its canonical / normalized value | — |
| `Resolver` | resolves an ambiguous input to a canonical value, in-proc | no external call; if it ever makes one → `Broker` | — |
| `Spec` | declarative render-input shape | a declarative shape consumed by a renderer / processor — not a wire `Dto`, not config | — |

Authority paths for the short names above:

- `services.md` → [../architecture/services.md](../architecture/services.md) · `clients.md` → [../integrations/clients.md](../integrations/clients.md)
- `naming.md` / `models.md` → [../code-style/](../code-style/) · `settings.md` → [../runtime/settings.md](../runtime/settings.md)
- `request-models.md` / `response-models.md` / `controllers.md` → [../presentation/](../presentation/)

Confirmed-in-source examples (sample paths, not exhaustive):

- `Service` — `ChannelsSeedService`, `PipelineConfigService`.
- `Client` — `TelegramClient`, `ClaudeClient`, `LocationApiClient`.
- `Repository` — `OtpRepository`, `LandmarkRepository`.
- `Factory` — `VaultDbContextFactory` (`secrets-vault.backend-services/SecretsVault.Persistence/`), `DataSourceConnectionFactory`.
- `Registry` — `PipelineRegistry`, `MessageDispatcherRegistry`.
- `Tracker` — `PipelineExecutionTracker`.
- `Configuration` (EF) — `ChannelConfiguration : IEntityTypeConfiguration<Channel>` (`sift.backend-services/Sift.Persistence/Configurations/`).
- `Options` — `JwtTokenIssuerOptions`, `OtpOptions` (SDK `src/Identity/`).
- `Cipher`/`Hasher`/`Issuer`/`Authenticator` — `AesGcmCipher`, `HashChainHasher`, `JwtAdminTokenIssuer`, `Argon2AdminAuthenticator`
  (`secrets-vault.backend-services/SecretsVault.Infrastructure/`).
- `Rasterizer`/`Normalizer` — `SkiaSvgRasterizer : ISvgRasterizer`, `StyleSpecNormalizer`
  (`smart-qr-poc/platform/src/backend/SmartQr.Codes/Rendering/Raster/`, `.../SmartQr.Codes/Models/Style/`).
- `Spec` — `StyleSpec`, `LogoSpec` (`smart-qr-poc/platform/src/backend/SmartQr.Codes/Models/Style/`) — render-input shapes the SVG path consumes.
- `Broker` — `StripeBillingBroker` (smart-qr, post-rename) — the app-side seam over the Stripe payment provider.
- `Resolver` — `IGeoResolver` (smart-qr — MaxMind-local, in-proc — no external call).
- `Renderer`/`Generator` — `SvgRenderer` (was `SvgEmitter`), `QrMatrixGenerator : IQrMatrixGenerator` (was `QrCoderMatrixSource`,
  `.Generate()`) (`smart-qr-poc/platform/src/backend/SmartQr.Codes/Rendering/`) — the `Emitter`→`Renderer` and `Source`→`Generator` folds.

### `Client` vs `Broker` — the boundary

- `Client` — a **concrete single-provider HTTP client** wrapping one third-party / sibling endpoint (`TelegramClient`, `ClaudeClient`).
- `Broker` — the **application-side dependency seam / port** over an external resource (3rd-party API, payment provider, file/blob store); may
  use a `Client` under it — `StripeBillingBroker` (smart-qr).
- the test: *am I the wire-level caller, or the app-facing seam the domain depends on?* wire → `Client`; seam → `Broker`.

### `Settings` vs `Options` — the one disambiguation

- `Settings` — **bound from config** (`appsettings.json` via `IOptions<TSettings>`); `sealed record`, `init`-only, no defaults —
  `ClassificationSettings`, `CorsSettings`.
- `Options` — **behavior knobs passed in code** to a helper / pipeline, not a config section — `HttpResilienceOptions`, `JwtTokenIssuerOptions`.
- the test: *does the config binder populate it?* yes → `Settings`; supplied by a caller's delegate / `new` → `Options`.

### Request sub-blocks — verb-first vs noun-first

The `{Verb}{Noun}ApiRequest` rule ([request-models.md](../presentation/request-models.md)) governs the **top-level** request — the body a
controller action binds. A body **sub-block nested inside** a request carries no verb of its own; name it **noun-first `{Noun}ApiRequest`**.

- top-level → `PreviewCodeApiRequest`, `CreateCodeApiRequest` (verb-first — the action).
- nested sub-block → `StyleApiRequest`, `LogoApiRequest`, `RuleApiRequest` (noun-first — a `Style`/`Logo`/`Rule` block; `StyleApiRequest` is shared across `PreviewCodeApiRequest`/`CreateCodeApiRequest`/`UpdateCodeApiRequest`). `smart-qr-poc/platform/src/backend/SmartQr.Api/Requests/`.

---

## Folds — synonyms → the one canonical name

Each left-hand suffix means a role an existing suffix already owns. Don't introduce the synonym; rename to the canonical. The seen-as symbols below
are real in the surveyed apps — the fold is the migration target, not a claim they're already renamed.

| Synonym | Canonical | Why |
|---|---|---|
| `Store` | `Repository` | both are "rows in / rows out" against a backing store |
| `Gateway` | `Broker` | a gateway to an external system is the app-side dependency seam — that's `Broker` |
| `Provider` | `Service` | "provides X" is what every service does; the word adds nothing |
| `Node` | `PipelineStep` | a node only has meaning inside a pipeline — name it as the step it is |
| `Encryptor` | `Cipher` | `Cipher` is the established crypto-primitive suffix |
| `Mapping` / `Profile` | `Mapper` | the type *maps*; `Profile` is AutoMapper's base type, not a role name |
| `Emitter` | `Renderer` | emitting a representation of a model is rendering it |
| `Source` | `Generator` | when the type **derives / produces** a value, it generates it |
| `Keeper` | `Service` | "keeper" is a synonym for a stateful service |

Seen-as sources (real today; the fold renames them):

- `Store` — `IProductStore`/`EfProductStore` (drydock), `ISecretStore`/`EfSecretStore` (vault), `IOtpStore`/`MemoryOtpStore` (SDK).
- `Gateway` — `IBillingGateway` → `IBillingBroker` (smart-qr — the Stripe payment seam; concrete `StripeBillingBroker` keep-list example above).
- `Provider` — `SystemJsonSerializationOptionsProvider` (SDK serialization).
- `Node` — `FetchUnclassifiedNode`, `PersistClassifiedNode` inside `ClassifyPipeline` (Haven).
- `Mapping`/`Profile` — `SymptomAnalysisMappingProfile : Profile`, `DoctorMapper : Profile` (your-pocket-doctor).
- `Emitter` / `Source` — `SvgEmitter` → `SvgRenderer`, `QrCoderMatrixSource` → `QrMatrixGenerator` (smart-qr — settled below).
- `Keeper` — `EnvKekSealKeeper` (vault).

> `Source` exception — keep `Source` only where it names a **content origin you read from**, not a value you derive: `IMigrationSource` /
> `FileSystemMigrationSource` (the SDK migrator's "where scripts come from") is a legitimate `Source`. The fold targets the *derive-a-value*
> misuse — `QrCoderMatrixSource` derives the matrix, so it folds to `QrMatrixGenerator` (§ Settled — smart-qr).

---

## Banned — the junk drawer

Zero usage across the surveyed product apps today. They name *nothing* — they describe "a class that does stuff". Never introduce one; if you reach
for one, the gate below points you at the real role.

| Banned | Why it's empty / forbidden | Reach for instead |
|---|---|---|
| `Manager` | "manages" = does unspecified work | `Service` / `Registry` / `Tracker` |
| `Helper` | a dumping ground for orphan statics | `Extensions`, or fold into its owner |
| `Util` / `Utils` | same as `Helper`, vaguer | `Extensions` |
| `Accessor` | "accesses" = reads — say what | `Repository` / `Client` / `Service` |
| `Engine` | "engine" = important-sounding `Service` | `Service`, or `Pipeline` if it's a flow |

> Lone legacy hit: `CronHelper` in paused Haven — pre-dates this convention, not a counter-example. New code: none.

---

## Adding a new suffix — the gate

Before coining a suffix, answer the why-questions in order; the first **yes** picks the suffix:

1. **does it call out-of-process** (external API, sibling service)? → `Client` (concrete single-provider HTTP client) or `Broker` (app-side seam).
2. **does it persist or read rows**? → `Repository`.
3. **does it only supply configuration** — bound from config vs knobs in code? → `Settings` / `Options`.
4. **is it pure compute / orchestration** with no narrower role? → `Service`.

Coin a **new** suffix only when the type names a role **no existing suffix covers** — a genuinely distinct verb, not a synonym for one above.
That's the bar `Rasterizer` (vector→pixels — neither render-to-markup nor compute) and `Normalizer` (returns a canonical form — distinct from
`Mapper`'s shape→shape) cleared. `Manager` / `Helper` / `Engine` fail it by definition: they name no verb.

---

## Settled — smart-qr render & finder names

> The four open questions are decided. Recorded here as the migration targets; symbols cited are real in `smart-qr-poc/platform/src/backend/`.

- **`Spec`** — blessed (keep-list above). `StyleSpec` / `LogoSpec` stay — declarative render-input shapes.
- **Request sub-blocks** — carved out (§ Request sub-blocks). `PreviewStyleApiRequest` / `PreviewLogoApiRequest` stay noun-first.
- **Finder inner shape — keep `Dot`.** The enum stays `FinderDotShape`: `Dot` matches the wire field (`finderDotShape`), the frontend, and
  `qr-code-styling`'s `cornersDot`. Resolution: align the lone internal method `SvgEmitter.AppendFinderPupil` → `AppendFinderDot` (and its
  `FinderDotSize` const reads consistently) so code matches the domain word the wire already uses.
- **Render renames** — `Source`→`Generator`: `QrCoderMatrixSource` → `QrMatrixGenerator` (+ `IQrMatrixSource` → `IQrMatrixGenerator`, method
  `.Create` → `.Generate`). `Emitter`→`Renderer`: `SvgEmitter` → `SvgRenderer`. **Keep** `SkiaSvgRasterizer` (`Rasterizer`) and
  `StyleSpecNormalizer` (`Normalizer` — → canonical form): both cleared the gate, intentionally exempt from the renames.

---

## Authoring this doc

- super-compact — vocabulary + role, not prose; cite the authority, don't restate its rules.
- every claim cites a **real** symbol (path + type) in a surveyed app — no invented examples.
- 150-col lines.
