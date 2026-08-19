# Conventions — Development — Backend (.NET)

*Last updated: 2026-08-19*

> .NET conventions for every backend service under `wow-two-ws/`. Lookup table — open a file when the task
> touches it; do not pre-read. Cut by **scope**: how far a rule reaches.
> How to write a doc here → template + rules in [conventions](../../../conventions.md).

## The three scopes

| Scope | Reaches | Holds |
|---|---|---|
| `lla/` | one symbol | `constructs/` (what C# offers) · `notation/` (how any symbol is written) |
| `mla/` | one service, and everything it talks to | `constructs/` · `components/` · `architecture/` · `platform/` · `domains/` |
| `hla/` | between our own services | gateway · gRPC contracts · cross-service events · quotas |

Each scope's own lead: [lla](lla/lla.md) · [mla](mla/mla.md) · [hla](hla/hla.md).

**Routing.** A kind of type you declare → `mla/constructs/{kind}.md`. A thing complete on its own → `mla/components/`. How any symbol is written → `lla/`.
Where a type lives → `mla/architecture/`. How the service builds and starts → `mla/platform/`. A concrete
technology or use case → `mla/domains/{domain}/`. A rule spanning services we both own → `hla/`.

**The test between `mla/` and `hla/`:** do we own both ends? A third party is adapted in `mla/`, never contracted in `hla/`.
**The three levels, and where each lands.** A C# construct is [constructs](lla/constructs/constructs.md). Everything we
define lands in `mla/`: a **role** that needs something else present → `mla/constructs/` (`Entity`, `Controller`, `Broker`);
a **thing complete alone** → `mla/components/` (`Constants`, `Enums`, `Settings`). A ban follows its rule — construct bans
in `lla/`, role bans with the role.

**The test between baseline and a domain:** would the rule survive if the feature were deleted? Yes → baseline. No → the domain that owns it.

---

## The layers of a thing [REQUIRED]

The model is [development conventions](../../development-conventions.md) § *The layers of a thing*.
What it means here:

| Layer | Home | Example |
|---|---|---|
| 1 · baseline | [lla/constructs](lla/constructs/constructs.md) | `const` · `record` · `BackgroundService` · `TimeProvider` |
| 2 · construct | [mla/constructs](mla/constructs/constructs.md) | what a `Broker`, a `Constants` class or an `Entity` **is** |
| 3 · application | [mla/components](mla/components/components.md) · [mla/domains](mla/domains/) | how it is applied, split by whether it stands alone |

- must not document a third-party library's own surface → [development conventions](../../development-conventions.md)
  § *Whose thing earns a doc*. Naming `AbstractValidator<T>` in a rule of ours is the allowed case; documenting
  FluentValidation is not.
- must place a rule at the lowest layer that can hold it — a rule about `const` is layer 1, a rule about our `Constants`
  class is layers 2 and 3.

---

### Reading the map

A thing occupies one home per layer it has. Two tests, applied in order:

1. **Does C# or .NET ship the form?** → it has an `lla/constructs` row. Absent for a role we coined.
2. **Do we define a thing of our own on top of it?** → it earns an `mla/constructs` doc, and its conditions
   land in `mla/components` when it stands alone, or in `mla/domains` when it needs collaborators.

| Thing | `lla/constructs` — the C# form | `mla/constructs` — what ours **is** | Layer 3 — every condition |
|---|---|---|---|
| `Constants` | `const` · `static readonly` | the class as one value's authority | `mla/components/constants.md` |
| `Extensions` | extension method | the static tier over a **domain** | `mla/components/extensions.md` |
| `Enum` | `enum` | a closed option set we name | `mla/components/enums.md` |
| `Settings` | `record` · `init` | the record a section binds into | `mla/components/settings.md` |
| `Time` | `TimeProvider` | our clock seam | `mla/components/time.md` |
| `Json` | — | the `{Type}Json` storage seam | `mla/components/json.md` |
| `Entity` | — | a type that owns a row | `mla/domains/persistence/` |
| `Repository` | — | rows in, rows out | `mla/domains/persistence/access/` |
| `BackgroundService` | `BackgroundService` | work the host runs off the request path | `mla/platform/startup/` |

- must give every `mla/components` doc an `mla/constructs` doc — a component is layer 3 **of** something,
  and the thing it applies has to be defined somewhere.
- must not read a missing `lla` row as a missing layer — `Broker`, `Constants` and `Json` are roles we
  coined, so they start at layer 2.
- must not read a missing `mla/components` doc as a gap — a thing needing collaborators has its layer 3 in
  the domain that supplies them.
- must keep a variation out of `mla/constructs` — one-to-many is an application of `Entity`, so it lives
  wherever that entity's layer 3 lives.

---

## Building the SDK itself [REQUIRED]

These conventions feed **both** the products and the backend-beta SDK — naming, documentation, constructs and
components hold identically in either repo. What differs is the shape a repo takes, and only that.

| Question | A product answers | The SDK answers |
|---|---|---|
| architecture | Clean layers per service → [architecture](mla/architecture/architecture.md) | a library, no Application / Infrastructure / Persistence split |
| host | one `HostConfiguration` per service → [host configuration](mla/platform/startup/host-configuration.md) | none; it ships `Add*` extensions a host calls |
| what earns a doc | its own business logic | its own surface, plus the seams a product wires |

- must apply every naming, documentation and construct rule in the SDK repo unchanged — the SDK is ours,
  so a convention change reaches it as a row in that repo's sweep file, never as an exemption.
- must keep an SDK type's public surface documented as a product type would be — a consumer reads only the
  XML doc.
- must decide what belongs there through [extract / keep / remove](../../sdk-extraction.md), never here.
- must leave the SDK's own package layout and registry to its `docs/` — that is repo shape, not a convention.

> **Queued.** A `use-case/` · `core/` cut of this tree — `core/` for what holds everywhere, `use-case/` for the
> shapes that differ (service, contained library, monolith, microservices, SDK) — is the direction, not yet the
> layout. Today the difference is small enough for the table above.

---

## Layer direction [REQUIRED]

Rules flow `lla` → `mla` → `hla`. A higher layer may **override or extend** a lower one; a lower layer never reaches up.

- must state an override in the higher layer's own file, never by editing the lower layer's rule.
- must carry a **backlink** from the higher layer to the exact lower-layer rule it overrides or extends —
  `{file}` § *Section*, the way a component doc cites `lla/notation/`.
- must cite the lower layer rather than restate it when the higher layer adds nothing.
- must resolve a conflict in favour of the higher layer, and say so at the point of override.

---

## What each scope owns

### `lla/` — one symbol
Every rule that holds for **any** symbol, whatever kind it is: its name, its doc blocks, its member bodies, its file layout,
and the language constructs banned outright. A rule naming a *kind* of type is not `lla/`; a rule naming a technology is not `lla/`.

### `mla/` — one service
Five buckets. `constructs/` = the roles we define, one file per suffix. `components/` = the things complete on their own.
`architecture/` = where it lives, one folder per pattern, testing among the layers. `platform/` = how the service builds,
starts and answers. `domains/` = a concrete technology or use case, one folder each.

- **A component has one home layer.** A kind is declared, stored and documented in one layer even when used from others.
  A `Validator` reading `Options` composes with another component that has its own home; it does not straddle. `Service` is
  the one exception — as the fallback suffix it lands in Application or Infrastructure per instance.
- **A third party is a member of the domain that consumes it**, never its own axis. If the app cannot run without it, it is
  infrastructure, whoever wrote it.
- **The SDK boundary.** *How to use* and *what to use* from our own SDK is a convention and lives here; the SDK's internals
  live in the SDK's own docs.

### `hla/` — between our own services
Named ahead of its contents on purpose: without it, the first gateway or gRPC rule lands in `mla/platform/` and becomes a
single-service default every later service inherits by accident.

---

## Files

### `lla/` — language level

Three levels, and they never share a folder ([conventions](../../../conventions.md) § *One level per folder*).

| Level | Answers | Lives in |
|---|---|---|
| **construct** | what C# offers, and which of it we use or forbid — `record` · `class` · `interface` · `enum` · `struct` · `delegate` | [constructs/](lla/constructs/constructs.md) |
| **role** | what a construct may stand for — data or behavior, and the starter that follows | the `data/` · `behavior/` split under [constructs](mla/constructs/constructs.md) |
| **definition** | the whole thing — folder, file, type doc, construct, type name, members | each doc's own file, via the template |

**The role level fixes the starters.** A data model — `record`, `struct` — takes **Represents**. An interface over a data
model takes **Defines**. A behavior type takes its role's verb. A data model may carry behavior, but never complex
behavior: the moment a flow appears, the type has stopped being a model.

| Level | Folder | Holds |
|---|---|---|
| the construct | [constructs/](lla/constructs/constructs.md) | every C# construct, what each is for, construct-level bans · [event](lla/constructs/constructs.md) · [records](lla/constructs/constructs.md) |
| the self-sufficient thing | [components/](mla/components/components.md) | [constants](mla/components/constants.md) · [enums](mla/components/enums.md) · [extensions](mla/components/extensions.md) · [json](mla/components/json.md) · [settings](mla/components/settings.md) · [time](mla/components/time.md) |
| how it is written down | [notation/](lla/notation/notation.md) | [naming](lla/notation/naming/naming.md) · [documentation](lla/notation/documentation/documentation.md) · [style](lla/notation/style/style.md) |

The leaves those folders hold:

| File | What it covers |
|---|---|
| [statements](lla/constructs/statements.md) | Every statement and expression form, with a verdict |
| [indexers](lla/components/indexers.md) | `this[…]` — accessor starters, and what the key selects |
| [summary](lla/notation/documentation/summary.md) | `<summary>` — the mandated first word per type-kind, plus tone |
| [remarks](lla/notation/documentation/remarks.md) | `<remarks>` — never required; the ten frames |
| [params](lla/notation/documentation/params.md) | `<param>` — one per parameter, always |
| [typeparams](lla/notation/documentation/typeparams.md) | `<typeparam>` — carried when it can be got wrong |
| [returns](lla/notation/documentation/returns.md) | `<returns>` — required on every method that returns a value |
| [inline](lla/notation/documentation/inline.md) | `//` inside a body — the maintainer's doc, never shipped |
| [exceptions](lla/notation/documentation/exceptions.md) | `<exception>` — only what a method throws itself |

**Membership in `components/`** — a thing passes only when it is **complete with nothing else present**.
The gate is a demonstration: declare it in a program with nothing around it, and use it. An `Entity` fails, because it stays
inert until a store exists; a `Handler` fails without a dispatcher.
A thing that fails belongs in [`mla/constructs/`](mla/constructs/constructs.md), which names roles rather than whole things.

**Notation is a default set** — every rule there applies to every symbol, and a component may override it in its own file.
A component that does not override cites `notation/` rather than restating it.

### `mla/constructs/` — a role we define

Split by what the type is for: [data/](mla/constructs/data/data.md) holds,
[behavior/](mla/constructs/behavior/behavior.md) does.
The lead is [constructs](mla/constructs/constructs.md) — the suffix keep-list, the folds, and the coining gate.

| File | What it covers |
|---|---|
| [broker.md](mla/constructs/behavior/broker.md) | The app-side seam — broker/client peering, degradation policy, `Integrates` starter |
| [client.md](mla/constructs/behavior/client.md) | HTTP API wrappers — `HttpClient` injection, resilience pipeline (`AddSdkResilience`), Refit |
| [constructs](mla/constructs/constructs.md) | Component-type naming vocabulary — canonical suffix→role keep-list · synonym folds · banned junk-drawer · new-suffix gate |
| [controller.md](mla/constructs/behavior/controller.md) | Thin-dispatcher controllers — `ISender.SendAsync` + `AppResult.Match` |
| [registry.md](mla/constructs/behavior/registry.md) | The key-to-type set — binds at composition, throws on a miss |
| [mapper.md](mla/constructs/behavior/mapper.md) | The transform — total, stateless, both shapes named |
| [entity-configuration.md](mla/domains/persistence/access/ef/entity-configuration.md) | EF `IEntityTypeConfiguration<T>` mapping — `Configures` starter, `<inheritdoc />` on `Configure`, call order |
| [entity.md](mla/constructs/data/entity.md) | Entity records, `IKeyedEntity<TId>` PK contract, audit/soft-delete/tenant traits |
| [enums](mla/components/enums.md) | Enum naming, member ordering, `[Flags]` — the mapping is [postgres](mla/domains/persistence/database/postgres/postgres.md) |
| [background-service.md](mla/constructs/behavior/background-service.md) | Host-run work — `Runs` / `Schedules` starters, the loop and the one-shot shape |
| [application request](mla/constructs/data/application-request.md) | The dispatched `Query` / `Command` / `Event` — folder, starters, `{Domain}{Action}{Kind}` |
| [handler](mla/constructs/behavior/handler.md) | The receiver bound to one message — `Handles` starter, collaborators via the constructor |
| [policy](mla/constructs/behavior/policy.md) | The decision that governs another operation — `Decides` starter, `Policy` suffix |
| [adapter](mla/constructs/behavior/adapter.md) | A third-party type fitted to our interface, in-process — `Adapts` starter |
| [builder](mla/constructs/behavior/builder.md) | Stepwise construction ending in `Build()` — `Builds` starter |
| [repository.md](mla/constructs/behavior/repository.md) | Dapper, `IDbConnectionFactory`, `SqlNaming`, generic repositories |
| [api request](mla/constructs/data/api-request.md) | The `{Verb}{Noun}ApiRequest` body — folder, summary starter, suffix |
| [dto](mla/constructs/data/dto.md) | The wire projection — `{Entity}Dto`, entity-first and singular |
| [value object](mla/constructs/data/value-object.md) | Values stored inside an entity's row; identity is the values |
| [result.md](mla/constructs/data/result.md) | Result carriers — `Result`/`Result<T>` + `AppResult<TSuccess>` closed unions over one `AppError` |
| [service.md](mla/constructs/behavior/service.md) | Service / Client / Broker / Factory / Repository shape, lifetime + doc starters |
| [settings.md](mla/components/settings.md) | Settings records — `sealed record`, `init`-only, `IOptions<T>` binding |
| [validator.md](mla/constructs/behavior/validator.md) | Input validation — `IValidator<T>`, mediator validation behavior |

#### `patterns/` — a pattern named in the literature

| File | What it covers |
|---|---|
| [patterns](mla/constructs/patterns/patterns.md) | The catalogue — a verdict per pattern, and the doc gate |
| [adapters](mla/constructs/patterns/adapters.md) | Our contract satisfied by delegating to a foreign type |
| [ambient context](mla/constructs/patterns/ambient-context.md) | A per-request value flowing with the async context |
| [builders](mla/constructs/patterns/builders.md) | Configuration accumulated across calls, closed into one value |
| [circuit breaker](mla/constructs/patterns/circuit-breaker.md) | Stops calling a failing dependency for a while |
| [decorators](mla/constructs/patterns/decorators.md) | One implementation wrapped, a behavior added around the call |
| [factories](mla/constructs/patterns/factories.md) | Instances the container cannot resolve on its own |
| [null object](mla/constructs/patterns/null-object.md) | A contract satisfied by doing nothing |
| [outbox](mla/constructs/patterns/outbox.md) | A message staged in the state change's transaction, sent after commit |
| [pipelines](mla/constructs/patterns/pipelines.md) | Ordered steps wrapping one call, each calling the next |
| [prototype](mla/constructs/patterns/prototype.md) | A value copied and changed where it differs — `record` `with` |
| [proxies](mla/constructs/patterns/proxies.md) | A stand-in carrying calls to an implementation elsewhere |
| [sagas](mla/constructs/patterns/sagas.md) | A multi-step process undone by compensating each completed step |
| [service locator](mla/constructs/patterns/service-locator.md) | Banned — and the legitimate container references |
| [singleton](mla/constructs/patterns/singleton.md) | One instance per process, owned by the container |
| [state machines](mla/constructs/patterns/state-machines.md) | The states a lifecycle passes through |
| [strategies](mla/constructs/patterns/strategies.md) | Interchangeable implementations, chosen at composition |
| [template method](mla/constructs/patterns/template-method.md) | An abstract base fixing the order |
| [unit of work](mla/constructs/patterns/unit-of-work.md) | One transactional boundary per use case |

### `mla/components/` — a thing complete on its own

The lead is [components](mla/components/components.md) — the self-sufficiency gate.

| File | What it covers |
|---|---|
| [json](mla/components/json.md) | One type's persisted JSON seam — its options, its `Serialize` / `Deserialize` pair |
| [settings](mla/components/settings.md) | The config-bound record — `sealed record`, `nameof` binding, validate-on-start |
| [time](mla/components/time.md) | The clock seam — `TimeProvider`, `IClock`, zone resolution, cron parsing |

---

### `mla/architecture/` — where a type lives

One folder per architecture pattern. The lead states the solution grouping; the pattern states the layers.

| File | What it covers |
|---|---|
| [architecture](mla/architecture/architecture.md) | Pattern catalogue + solution-folder grouping (`services/ platform/ libraries/ tools/ tests/`) + `.slnx` encoding |
| [clean architecture](mla/architecture/clean/clean.md) | The six layers (Api / Application / Domain / Infrastructure / Persistence / Testing), dependency direction, deviations |
| [domain structuring](mla/architecture/clean/domain-structuring.md) | Subdomain pattern, `Core/` vs operation folders, role-group naming, default placement |
| [testing](mla/architecture/clean/testing.md) | E2E-first (Testcontainers + `WebApplicationFactory`, Respawn); unit for pure logic; harness mirrors the SDK scaffold |

### `mla/platform/` — how the service is built, started and answers

| File | What it covers |
|---|---|
| [api-context-building.md](mla/domains/api/api-context-building.md) | Sourcing caller context at the edge via `ICurrentUser` |
| [build.md](mla/platform/build/build.md) | Sub-domain lead — the two solution-root files, the minimal-`.csproj` invariant |
| [central-package-management.md](mla/platform/build/central-package-management.md) | `Directory.Packages.props` — CPM: one `PackageVersion` per package, `.csproj` refs by name (no `Version`); add/bump; SDK ref + `FrameworkReference` |
| [directory-build-props.md](mla/platform/build/directory-build-props.md) | `Directory.Build.props` — shared props (`net10.0` · `Nullable` · `ImplicitUsings` · `LangVersion latest`); opt-in warnings-as-errors + NuGet-audit stance; packaging props SDK-only |
| [host configuration](mla/platform/startup/host-configuration.md) | `HostConfiguration.Configure` + Extensions split, slim `Program.cs` |
| [known-endpoints.md](mla/platform/responses/known-endpoints.md) | Fixed identity / system endpoints — `api/identity/*`, `api/system/status` |
| [launch-profiles.md](mla/platform/startup/launch-profiles.md) | `launchSettings.json` — a single `https` profile, even/odd port pair from `ports.md` |
| [platform](mla/platform/platform.md) | The bucket lead — `build/` · `startup/` · `responses/` |
| [problem-details.md](mla/platform/responses/problem-details.md) | RFC 9457 error responses — `Problem()`, `IErrorHttpStatusCodeMapper`, global handler |
| [responses](mla/platform/responses/responses.md) | Sub-domain lead — one success shape, one error shape |
| [results.md](mla/platform/responses/results.md) | `AppResult<TSuccess>` — the outcome contract every layer returns |
| [serialization.md](mla/platform/responses/serialization.md) | JSON wire contract — camelCase props + **camelCase string enums** + null-omit + ISO dates; wired once in `AddControllers()` |
| [startup](mla/platform/startup/startup.md) | Sub-domain lead — how a host is composed, and what runs first |
| [startup-defaults.md](mla/platform/startup/startup-defaults.md) | `AddApiDefaults()` / `UseApiDefaults()` boot floor — what the bundle folds in, `ApiDefaultsOptions` tuning |
| [time.md](mla/components/time.md) | Time abstraction — `TimeProvider`, no `DateTime.Now` |

### `mla/domains/` — a capability, its contract and its providers

Each domain is one folder: the lead states the contract, and every technology-tied rule sits in its provider's folder.

| Domain | What it covers |
|---|---|
| [domains](mla/domains/domains.md) | The shape every domain follows, the built four, and the recognized five |
| [persistence](mla/domains/persistence/persistence.md) | Schema-first contract + the four axes: entities · database · access · migrations |
| [access](mla/domains/persistence/access/access.md) | How code reaches a row — EF tracked, Dapper untracked |
| [ef mapping](mla/domains/persistence/access/ef/ef-mapping.md) | `DbContext`, entity configurations, what never to configure |
| [dapper](mla/domains/persistence/access/dapper/dapper.md) | Connections, SQL conventions, type handlers, generic CRUD |
| [postgres](mla/domains/persistence/database/postgres/postgres.md) | Type mappings, numeric units, native enum types, column constraints |
| [database](mla/domains/persistence/database/database.md) | Engine lead — which engine, and what it fixes |
| [entity contracts](mla/domains/persistence/entities/entity-contracts.md) | Identity, audit, soft-delete, tenancy |
| [migration strategies](mla/domains/persistence/migrations/migrations.md) | Picking `Bespoke`, `Ef` or `DbUp` |
| [test databases](mla/domains/persistence/testing/test-databases.md) | The tier a test picks, and the provider switch |
| [ef](mla/domains/persistence/access/ef/ef.md) | Provider lead — the change tracker and the mapping |
| [ef migrations](mla/domains/persistence/migrations/ef/ef-migrations.md) | EF code-first migrations — `AddEfMigrationsRunner<TContext>` |
| [entity configuration](mla/domains/persistence/access/ef/entity-configuration.md) | EF `IEntityTypeConfiguration<T>` mapping — `Configures` starter, call order |
| [sql](mla/domains/persistence/migrations/sql/sql.md) | Provider lead — ordered scripts, and the tooling around them |
| [bespoke migrations](mla/domains/persistence/migrations/sql/bespoke-migrations.md) | Bespoke-SQL migrator — `AddDatabaseBespokeMigrations`, layout, drift |
| [migration dialects](mla/domains/persistence/migrations/sql/migration-dialects.md) | Writing Apply/Rollback SQL — quoting, rollback idioms, `@no-transaction` |
| [migration tooling](mla/domains/persistence/migrations/sql/migration-tooling.md) | `dotnet tool` CLIs — packaging, exit codes, destructive-op guard |
| [dbup migrations](mla/domains/persistence/migrations/dbup/dbup-migrations.md) | DbUp forward-only scripts — `AddDbUpRunner` |
| [dapper](mla/domains/persistence/access/dapper/dapper.md) | Provider lead — a connection and hand-written SQL |
| [messaging](mla/domains/messaging/messaging.md) | Dispatch contract, the in-process message set, and the transport providers |
| [mediator](mla/domains/messaging/mediator/mediator.md) | `ISender` / `IPublisher`, pipeline behaviors, registration |
| [identity](mla/domains/identity/identity.md) | The claim-set contract + `jwt/` · cookie · OAuth providers |
| [jwt auth](mla/domains/identity/jwt/jwt-auth.md) | JWT bearer — token issuance and validation wiring |
| [api](mla/domains/api/api.md) | The HTTP surface contract — action naming, attributes, content, response mapping |
| [api messages](mla/domains/api/api-messages.md) | Request naming, sub-blocks, the envelope, the edge mapping |
| [integrations](mla/domains/integrations/integrations.md) | The client/broker seam, and where degradation sits |
| [http](mla/domains/integrations/http/http.md) | Outbound HTTP — registration, resilience, cross-cutting handlers |
| [validation](mla/domains/validation/validation.md) | Phases, layer independence, rule codes, the HTTP mapping |
