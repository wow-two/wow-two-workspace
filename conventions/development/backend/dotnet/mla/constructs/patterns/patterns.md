# Patterns

*Last updated: 2026-08-16*

> Every design pattern a backend service meets, the form we write for it, and the doc or rule that governs it.
> Purpose — give a pattern one home, so its shape, naming and docs are settled once instead of per use.
> Use case — reach here when the thing being built is named after a pattern rather than after a layer role.

## Membership

- must be a pattern with a **settled name in the literature** — `Factory`, `Decorator`, `Adapter`, `Strategy`.
- must state what the pattern buys in this codebase, never what the book says it buys.
- must live in `mla/`, not `lla/`: a pattern needs collaborators to mean anything, so it fails the self-sufficiency
  gate ([lla components](../../../lla/components/components.md) § *The gate*).
- must not restate a component's rules — a pattern a component doc already owns is a row below, not a doc
  ([components](../constructs.md)).

---

## Doc gate

A pattern earns its own file only when **we write the type**. Everything else is a row carrying a verdict.

- must open a doc when the codebase declares the type and its shape, naming or docs need settling.
- must leave a row when a component doc, a domain doc or the framework already owns the pattern.
- must cite the rule that decides a non-`use` verdict as `{file}:{line}` or `{file}` § *Section* — a refusal with no
  cited rule is not a refusal, it is an opinion.
- must not open a doc for a pattern with no instance in the tree — a pattern doc records what we build, never
  what we might.

---

## Doc shape

- must carry `Shape` · `Use` · `Limits` · `Components`, in that order, after the description blockquote.
- must show one short C# fence in `Shape` — the form we write, not the book's UML.
- must name in `Components` every component the pattern touches, and stop there; the component's own rules stay there.
- must add the component template's `Location` · `Declaration` · `Content` when the pattern also names a keep-listed
  suffix — [factories](factories.md) is that case, and today the only one.
- must name the file for the pattern: plural when it names a type kind (`decorators.md`), singular when it names a
  policy or a flow (`outbox.md`).
- must follow the authoring rules in [conventions](../../../../../../conventions.md) § *Authoring a convention* for
  everything else — budget, headers, citation.

---

## Verdicts

Exhaustive across the four families below. A pattern we have never written is still listed, with a verdict.

- must read `use` as a pattern we write — the pattern name links its doc.
- must read `owned` as ruled by another doc, and read that doc instead — § *Owned elsewhere*.
- must read `folded` as a pattern an existing name already covers — § *Folds*.
- must read `banned` as never declared — § *Banned patterns* carries the rule that kills it.
- must read `open` as unruled — no instance and no rule yet, § *Open*.
- `Our form` names what we write for that need, including for a pattern we refuse.

---

## Creational

| Pattern | Our form | Verdict |
|---|---|---|
| [Factory Method](factories.md) | a `Factory` per dispatch axis, resolved from the container | `use` |
| [Builder](builders.md) | a fluent `{Thing}Builder` closing on `Build()` | `use` |
| [Singleton](singleton.md) | a container lifetime, never a static `Instance` | `use` |
| [Prototype](prototype.md) | `record` `with`, never `ICloneable` or `MemberwiseClone` | `use` |
| Abstract Factory | one `Factory` per axis, a `Registry` for the family | `folded` |
| Object Pool | one fresh connection per operation; the data source pools | `owned` |
| Lazy Initialization | `Lazy<T>` for one expensive field | `open` |

---

## Structural

| Pattern | Our form | Verdict |
|---|---|---|
| [Adapter](adapters.md) | a `{Foreign}Adapter` satisfying our contract with theirs | `use` |
| [Decorator](decorators.md) | the same interface, one collaborator wrapped | `use` |
| [Proxy](proxies.md) | a generated or interception-based stand-in | `use` |
| Bridge | a house contract, the engine pinned behind it | `folded` |
| Facade | a `Broker` facing outward, a `Service` facing inward | `folded` |
| Composite | a `Pipeline` and its ordered steps, never a uniform tree | `banned` |
| Flyweight | a plain reference type, allocation unmeasured | `banned` |

---

## Behavioral

| Pattern | Our form | Verdict |
|---|---|---|
| [Chain of Responsibility](pipelines.md) | an ordered pipeline, each step calling the next once | `use` |
| [State](state-machines.md) | a `SagaStateMachine<TState>` binding events to transitions | `use` |
| [Strategy](strategies.md) | one interface chosen at composition; the type is named for its role | `use` |
| [Template Method](template-method.md) | an abstract base fixing the order, hooks for the steps | `use` |
| Observer | `Handler` for a fact, `BackgroundService` for a poll | `folded` |
| Command | the CQRS `Command` and the one `Handler` bound to it | `owned` |
| Iterator | `yield return`, `IEnumerable<T>` / `IAsyncEnumerable<T>` | `owned` |
| Mediator | `ISender` / `IPublisher` dispatch over `IRequest` | `owned` |
| Visitor | a `switch` over a closed union, or `.Match` | `banned` |
| Memento | — | `open` |

---

## Enterprise

| Pattern | Our form | Verdict |
|---|---|---|
| [Unit of Work](unit-of-work.md) | the `DbContext` itself; no `IUnitOfWork` wrapper | `use` |
| [Outbox / Inbox](outbox.md) | rows staged in the business transaction, dispatched after | `use` |
| [Saga / Routing Slip](sagas.md) | `SagaStateMachine<TState>` orchestration, `EventSaga` for a slip | `use` |
| [Circuit Breaker / Retry](circuit-breaker.md) | one resilience pipeline, bound to the `Client` | `use` |
| [Ambient Context](ambient-context.md) | `AsyncLocal` tenant; time and actor injected | `use` |
| [Null Object](null-object.md) | a `NoOp{Capability}` at an infrastructure seam | `use` |
| Repository | rows in, rows out, hand-written SQL or generic CRUD | `owned` |
| CQRS | a `Query` or `Command` message, one handler each | `owned` |
| Registry | key → type bindings, complete or it throws | `owned` |
| Mapper | a total in→out transform owning no data | `owned` |
| Options | `Settings` bound from config, `Options` passed in code | `owned` |
| Result / Either | `Result<T>` and `AppResult<TSuccess>` closed unions | `owned` |
| Dependency Injection | constructor injection, wired once at the root | `owned` |
| Idempotency | `IIdempotent` plus the `IdempotencyBehavior<,>` step | `owned` |
| Publish / Subscribe | an event on the bus, 0..N handlers | `owned` |
| Claim Check | the payload stored out of band, a pointer on the message | `owned` |
| MVC | a thin controller dispatching to a handler | `owned` |
| [Service Locator](service-locator.md) | constructor injection, the composition root aside | `banned` |
| Specification | hand-written SQL, filtered in the query | `banned` |
| Event Sourcing | the row is the state; an event carries the fact | `banned` |

---

## Owned elsewhere

The pattern is real and in use; another doc is its authority, and this row only routes you there.

| Pattern | Ruled by | Reach for |
|---|---|---|
| Repository | `repository.md` § *No query abstraction* | hand-written SQL, or `DapperRepository<,>` |
| Object Pool | `repository.md` § *Connections* | `CreateOpenAsync` per operation |
| Iterator | `statements.md:37` | `yield return`, `IAsyncEnumerable<T>` |
| Command | `application-request.md` § *Type name* | `{Domain}{Action}Command` and its `Handler` |
| CQRS | `mediator.md` § *Common* | a `Query` or `Command`, one handler each |
| Mediator | `mediator.md` § *Registration & usage* | `ISender.SendAsync`, never concrete `Mediator` |
| Publish / Subscribe | `mediator.md` § *Events* | `IPublisher.PublishAsync`, 0..N handlers |
| Idempotency | `mediator.md` § *Pipeline behaviors* | `IIdempotent` + `IdempotencyBehavior<,>` |
| Registry | `registry.md` § *Members* | a `Registry` that throws on an unbound key |
| Mapper | `mapper.md` § *Members* | a total `Mapper`, handed every input |
| Options | `components.md` § *`Settings` vs `Options`* | `Settings` from config, `Options` in code |
| Result / Either | `result.md` § *Rules* | `AppResult<TSuccess>` collapsed with `.Match` |
| Dependency Injection | `constructs.md:229` | constructor injection |
| Claim Check | `outbox.md` § *Limits* | store the payload, stage the pointer |
| MVC | `controller.md` § *No business logic* | a controller that dispatches and maps |

---

## Folds

The pattern names a role an existing name already owns. Don't introduce the pattern's name; use the canonical one.

| Pattern | Canonical | Rule |
|---|---|---|
| Abstract Factory | a `Factory` per axis, a `Registry` for the family | `factories.md` § *Members* |
| Bridge | a house contract, adapters behind it | `swappable-modules.md:11` |
| Facade | `Broker` outward, `Service` inward | `components.md` § *Adding a new suffix* |
| Observer | `Handler`, or `BackgroundService` for a poll | `components.md` § *Folds* |

---

## Banned patterns

Never declared. The rule that kills each one is written elsewhere; this table names it and the replacement.

| Pattern | Killing rule | Reach for |
|---|---|---|
| Composite | `components.md` § *Folds* — `Node` → `PipelineStep` | a `Pipeline` and its ordered steps |
| Flyweight | `constructs.md:94` — allocation must be measured first | a plain reference type |
| Visitor | `result.md` § *Carriers* — `.Match` is the consume path | a `switch` over the closed union |
| Specification | `repository.md` § *No query abstraction* | SQL that filters, composed in the query |
| Service Locator | `constructs.md:229` | constructor injection ([service locator](service-locator.md)) |
| Event Sourcing | `database.md` § *Schema-first rule* | the row as state; an event carries the fact |

---

## Open

- **Memento** — no written rule anywhere in `lla/` or `mla/`, and no instance in the tree. Decide the verdict when
  an undo or draft-restore surface is first specified, not before.
- **Lazy Initialization** — `Lazy<T>` is a BCL type we instantiate, not a construct we declare, so
  [constructs](../../../lla/constructs/constructs.md) does not reach it. The verdict is this folder's to take:
  decide it against the container's own lifetimes, which already defer construction.
