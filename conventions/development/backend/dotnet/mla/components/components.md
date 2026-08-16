# Component names

*Last updated: 2026-08-15*

> What — the canonical suffix→role vocabulary for backend types: one name per role, a type's suffix declares its responsibility (the
> `Store` vs `Repository` vs `Service` decision — not the brand/casing rules in [../code-style/naming.md](../../lla/notation/naming/naming.md)).
> Purpose — kill naming entropy: when three synonyms (`Store` / `Repository` / `Provider`) all mean "data access", a reader can't infer role from the
> name; one suffix per role lets the name carry the responsibility.
> Use case — reach for it whenever you name any backend type; check the keep-list before inventing a suffix, run the gate before adding a new one.

## Renaming is never the cost [REQUIRED]

**A rename is not an argument against getting a name right.** "That would rename types in other repos" is not a reason to keep a wrong name — it is a description of the work, and the work is the point.

- must not weigh rename cost when deciding a name. Decide what is correct, then rename everything that carries the old one.
- must not preserve a wrong name because it is established, widely used, or shipped. An SDK exists precisely because a library that merely works is not enough; if working were the bar, every wrapper we write already has an upstream equivalent and none of this would be worth building.
- must treat a convention as **iterable** — a name settled last month gets re-settled the moment a better one is argued, and the sweep that follows is normal maintenance, not churn.
- the compiler and the tests are what make this cheap. A rename that builds and passes is done; that is the whole safety argument.
- the real cost to weigh is **saturation** — a vocabulary that grows a word per situation stops carrying meaning. Refuse a name because it duplicates a role, never because renaming is work.

## Terms used in this vocabulary

- **seam** — the interface at which an implementation can be swapped without editing the callers. From Michael Feathers, *Working Effectively with Legacy Code*: *a place where you can alter behavior without editing in that place*. The metaphor is the sewn seam — the join two pieces come apart at. `IGeoBroker` is a seam: swapping MaxMind in never touches `RedirectEndpoints`.
- **role** — what a type is responsible for, which is what its suffix declares. Two types with the same role take the same suffix, whatever their shape.
- **the gate** — the ordered why-questions in § *Adding a new suffix*; the first `yes` picks the suffix, and coining a new one requires all four to be `no`.

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
| `BackgroundService` | long-running work off the request path | derives from `Microsoft.Extensions.Hosting.BackgroundService`; polls a source on a timer or drains a queue — `{What}ObserveBackgroundService` for a poller. The suffix names the hosting shape; what it watches is the noun in front of it | — |
| `Client` | external single-provider call (out-of-proc) | wraps one third-party / sibling REST or SDK endpoint | `clients.md` |
| `Broker` | app-side seam over an external dependency | 3rd-party API, payment provider, file/blob store; a `Client` may sit under it, and neither owns the other | `brokers.md` |
| `Repository` | data access (rows in / rows out) | reads or persists against the DB | `services.md` · `data-access.md` |
| `Factory` | runtime instance creation | builds instances dynamically (per-key, per-request) | `services.md` |
| `Registry` | key → **type** / capability bindings | holds what callers registered at composition time and validates the set is complete — `SubtypeRegistry`. Holds types, never data; a store of instances is a `Repository` | below |
| `Tracker` | live status pushed by many producers | producers notify it as work runs, and it never persists what it accumulates; it may also own the run's control handles — `PipelineExecutionTracker`. Callers **notify** a `Tracker`; they **ask** a `Repository` | `services.md` |
| `Extensions` | the static-logic tier over a domain | stateless logic layered on a domain's types — encoding, projection, registration. No injection, no state; the receiver may be a `this` parameter or an argument | `naming.md` |
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
| `Mapper` | any deterministic in→out transform | maps one value to another — model↔model, primitive↔model, id↔bytes, enum↔token, T→T. Pure, no injection, owns no data; it transforms what it is handed | below |
| `Pipeline` / `PipelineStep` | ordered multi-step flow | a pipeline + its individual ordered steps | — |
| `Middleware`/`Filter`/`Interceptor` | framework hook | framework-named — **exempt from the gate** | — |
| `Cipher`/`Hasher`/`Issuer`/`Authenticator` | crypto / auth primitive | a single cryptographic or auth operation | — |
| `Rasterizer` | vector→pixels | rasterizes a vector form to a bitmap | — |
| `Spec` | declarative render-input shape | a declarative shape consumed by a renderer / processor — not a wire `Dto`, not config | — |
| `Json` | one type's persisted JSON seam | static holder of the `Options` plus `Serialize` / `Deserialize` for **one** type's stored representation — `CodeContentJson`, `CodeRuleJson`. Named for the format, not the type, because the type is already in the prefix | below |

Authority paths for the short names above:

- `services.md` → [../architecture/services.md](behavior/service.md) · `clients.md` → [../integrations/clients.md](behavior/client.md)
- `naming.md` / `models.md` → [../code-style/](../code-style/) · `settings.md` → [../runtime/settings.md](data/settings.md)
- `request-models.md` / `response-models.md` / `controllers.md` → [../presentation/](../presentation/)
- `mediator.md` → [../messaging/mediator.md](../domains/messaging/mediator.md) · `validation.md` / `result-pattern.md` → [./](./)
- `database.md` / `data-access.md` → [../persistence/](../persistence/)

Confirmed-in-source examples (sample paths, not exhaustive):

- `Service` — `ChannelsSeedService`, `PipelineConfigService`.
- `Client` — `TelegramClient`, `ClaudeClient`, `LocationApiClient`.
- `Repository` — `OtpRepository`, `LandmarkRepository`.
- `Factory` — `VaultDbContextFactory` (`secrets-vault.backend-services/SecretsVault.Persistence/`), `DataSourceConnectionFactory`.
- `Registry` — `PipelineRegistry`, `EventDispatcherRegistry` (SDK `src/Messaging/`).
- `Tracker` — `PipelineExecutionTracker`.
- `Configuration` (EF) — `ChannelConfiguration : IEntityTypeConfiguration<Channel>` (`sift.backend-services/Sift.Persistence/Configurations/`).
- `Options` — `JwtTokenIssuerOptions`, `OtpOptions` (SDK `src/Identity/`).
- `Cipher`/`Hasher`/`Issuer`/`Authenticator` — `AesGcmCipher`, `HashChainHasher`, `JwtAdminTokenIssuer`, `Argon2AdminAuthenticator`
  (`secrets-vault.backend-services/SecretsVault.Infrastructure/`).
- `Rasterizer` — `SkiaSvgRasterizer : ISvgRasterizer` (SDK `src/Codes/Rendering/Raster/`).
- `Spec` — `StyleSpec`, `LogoSpec` (SDK `src/Codes/Models/Style/`) — render-input shapes the SVG path consumes.
- `Broker` — `StripeBillingBroker` (`smart-qr-poc/engineering/codebase/smartqr.backend-services/SmartQr.Infrastructure/Billing/Services/`) —
  the app-side seam over the Stripe payment provider.
- `Renderer`/`Generator` — `SvgRenderer`, `QrMatrixGenerator : IQrMatrixGenerator` (SDK `src/Codes/Rendering/`) — the `Emitter`→`Renderer`
  and `Source`→`Generator` folds, landed.

### `Mapper` vs `Registry` — who owns the data

Both answer "given X, give me Y". The line is **ownership of the mapping data**.

- `Mapper` — is **handed** what it needs, every call. `PlanPriceMapper.PriceIdFor(settings, plan)` takes the settings; it stores nothing. Pure, no injected collaborators, no I/O. Any in→out transform qualifies: model↔model, primitive↔model, id↔bytes, enum↔wire token, or `T → T`.
- `Registry` — **owns** the set. Callers register items into it at construction, it validates the set is complete, and it answers lookups against what it holds. `SubtypeRegistry` throws when an enum member has no registered subtype; a `Mapper` has nothing to be incomplete about.
- the test: *does the data live inside the type, or arrive as an argument?* inside → `Registry`; argument → `Mapper`.
- a lookup that needs injected collaborators or I/O is neither — that is a `Service` or a `Broker`.

**A `Registry` holds types and capabilities. A `Repository` holds data.** That is the line, and it is not about where the store lives — an in-memory `Repository` is still a `Repository`, because it still holds *instances*.

| | `Registry` | `Repository` |
|---|---|---|
| Holds | key → **type** or capability bindings | **instances** of an entity |
| Entries appear | declared at composition time, in code | at runtime, from user or system action |
| Entries identified by | the key they were registered under | their own identity |
| Answering a lookup gives you | something to **dispatch to** | something to **read or write** |

- **registration must be a real act.** If nothing registers, it is not a registry — a lookup table read from config is a `Mapper` handed its data, however it was populated.
- **completeness is the registry's to enforce.** `SubtypeRegistry` throws when an enum member has no registered subtype; owning the set means owning whether the set is whole.
- `SubtypeRegistry<CodeContentValueObject, CodeContentType>` binds each enum member to a `Type` so serialization can dispatch. Nothing about it is data.
- `PlanPriceMap` bound a `Plan` to a **price-id string** — a value, not a type — which is why it folded to `Mapper`.

### `Client` vs `Broker` — whose model does it speak

Both reach an external system. The line is **whose vocabulary the type exposes**, and neither depends on the other existing.

- `Client` — speaks the **provider's** model. It surfaces the external system's own types and its full call set, and adds nothing of ours. A Redis client offers Redis's commands and Redis's shapes.
- `Broker` — speaks **ours**. It is the app-facing abstraction over that system, built for our purpose, and it owns whatever we need on top: auth, caching, retry, error mapping, defaults. A cache-storage broker offers *our* cache operations, whatever it calls underneath.
- the test: *would this type's surface change if we swapped the provider?* No → `Client`, it is the provider's shape. Yes → `Broker`, it is ours.
- **either may exist alone.** A `Client` with no `Broker` over it is legitimate; it is simply less useful, since the caller then carries the provider's whole model. A `Broker` with no `Client` under it is equally fine — the vendor SDK plays that part.
- a `Broker` may sit over a `Client`, over a vendor SDK, or over raw `HttpClient`. What it sits on is not what names it.

### `Settings` vs `Options` — the one disambiguation

- `Settings` — **bound from config** (`appsettings.json` via `IOptions<TSettings>`); `sealed record`, `init`-only, no defaults —
  `ClassificationSettings`, `CorsSettings`.
- `Options` — **behavior knobs passed in code** to a helper / pipeline, not a config section — `HttpResilienceOptions`, `JwtTokenIssuerOptions`.
- the test: *does the config binder populate it?* yes → `Settings`; supplied by a caller's delegate / `new` → `Options`.

### Request sub-blocks — verb-first vs noun-first

The `{Verb}{Noun}ApiRequest` rule ([request-models.md](data/request-model.md)) governs the **top-level** request — the body a
controller action binds. A body **sub-block nested inside** a request carries no verb of its own; name it **noun-first `{Noun}ApiRequest`**.

- top-level → `PreviewCodeApiRequest`, `CreateCodeApiRequest` (verb-first — the action).
- nested sub-block → `StyleApiRequest`, `LogoApiRequest` (noun-first — a `Style`/`Logo` block; `StyleApiRequest` is shared across `PreviewCodeApiRequest`/`CreateCodeApiRequest`/`UpdateCodeApiRequest`). `smart-qr-poc/engineering/codebase/smartqr.backend-services/SmartQr.Api/Requests/Codes/`.

### `Extensions` — per target, or per family

Default: name the **domain the logic belongs to**, not the type it happens to extend — `ContentEncodingExtensions`, `HostConfigurationExtensions`.

- an extension class is the static-logic tier over a domain, so the domain is what identifies it; the receiver type is an implementation detail of each method.
- **never carry an interface's `I` into the class name** — `ServiceCollectionExtensions`, never `IServiceCollectionExtensions`. The `I` belongs to the interface, and the class is not one.
- **must not name a type the domain does not answer to** — `ContentWifiTypeExtensions` names an enum, `ICodeRepositoryExtensions` names an interface. Both lock the class to one declaration, so the first method touching a sibling forces a rename. `WifiEncryptionExtensions` is fine: Wi-Fi encryption *is* the subject, not an incidental target.
- name the target type only when the target **is** the domain — `ServiceCollectionExtensions` for container registration, where the container is the subject.
- for DI registration in a library, `naming.md` narrows this further to `<Area>ServiceCollectionExtensions` ([naming.md](../../lla/notation/naming/naming.md) § *Registration and extension-method naming*).

**Exception — a closed family.** When several types form one modelled family (a discriminated union's variants plus the enums they carry), one `{Family}Extensions` class may host the extensions for all of them.

- must apply only to a **closed** set the codebase owns — a union with a fixed variant list, not an open bag of related types
- must name the family, not one member: `WifiContentExtensions`, not `WifiEncryptionExtensions` when it also extends the content type
- the family class owns the family's format constants too, keeping wire spellings out of the model
- rationale: a per-target split gives 2+ files per family and scatters one wire contract; per-family gives one place to look and one place for the spec's literals to live
- summary starter is `Extends` — see [documentation/summary.md](../../lla/notation/documentation/summary.md) § *Extension classes*

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
| `Resolver` | `Mapper` · `Broker` · `Service` | "resolve" names no verb of its own. Pure and deterministic → `Mapper`; reaches out-of-process → `Broker`; needs injected collaborators → `Service`. Every candidate lands in one of the three |
| *(framework names)* | — | a third-party API is named as it ships, because we **call** it rather than coined it — `DefaultJsonTypeInfoResolver` (`models.md`), `ValidatorOptions.Global.ErrorCodeResolver` (`validation.md`). Every fold governs names we choose |
| `Normalizer` | `Mapper` | canonicalizing is a `T → T` transform, and a transform is a `Mapper`. The idempotence is a property of the function, not a distinct role |
| `Map` (as a suffix) | `Mapper` | the type *maps*; `PlanPriceMap` reads as data, and it is a function |
| `Emitter` | `Renderer` | emitting a representation of a model is rendering it |
| `Source` | `Generator` | when the type **derives / produces** a value, it generates it |
| `Observer` | `Handler` · `BackgroundService` | reacting to something that happened is a handler's verb, and the event bus already fans one event out to a registered set. A type that *polls* a source on a timer is a hosted service — `{Source}ObserveBackgroundService`; observing is what it does, never what it is |
| `Scheduler` | `BackgroundService` | a poller on a timer schedules nothing, it runs. Keep the word only for a type that decides when **other** work runs, and even then it is a `BackgroundService` doing the deciding |
| `Keeper` | `Service` | "keeper" is a synonym for a stateful service |

Seen-as sources (real today; the fold renames them):

- `Store` — `ISecretStore`/`EfSecretStore` (vault), `IOtpStore`/`MemoryOtpStore` (SDK). Landed in drydock: `IProductRepository`/`EfProductRepository`.
- `Gateway` — landed in smart-qr: `IBillingGateway` → `IBillingBroker`, the Stripe payment seam (concrete `StripeBillingBroker`, keep-list above).
- `Provider` — `SystemJsonSerializationOptionsProvider` (SDK serialization).
- `Node` — `FetchUnclassifiedNode`, `PersistClassifiedNode` inside `ClassifyPipeline` (Haven).
- `Mapping`/`Profile` — `SymptomAnalysisMappingProfile : Profile`, `DoctorMapper : Profile` (your-pocket-doctor).
- `Emitter` / `Source` — landed in the SDK: `SvgEmitter` → `SvgRenderer`, `QrCoderMatrixSource` → `QrMatrixGenerator`.
- `Keeper` — `MasterKeySealKeeper : ISealKeeper` (vault).

> `Source` exception — keep `Source` only where it names a **content origin you read from**, not a value you derive: `IMigrationSource` /
> `FileSystemMigrationSource` (the SDK migrator's "where scripts come from") is a legitimate `Source`. The fold targets the *derive-a-value*
> misuse — `QrCoderMatrixSource` derives the matrix, so it folds to `QrMatrixGenerator` (§ *Settled*).

---

## Adding a new suffix — the gate [REQUIRED]

Before coining a suffix, answer the why-questions in order; the first **yes** picks the suffix:

1. **does it call out-of-process** (external API, sibling service)? → `Client` (concrete single-provider HTTP client) or `Broker` (app-side seam).
2. **does it persist or read rows**? → `Repository`.
3. **does it only supply configuration** — bound from config vs knobs in code? → `Settings` / `Options`.
4. **is it pure compute / orchestration** with no narrower role? → `Service`.

Coin a **new** suffix only when the type names a role **no existing suffix covers** — a genuinely distinct verb, not a synonym for one above.
That's the bar `Rasterizer` (vector→pixels — neither render-to-markup nor compute) cleared. `Manager` / `Helper` / `Engine` fail it by
definition: they name no verb.

**Never coin a suffix inline.** A name that misses is copied forward by every later scaffold, and the SDK is young enough that most new
components land in a category the keep-list has not written yet. Coining is its own step, and it never rides inside the implementation:

1. **state the role's verb** — what the type does for its caller, in one line. No verb to state → it is a `Service`, not a new suffix.
2. **name the nearest two existing suffixes and why each fails** — a suffix that fails against none of them is a synonym, and synonyms fold.
3. **bring both to the developer and wait.** Only a confirmed suffix gets implemented, and it lands in the keep-list in the same pass.

Rapid scaffolding does not lower this bar, it raises it: scaffolding is where an unconfirmed name gets replicated fastest.

---

## Model suffixes

Lifted from `lla/shape/models.md` — a suffix is component vocabulary, so it lives with the keep-list.

- **Entities** — suffix with `Entity` when the type maps 1:1 to a DB table (`ChannelEntity` → `channels` table)
- **Value objects within entities** — suffix with `ValueObject` (`WifiContentValueObject`, `CodeRuleValueObject`). A persisted value object reads as an entity otherwise, and the suffix is what separates a type that owns a row from one that rides inside one. The wire is unaffected when a `SubtypeRegistry` binds discriminators to types explicitly.
  - Frontend types do **not** mirror the suffix — a browser-side type is a wire projection, not a persisted object, and naming it after the domain claims an identity and change-tracking it does not have. Suffix those `Dto`.
- **DTOs** — suffix with `Dto` (`ChannelDto`, `ChannelWithPipelinesDto`)
- **Settings** — suffix with `Settings` (`ClassificationSettings`)
- **Results** — suffix with `Result` (`ChannelGetAllResult`)
- **Query/Command** — suffix with `Query` / `Command` (`ChannelGetAllQuery`, `PipelineExecuteCommand`)

## Banned — the junk drawer

Zero usage across the surveyed product apps today. They name *nothing* — they describe "a class that does stuff". Never introduce one; if you reach
for one, the gate above points you at the real role.

| Banned | Why it's empty / forbidden | Reach for instead |
|---|---|---|
| `Manager` | "manages" = does unspecified work | `Service` / `Registry` / `Tracker` |
| `Helper` | a dumping ground for orphan statics | `Extensions`, or fold into its owner |
| `Util` / `Utils` | same as `Helper`, vaguer | `Extensions` |
| `Accessor` | "accesses" = reads — say what | `Repository` / `Client` / `Service` |
| `Engine` | "engine" = important-sounding `Service` | `Service`, or `Pipeline` if it's a flow |

> Lone legacy hit: `CronHelper` in paused Haven — pre-dates this convention, not a counter-example. New code: none.

---

## Settled — render & finder names

> Decided, and the renames have landed in the SDK `src/Codes/`. `Spec` and the request sub-blocks are covered by the keep-list and
> § *Request sub-blocks* — not repeated here.

- **Finder inner shape — keep `Dot`.** The enum stays `FinderDotShape`: `Dot` matches the wire field (`finderDotShape`), the frontend, and
  `qr-code-styling`'s `cornersDot`. `AppendFinderDot` + the `FinderDotSize` const carry the same word.
- **Render renames** — `QrCoderMatrixSource` → `QrMatrixGenerator` (`IQrMatrixSource` → `IQrMatrixGenerator`, `.Create` → `.Generate`);
  `SvgEmitter` → `SvgRenderer`. **Keep** `SkiaSvgRasterizer` (`Rasterizer`): it cleared the gate.
- **`StyleSpecNormalizer` → `StyleSpecMapper`** — no exemption. `StyleSpec → StyleSpec` is a transform, and the fold above owns every
  transform; idempotence is a property of the function, not a role. The type is SDK-side (`src/Codes/Models/Style/`), so the rename is the
  SDK sweep's to land — this doc is the authority, not the diff.

---

## Authoring this doc

- super-compact — vocabulary + role, not prose; cite the authority, don't restate its rules.
- every claim cites a **real** symbol (path + type) in a surveyed app — no invented examples.
- 150-col lines.
