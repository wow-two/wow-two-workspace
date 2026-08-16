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

| File | What it covers |
|---|---|
| [banned-constructs.md](lla/banned-constructs.md) | Language-level prohibitions in one list — `event`, `using static`, sync-over-async, positional data records |
| [code-organization.md](lla/code-organization.md) | One file per type, section dividers, parameter formatting, raw strings, SQL line length |
| [documentation.md](lla/documentation.md) | XML doc index — format, the three gates (convention → compaction → length), required tags, anti-patterns |
| [documentation/remarks.md](lla/documentation/remarks.md) · [params.md](lla/documentation/params.md) · [typeparams.md](lla/documentation/typeparams.md) · [returns.md](lla/documentation/returns.md) · [exceptions.md](lla/documentation/exceptions.md) | Per-block rules for the remaining XML doc tags |
| [documentation/summary.md](lla/documentation/summary.md) | **The canonical `<summary>` starter table** per type-kind + the falsifiability test; every other file links here |
| [idioms.md](lla/idioms.md) | Idiomatic C# sugar — method groups (`IDE0200`); room to grow (target-typed `new`, collection expressions) |
| [members.md](lla/members.md) | Member bodies — block `{ }` over expression `=>`, debuggability rationale |
| [models.md](lla/models.md) | Record style (`{ get; init; }`), member rules, naming |
| [naming.md](lla/naming.md) | Symbol naming — no brand/product prefix on types/members/extensions; predicates `Is`/`Has`/`Can`, never `Be` |

### `mla/components/` — a kind of type you declare

| File | What it covers |
|---|---|
| [broker.md](mla/components/broker.md) | The app-side seam — broker/client peering, degradation policy, `Integrates` starter |
| [client.md](mla/components/client.md) | HTTP API wrappers — `HttpClient` injection, resilience pipeline (`AddSdkResilience`), Refit |
| [components.md](mla/components/components.md) | Component-type naming vocabulary — canonical suffix→role keep-list · synonym folds · banned junk-drawer · new-suffix gate |
| [controller.md](mla/components/controller.md) | Thin-dispatcher controllers — `ISender.SendAsync` + `AppResult.Match` |
| [entity.md](mla/components/entity.md) | Entity records, `IKeyedEntity<TId>` PK contract, audit/soft-delete/tenant traits |
| [enum.md](mla/components/enum.md) | Enum naming, native PG enum mapping (`MapEnums`), string-conversion fallback |
| [repository.md](mla/components/repository.md) | Dapper, `IDbConnectionFactory`, `SqlNaming`, generic repositories |
| [request-model.md](mla/components/request-model.md) | `*ApiRequest` bodies + the edge mapping method to the application request |
| [response-model.md](mla/components/response-model.md) | `ApiResponse<T>` success envelope + DTO rules (`{Entity}Dto`) |
| [result.md](mla/components/result.md) | Result carriers — `Result`/`Result<T>` + `AppResult<TSuccess>` closed unions over one `AppError` |
| [service.md](mla/components/service.md) | Service / Client / Broker / Factory / Repository shape, lifetime + doc starters |
| [settings.md](mla/components/settings.md) | Settings records — `sealed record`, `init`-only, `IOptions<T>` binding |
| [validator.md](mla/components/validator.md) | Input validation — `IValidator<T>`, mediator validation behavior |

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
