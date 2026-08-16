# Conventions — Development — Backend (.NET)

*Last updated: 2026-08-16*

> .NET conventions for every backend service under `wow-two-ws/`. Lookup table — open a file when the task
> touches it; do not pre-read. Cut by **scope**: how far a rule reaches.
> How to write a doc here → template + rules in [../../../conventions.md](../../../conventions.md).

## The three scopes

| Scope | Reaches | Holds |
|---|---|---|
| `lla/` | one symbol | naming · doc blocks · members · idioms · banned constructs |
| `mla/` | one service, and everything it talks to | `components/` · `layers/` · `platform/` · `domains/` |
| `hla/` | between our own services | gateway · gRPC contracts · cross-service events · quotas |

**Routing.** A kind of type you declare → `mla/components/{kind}.md`. How any symbol is written → `lla/`.
Where a type lives → `mla/layers/`. How the service builds and starts → `mla/platform/`. A concrete
technology or use case → `mla/domains/{domain}/`. A rule spanning services we both own → `hla/`.

**The test between `mla/` and `hla/`:** do we own both ends? A third party is adapted in `mla/`, never contracted in `hla/`.
**The three levels, and where each lands.** A C# construct is `lla/shape/language-constructs.md`. A role's shape and its
documentation land wherever the rule reaches: **does it need a service around it?** No → `lla/` (`Constants`, `Extensions`).
Yes → `mla/components/` (`Entity`, `Controller`, `Broker`). A ban follows its rule — construct bans in `lla/`, role bans with the role.

**The test between baseline and a domain:** would the rule survive if the feature were deleted? Yes → baseline. No → the domain that owns it.

## What each scope owns

### `lla/` — one symbol
Every rule that holds for **any** symbol, whatever kind it is: its name, its doc blocks, its member bodies, its file layout,
and the language constructs banned outright. A rule naming a *kind* of type is not `lla/`; a rule naming a technology is not `lla/`.

### `mla/` — one service
Four buckets. `components/` = what am I building, one file per suffix. `layers/` = where it lives, the Clean-Arch projects
with testing among them. `platform/` = how the service builds, starts and answers. `domains/` = a concrete technology or
use case, one folder each.

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

## Files

### `lla/` — language level

Three levels, and they never share a folder ([../../../conventions.md](../../../conventions.md) § *One level per folder*).

| Level | Answers | Lives in |
|---|---|---|
| **construct** | what C# offers, and which of it we use or forbid — `record` · `class` · `interface` · `enum` · `struct` · `delegate` | [constructs/](lla/constructs/constructs.md) |
| **role** | what a construct may stand for — data or behavior, and the starter that follows | the `data/` · `behavior/` split, and [components.md](lla/components/components.md) |
| **definition** | the whole component — folder, file, type doc, type name, member doc, content | each component's own file, via the six-section template |

**The role level fixes the starters.** A data model — `record`, `struct` — takes **Represents**. An interface over a data
model takes **Defines**. A behavior type takes its role's verb. A data model may carry behavior, but never complex
behavior: the moment a flow appears, the type has stopped being a model.

| Level | Folder | Holds |
|---|---|---|
| the construct | [constructs/](lla/constructs/constructs.md) | every C# construct, what each is for, construct-level bans · [event](lla/constructs/event.md) · [records](lla/constructs/records.md) |
| the service-free role | [components/](lla/components/components.md) | [constants](lla/components/constants.md) · [extensions](lla/components/extensions.md) — the only two that pass the gate |
| how it is written down | [notation/](lla/notation/notation.md) | [naming](lla/notation/naming/naming.md) · [documentation](lla/notation/documentation/documentation.md) · [style](lla/notation/style/style.md) |

**Membership in `components/`** — a role passes only when it owns **both its shape and its role with no service around it**.
The gate is a demonstration: show it declared *and used* in a program that has no services. An `Entity` fails, because an entity
is a model and a model needs a store and a domain. An `enum` fails, because any role an enum plays gathers logic around it.
A role that fails belongs in [`mla/components/`](mla/components/components.md).

**Notation is a default set** — every rule there applies to every symbol, and a component may override it in its own file.
A component that does not override cites `notation/` rather than restating it.

### `mla/components/` — a kind of type you declare

Split by what the type is for: [data/](mla/components/data/entity.md) holds, [behavior/](mla/components/behavior/service.md) does.
The lead is [components.md](mla/components/components.md) — the suffix keep-list, the folds, and the coining gate.

| File | What it covers |
|---|---|
| [broker.md](mla/components/behavior/broker.md) | The app-side seam — broker/client peering, degradation policy, `Integrates` starter |
| [client.md](mla/components/behavior/client.md) | HTTP API wrappers — `HttpClient` injection, resilience pipeline (`AddSdkResilience`), Refit |
| [components.md](mla/components/components.md) | Component-type naming vocabulary — canonical suffix→role keep-list · synonym folds · banned junk-drawer · new-suffix gate |
| [controller.md](mla/components/behavior/controller.md) | Thin-dispatcher controllers — `ISender.SendAsync` + `AppResult.Match` |
| [entity.md](mla/components/data/entity.md) | Entity records, `IKeyedEntity<TId>` PK contract, audit/soft-delete/tenant traits |
| [enum.md](lla/components/enums.md) | Enum naming, native PG enum mapping (`MapEnums`), string-conversion fallback |
| [repository.md](mla/components/behavior/repository.md) | Dapper, `IDbConnectionFactory`, `SqlNaming`, generic repositories |
| [request-model.md](mla/components/data/request-model.md) | `*ApiRequest` bodies + the edge mapping method to the application request |
| [response-model.md](mla/components/data/response-model.md) | `ApiResponse<T>` success envelope + DTO rules (`{Entity}Dto`) |
| [result.md](mla/components/data/result.md) | Result carriers — `Result`/`Result<T>` + `AppResult<TSuccess>` closed unions over one `AppError` |
| [service.md](mla/components/behavior/service.md) | Service / Client / Broker / Factory / Repository shape, lifetime + doc starters |
| [settings.md](mla/components/data/settings.md) | Settings records — `sealed record`, `init`-only, `IOptions<T>` binding |
| [validator.md](mla/components/behavior/validator.md) | Input validation — `IValidator<T>`, mediator validation behavior |

### `mla/layers/` — where a type lives

| File | What it covers |
|---|---|
| [domain-structuring.md](mla/layers/domain-structuring.md) | Subdomain pattern, `Core/` vs operation folders |
| [layers.md](mla/layers/layers.md) | Solution-folder grouping + 5-layer Clean Arch (Api / Application / Domain / Infrastructure / Persistence) |
| [test-databases.md](mla/layers/test-databases.md) | Test-DB selection — tiers (`RelationalTestDb<TContext>` · `MultiHostFixture` · `MigratorHarness`), Postgres default, `WOW2_TEST_DB` switch + SQLite speed fallback |
| [test-databases.md](mla/layers/test-databases.md) | Test-DB tiers — container vs shared, Respawn reset boundaries |
| [testing.md](mla/layers/testing.md) | E2E-first (Testcontainers + `WebApplicationFactory`, Respawn); unit for pure logic; harness mirrors the SDK scaffold |

### `mla/platform/` — how the service is built, started and answers

| File | What it covers |
|---|---|
| [api-context-building.md](mla/platform/api-context-building.md) | Sourcing caller context at the edge via `ICurrentUser` |
| [build.md](mla/platform/build/build.md) | Sub-domain lead — the two solution-root files, the minimal-`.csproj` invariant |
| [central-package-management.md](mla/platform/build/central-package-management.md) | `Directory.Packages.props` — CPM: one `PackageVersion` per package, `.csproj` refs by name (no `Version`); add/bump; SDK ref + `FrameworkReference` |
| [directory-build-props.md](mla/platform/build/directory-build-props.md) | `Directory.Build.props` — shared props (`net10.0` · `Nullable` · `ImplicitUsings` · `LangVersion latest`); opt-in warnings-as-errors + NuGet-audit stance; packaging props SDK-only |
| [host-configuration.md](mla/platform/host-configuration.md) | `HostConfiguration.Configure` + Extensions split, slim `Program.cs` |
| [known-endpoints.md](mla/platform/known-endpoints.md) | Fixed identity / system endpoints — `api/identity/*`, `api/system/status` |
| [launch-profiles.md](mla/platform/launch-profiles.md) | `launchSettings.json` — a single `https` profile, even/odd port pair from `ports.md` |
| [problem-details.md](mla/platform/problem-details.md) | RFC-7807 error responses — `Problem()`, `IErrorHttpStatusCodeMapper`, global handler |
| [serialization.md](mla/platform/serialization.md) | JSON wire contract — camelCase props + **camelCase string enums** + null-omit + ISO dates; wired once in `AddControllers()` |
| [startup-defaults.md](mla/platform/startup-defaults.md) | `AddApiDefaults()` / `UseApiDefaults()` boot floor — what the bundle folds in, `ApiDefaultsOptions` tuning |
| [time.md](mla/platform/time.md) | Time abstraction — `TimeProvider`, no `DateTime.Now` |

### `mla/domains/` — instances of the baseline

| File | What it covers |
|---|---|
| [jwt-auth.md](mla/domains/identity/jwt-auth.md) | JWT bearer auth — token issuance + validation wiring |
| [mediator.md](mla/domains/messaging/mediator.md) | In-process request/response + fan-out — `IRequest`/`INotification`, CQRS query/command naming, `ISender`/`IPublisher`, pipeline behaviors |
| [database.md](mla/domains/persistence/database.md) | Schema-first rule (canonical = `Migrations/*/Apply.sql` for Sql-strategy), column constraints, type mappings, EF-as-mapper |
| [bespoke-migrations.md](mla/domains/persistence/migrations/bespoke-migrations.md) | Bespoke-SQL migrator — components + lifecycle (provider-agnostic): `AddDatabaseBespokeMigrations`, layout, drift/orphan |
| [dbup-migrations.md](mla/domains/persistence/migrations/dbup-migrations.md) | DbUp forward-only scripts — `AddDbUpRunner` |
| [ef-migrations.md](mla/domains/persistence/migrations/ef-migrations.md) | EF Core code-first migrations — `AddEfMigrationsRunner<TContext>` |
| [migration-dialects.md](mla/domains/persistence/migrations/migration-dialects.md) | Writing Apply/Rollback SQL — dialect rules (Postgres): quoting, rollback idioms, `@no-transaction` |
| [migration-tooling.md](mla/domains/persistence/migrations/migration-tooling.md) | `dotnet tool` CLIs — packaging, exit codes, destructive-op target guard, secret hygiene |
| [migrations.md](mla/domains/persistence/migrations/migrations.md) | Strategy index — pick `Ef` / `DbUp` / `Sql` (default) + shared concepts |
