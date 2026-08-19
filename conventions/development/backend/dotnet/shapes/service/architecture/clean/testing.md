# Testing

*Last updated: 2026-08-18*

> The sixth [layer](clean.md) — its projects, its tiers, and how a test is named. Its own `tests/` solution folder.
> Purpose — end-to-end over unit: run the real flow, mock as little as can be run for real.

## Principle

- a service with **few external dependencies** → test it **end-to-end**.
  - real HTTP through the real pipeline, against a **real database**.
  - mock nothing you can run for real.
- reserve **unit tests** for **pure, I/O-free logic** — evaluators, formatters, generators.
  - fast, deterministic, no host/DB.
- handlers/repos are thin, so isolating them over an in-memory DB exercises little.
  - it hides provider-specific, serialization, auth and ownership bugs.
  - one E2E test covers the same logic **plus** the wiring, and the cross-service flows units can't see.

---

## E2E / integration stack

- **runner** — xUnit.
- **host** — `WebApplicationFactory<Program>` (in-proc), one per host.
  - multi-host flows build several on one DB.
- **DB** — **Testcontainers** real engine (e.g. `postgres:N-alpine`).
  - **never** SQLite / in-memory for the integration layer — dialect drift hides bugs.
- **reset** — **Respawn** between tests, **excluding the migration-history table**.
- **assertions** — one fluent lib (AwesomeAssertions).
- **time** — `FakeTimeProvider` for time-dependent paths.

- **one shared container** per suite (collection fixture); non-parallel within the collection.
- migrations **auto-apply on host startup** — no separate migrate step.
- inject the container connection string via config/env override; all hosts point at the same DB.
- **only stub genuinely-external 3rd-party APIs** — a WireMock fixture.
  - in-proc components (codegen, detectors, queues) run for real.
- **async work** (background flushers/queues): assert via **poll-with-timeout**, never a fixed `Task.Delay`.
- **Docker required** locally + in CI — this is the pre-ship gate.

---

## Coverage

Per feature, cover success **and** the edges — `401` auth, `404` ownership with **no existence leak**,
validation, invariants.
Automating the edges leaves the **frontend to smoke-test the happy path only**.

---

## Layout

- tests live in a `tests/` folder in the backend solution.
- **test projects are named `{Product}.Tests.{Type}`** — every one sits under a shared `.Tests.` prefix.
  - `Type` ∈ {`Unit`, `Integration`, `E2E`}, one project per tier that has tests:
  - **`{Product}.Tests.Unit`** — pure, I/O-free logic; no host, no DB, Docker-free.
    - evaluators, formatters, generators, validators in isolation.
  - **`{Product}.Tests.Integration`** — real DB / infra **below** the HTTP pipeline.
    - a repository or handler over a real `DbContext`.
  - **`{Product}.Tests.E2E`** — the full API over HTTP via host-boot; real Postgres, real pipeline.
    - the **primary tier** — push request-flow coverage here.
    - it catches serialization / mediator / model-binding / filter failures that green handlers miss.
    - ships a `README.md` noting the Docker prerequisite + coverage.
- a **descriptive `{Type}`** is allowed for a specialized suite that doesn't fit the three tiers.
  - e.g. **`{Product}.Tests.Migrations`** for migrator-engine tests.
  - keep it a single noun naming the suite's subject.
- **the bare `{Product}.Tests` name is disallowed** — it is ambiguous about its type.
  - create a `{Product}.Tests.{Type}` project instead.
- the tier maps 1:1 to the DB-selection tiers in
  [test databases](../../../../core/mla/domains/persistence/testing/test-databases.md).
  - `Tests.Unit` → pure-logic, no DB.
  - `Tests.Integration` → repository / handler (`RelationalTestDb<TContext>`).
  - `Tests.E2E` → host-boot (`MultiHostFixture` + `PostgresFixture`).
- existing apps (`SmartQr.*`, `SecretsVault.*`) are being renamed to match; stragglers get retrofitted.

---

## Method naming

Pattern — `{Unit}_Should{Expectation}[_When{Condition}]`.
PascalCase segments; the `_` separates the three parts, never words.
Reads as a sentence: *"{unit} should {expectation} when {condition}"*.

- **`{Unit}`** — the action / method / behaviour under test: `Create`, `GetById`, `Attempt`, `Classify`.
- **`Should{Expectation}`** — the asserted outcome.
  - integration → `ShouldReturn{Status}` (`ShouldReturn404`).
  - unit → `Should{Behaviour}` (`ShouldReturnCanceled`, `ShouldThrow`).
- **`When{Condition}`** — the scenario under test.

| | Rule |
|---|---|
| must | three-part `_Should…_When…`, PascalCase each segment |
| must | integration names state the HTTP status (`ShouldReturn201`, `ShouldReturn422`) |
| must | the `When` describes behaviour / state, never implementation |
| may | drop `_When…` only when the behaviour is unconditional |

- **integration (E2E)** — `{Action}_ShouldReturn{Status}_When{Condition}`.
  - `Create_ShouldReturn422_WhenMedicationDoesNotExist`
- **unit (pure logic)** — `{Method}_Should{Outcome}_When{Condition}`.
  - `Attempt_ShouldReturnCanceled_WhenOperationCanceled`
- **unconditional** — `{Method}_Should{Outcome}`.
  - `Flatten_ShouldCapDepthAtFive`

✅ `GetById_ShouldReturn404_WhenRecordDoesNotExist` · `Classify_ShouldBeTransient_WhenDbTimeout`
❌ `Attempt_converts_cancellation_to_canceled` (snake, no Should/When) · `Test_Create` · `Should_Work`

---

## Harness extraction

The **generic** E2E harness — host factory, container fixtures, base classes — **mirrors the backend-beta SDK
testing scaffold** (`WebApiTestHost<T>`, `WebApiTestBase<T>`, `PostgresFixture`, `IAsyncTestFixture`, …)
with API-identical signatures, so it lifts into the SDK mechanically.
**Product-coupled** fixtures stay in the product test project — the app's specific multi-host wiring,
auth helper, DTO mirrors.

Reference implementation: `smart-qr-poc/.../backend/SmartQr.Tests.Integration`.

---

## Ownership

A testing rule specific to a domain belongs **inside that domain**, never here. This doc keeps only what holds
whatever the feature is.

- must keep here: the `tests/` layout, the three tiers, method naming, and the shared harness.
- must file a fixture with the domain it exercises.
  - a database fixture with [persistence](../../../../core/mla/domains/persistence/persistence.md).
  - a bus fixture with messaging, an auth helper with identity.
- must not add a domain's fixture rules here to keep them together — a provider-specific fixture differs per provider.
- must let each domain's own doc carry its testing section, and cite it rather than restating it.

---

## Open

- **Test documentation is unruled.** A test carries no `<summary>` and no `<remarks>`
  ([remarks](../../../../core/lla/notation/documentation/remarks.md) § *Never required*), so nothing states in human language
  what a test covers at a glance. Two halves to settle together, after research:
  - the **AAA comment format** — how arrange, act and assert are marked inside a test body.
  - where the test's **gist** lives, given the name carries the case and no doc block is allowed.
- Deferred deliberately; the naming rules above stand in the meantime.
