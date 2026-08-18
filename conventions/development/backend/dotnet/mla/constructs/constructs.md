# Constructs

*Last updated: 2026-08-18*

> The canonical suffix→role vocabulary for backend types — one name per role, the suffix declaring the responsibility.
> Purpose — when `Store`, `Repository` and `Provider` all mean data access, a reader cannot infer role from a name.
> Use case — naming any backend type; check the keep-list before coining, run the gate before adding.

## How to use

- must pick the suffix whose **role** matches what the type does — a suffix is a contract, not decoration.
- must rename to the canonical when the name you reached for appears in § *Folds*.
- must run § *Adding a new suffix* when no existing suffix fits.
- must leave *how* a role behaves to the cited authority — this doc is the vocabulary.
- framework-named types (`Middleware` · `Filter` · `Interceptor`) are exempt; the framework owns the name.

---

## Rename cost [REQUIRED]

- must not weigh rename cost when deciding a name — decide what is correct, rename everything carrying the old one.
- must not keep a wrong name because it is established, shipped, or used in another repo.
- must treat the vocabulary as iterable — a name settled last month gets re-settled the moment a better one is argued.
- must refuse a name for duplicating a role, never for the work of renaming; **saturation** is the real cost.

A rename that builds and passes is done — the compiler and the tests are the whole safety argument.

---

## Keep-list

One suffix per role. Where another doc owns the role, that doc is the **authority** and this row is the index.
Split by what the type is for — [data](data/data.md) holds, [behavior](behavior/behavior.md) does.

| Suffix | Role | Authority |
|---|---|---|
| `Service` | business logic, orchestration, compute — the default when no narrower role fits | [service](behavior/service.md) |
| `BackgroundService` | long-running work off the request path, polling or draining on a timer | [hosted service](behavior/hosted-service.md) |
| `HostedService` | one-shot work at host start or stop | [hosted service](behavior/hosted-service.md) |
| `Client` | one external provider's call surface, out-of-proc | [client](behavior/client.md) |
| `Broker` | the app-side seam over an external dependency | [broker](behavior/broker.md) |
| `Repository` | data access — rows in, rows out | [repository](behavior/repository.md) |
| `Factory` | runtime instance creation, per key or per request | [factories](patterns/factories.md) |
| `Registry` | key → type or capability bindings, registered at composition | [registry](behavior/registry.md) |
| `Tracker` | live status many producers push into, persisted nowhere | — |
| `Extensions` | the static-logic tier over a domain — no injection, no state | [extensions](../components/extensions.md) |
| `Handler` | the receiver of one dispatched message | [handler](behavior/handler.md) |
| `Command` · `Query` · `Event` | a dispatched use case — write, read, fan-out | [application request](data/application-request.md) |
| `Validator` | input validation for one request | [validator](behavior/validator.md) |
| `Controller` | the HTTP delivery surface — a thin dispatcher | [controller](behavior/controller.md) |
| `ApiRequest` | the API edge body one controller action binds | [api request](data/api-request.md) |
| `ApiResponse` | the success envelope a client reads `.data` from | [api messages](../domains/api/api-messages.md) |
| `Dto` | a projection onto the wire — data, never behavior | [dto](data/dto.md) |
| `Entity` | a table-mapped row, owning its identity | [entity](data/entity.md) |
| `ValueObject` | values stored inside a row; identity is the values | [value object](data/value-object.md) |
| `Result` | an operation's outcome — a typed success or an `AppError` | [result](data/result.md) |
| `Adapter` | a third-party type fitted to an interface we declared | [adapter](behavior/adapter.md) |
| `Builder` | stepwise construction, ending in `Build()` | [builder](behavior/builder.md) |
| `Policy` | decides whether, when, or how often another operation runs | [policy](behavior/policy.md) |
| `Settings` | a config section bound through `IOptions<T>` | [settings](../components/settings.md) |
| `Options` | behavior knobs passed in code, bound from nothing | § *`Settings` vs `Options`* |
| `DbContext` | the EF unit of work | [database](../domains/persistence/database/database.md) |
| `Configuration` | an EF `IEntityTypeConfiguration<T>` | [entity configuration](../domains/persistence/access/ef/entity-configuration.md) |
| `Constants` | a holder of `const` and `static readonly` values | [constants](../components/constants.md) |
| `Mapper` | any deterministic in→out transform, owning no data | [mapper](behavior/mapper.md) |
| `Pipeline` · `PipelineStep` | an ordered multi-step flow, and one step of it | [pipelines](patterns/pipelines.md) |
| `Middleware` · `Filter` · `Interceptor` | a framework hook — exempt from the gate | — |
| `Cipher` · `Hasher` · `Issuer` · `Authenticator` | one cryptographic or auth operation | — |
| `Renderer` | turns a model into a representation of it — text, markup, an image | — |
| `Generator` | derives a value from its inputs — an id, a code, a matrix | — |
| `Rasterizer` | vector → pixels | — |
| `Spec` | a declarative input shape a renderer consumes — not a wire `Dto` | — |
| `Json` | one type's persisted JSON seam — its `Options` plus `Serialize` / `Deserialize` | [json](../components/json.md) |
| `Enum` | a closed set of named options | [enums](../components/enums.md) |

**Scope.** Every suffix here names a type inside a .NET service. A browser-side type is a wire projection of one, so it
carries none of them; what the frontend calls its own types is [the frontend's](../../../../frontend/frontend-conventions.md).

---

## `Mapper` vs `Registry`

Both answer "given X, give me Y". The line is who owns the mapping data.

- must use `Mapper` when the data arrives as an argument — pure, no injection, no I/O, nothing stored.
- must use `Registry` when callers register into it and it owns whether the set is whole.
- must use `Service` or `Broker` instead when the lookup needs injected collaborators or I/O.
- must not call it a `Registry` when nothing registers — a table read from config is a `Mapper` handed its data.

`Registry` holds **types and capabilities**; `Repository` holds **instances**. An in-memory `Repository` is still one.

| | `Registry` | `Repository` |
|---|---|---|
| Holds | key → type or capability | instances of an entity |
| Entries appear | at composition, in code | at runtime, from user or system action |
| A lookup gives you | something to dispatch to | something to read or write |

---

## `Client` vs `Broker`

Both reach an external system. The line is whose vocabulary the type exposes.

- must use `Client` when the surface is the provider's own — its types, its call set, nothing of ours.
- must use `Broker` when the surface is ours, whatever it calls underneath.
- the test: would the surface change if the provider were swapped? no → `Client`; yes → `Broker`.
- either may exist alone; a `Broker` may sit over a `Client`, a vendor SDK, or a raw `HttpClient`.

---

## `Settings` vs `Options`

- must use `Settings` when the config binder populates it from `appsettings.json`.
- must use `Options` when a caller supplies it in code — a delegate, or `new`.

---

## Folds

Each left-hand suffix names a role an existing suffix already owns. Rename to the canonical; never introduce the synonym.

| Synonym | Canonical | Why |
|---|---|---|
| `Store` | `Repository` | both are rows in, rows out against a backing store |
| `Gateway` | `Broker` | a gateway to an external system is the app-side seam |
| `Provider` | `Service` | every service provides something; the word adds nothing |
| `Node` | `PipelineStep` | a node means nothing outside the pipeline it steps through |
| `Encryptor` | `Cipher` | `Cipher` is the established crypto-primitive suffix |
| `Mapping` · `Profile` | `Mapper` | the type maps; `Profile` is AutoMapper's base type, not a role |
| `Normalizer` | `Mapper` | `T → T` is a transform; idempotence is a property, not a role |
| `Map` | `Mapper` | the type is a function, and `Map` reads as data |
| `Resolver` | `Mapper` · `Broker` · `Service` | pure → `Mapper`; out-of-process → `Broker`; injected collaborators → `Service` |
| `Emitter` | `Renderer` | emitting a representation of a model is rendering it |
| `Source` | `Generator` | a type that derives a value generates it |
| `Observer` | `Handler` · `BackgroundService` | reacting is a handler's verb; polling on a timer is a hosted service |
| `Scheduler` | `BackgroundService` | a poller schedules nothing, it runs |
| `Keeper` | `Service` | a synonym for a stateful service |

- must keep a framework's own name as it ships — a fold governs only names we choose.
- must name a pure `static class` as one of three — `Constants` for values, `Extensions` for logic over a domain,
  `Mapper` for a transform. There is no fourth static form, and a bare noun (`SqlNaming`, `Geohash`) is none of them.
- must keep `Source` where it names a content origin read from, not a value derived — `IMigrationSource`.

---

## Banned

Each names *nothing* — it describes "a class that does stuff". The gate points at the real role.

| Banned | Why | Reach for |
|---|---|---|
| `Manager` | "manages" = unspecified work | `Service` · `Registry` · `Tracker` |
| `Helper` | a dumping ground for orphan statics | `Extensions`, or fold into its owner |
| `Util` · `Utils` | `Helper`, vaguer | `Extensions` |
| `Accessor` | "accesses" = reads — say what | `Repository` · `Client` · `Service` |
| `Engine` | an important-sounding `Service` | `Service`, or `Pipeline` for a flow |
| `Strategy` | names swappability, which is a shape rather than a responsibility | `Policy` · `Mapper` · `Service` |

---

## Adding a new suffix [REQUIRED]

Answer in order; the first **yes** picks the suffix, and coining requires four `no`s.

1. does it call out-of-process? → `Client` or `Broker`.
2. does it persist or read rows? → `Repository`.
3. does it only supply configuration? → `Settings` or `Options`.
4. is it pure compute or orchestration with no narrower role? → `Service`.

- must coin only for a role no existing suffix covers — a distinct verb, never a synonym.
- must not coin inline; a name that misses is copied forward by every later scaffold.
- must state the role's verb in one line — no verb to state means it is a `Service`.
- must name the nearest two suffixes and why each fails — failing against none means it folds.
- must bring both to the developer and wait; only a confirmed suffix is implemented.

Rapid scaffolding raises this bar rather than lowering it — scaffolding replicates an unconfirmed name fastest.

---

## Adding a component [REQUIRED]

A confirmed suffix earns a keep-list row and a doc in the same pass. The doc states the **baseline** — what the type is,
wherever it is used. Whatever varies by technology or by flow belongs to the domain that uses it.

- must give each component one file, named for the suffix it defines — `mapper.md` for `Mapper`.
- must carry the `##` sections in order — `Location` · `Declaration` · `Content`; omit a section rather than rename it.
- must name the folder as the **plural of the suffix** — `Mapper` → `Mappers/`, `Entity` → `Entities/`.
- must state only the folder **name**, never its layer ([domain structuring](../architecture/clean/domain-structuring.md)).
- must not state a technology, a registration, or an end-to-end flow — a [domain](../domains/) owns those.
- must cite [notation](../../lla/notation/notation.md) rather than restate a default it does not override.
- must land before the first implementation — an unwritten baseline is what lets `Normalizer` ship beside `Mapper`.
- may close with `## Neighbours` — links out, one line each, carrying no rules.

| Section | Sub-headings | States |
|---|---|---|
| Location | Folder · File | the folder name that wraps it, and the file's name |
| Declaration | Type doc · Construct · Type name | the doc fields, the form declared, and the name |
| Content | Member docs · Members | the members, when this doc is what fixes them |

- must omit `Content` when the shape belongs elsewhere — the SDK for a type it declares, the domain for the rest.
- must carry `Content` when the members **are** the contract, as a [component](../components/components.md) does.
- must give the construct its own `### Construct` sub-heading — `sealed record`, `sealed class`, `static class`.
- must keep a member fact out of `Type name` — `init`-only and `required` are the construct's, ruled at
  [lla constructs](../../lla/constructs/constructs.md) § *Data components*.
- must state under `Type name` only what governs the **name**: the suffix, the prefix, the ordering, the ban.

````markdown
# {Components}

*Last updated: {YYYY-MM-DD}*

> {One line saying what the role is.}
> Purpose — {what having it buys}.
> Use case — {when to reach for it}.

## Location

### Folder
- must {rule}

### File
- must {rule}

---

## Declaration

### Type doc

#### [Summary](../../lla/notation/documentation/summary.md)
- must {rule}

```csharp
// ✅
{good}
// ❌ {why it fails}
{bad}
```

### Type name
- must {rule}
````

[The component template](../components/components.md) § *Adding a component* keeps a third `Content` section, because a
component is self-sufficient: its members are the whole contract, and no domain exists to own them.

---

## Authoring this doc

- must stay vocabulary and role, never prose — cite the authority instead of restating its rules.
- must list what we **recognize**, not what has shipped — a role earns a row before any type carries it.
- must cite a real symbol in an example, and carry no example at all for a recognized-but-unbuilt role.
