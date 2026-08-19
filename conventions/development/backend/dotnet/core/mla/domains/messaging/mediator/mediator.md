# Mediator

*Last updated: 2026-08-15*

> The in-process request/response mediator — its message kinds, their handlers, and the pipeline around them.
> Purpose — decouple presentation from infrastructure so a use case is dispatched, not called directly.
> Use case — between the presentation and infrastructure layers; not infrastructure-to-infrastructure calls.

## Queries, Commands, Events and their Handlers

### Common

- a **query, command and event are all request messages** — declared, named and handled separately.
- query = read · command = write · event = fan-out fact ("X happened").
- **Naming** — `{Domain}{Action}[{Meta}]{Kind}`, **domain-first, singular**.
- singular — `Code`, `Product`, `Channel`, never `Codes`.
- the domain prefix sorts related types together; the action mirrors the controller method stem.
- **Shape** — messages = `public sealed record` carrying inputs as members; handlers = `public sealed class`.
- **Cardinality** — a query and a command have **exactly one** handler each; an event has **0..N**.
- SDK markers rebase onto `IRequest` / `INotification`.
- SDK handler interfaces refine `IRequestHandler` / `INotificationHandler`.
- same DI scan, same pipeline, no extra wiring.
- **Result** — a result-carrying request returns `AppResult<TSuccess>` as its `TResult`.
- construction, shape and `.Match` collapse in [result-pattern.md](../../../constructs/data/result.md).
- cannot-fail — a value type directly (query), or no value (`ICommand`, returns `Unit`).

### Query

- **Marker** — `IQuery<TResult>` (invariant — result type fixed per query)
- **Handler** — `IQueryHandler<TQuery,TResult>`
- **Verb** — `GET`
- **Location** — `Application/{Domain}/Queries/`
- **Example** — `CodeGetByIdQuery`

### Command

- **Markers** — `ICommand` (no value) / `ICommand<TResult>` (value)
- **Handlers** — `ICommandHandler<TCommand>` / `ICommandHandler<TCommand,TResult>`
- **Verbs** — `POST` `PUT` `PATCH` `DELETE`
- **Location** — `Application/{Domain}/Commands/`
- **Examples** — `CodeSetActiveCommand` (no value) · `CodeCreateCommand` (value)

### Events

> Document now, deferred use — uses what the SDK mediator already offers.

- **Marker** — `INotification`
- **Handler** — `INotificationHandler<TEvent>` (0..N)
- **Raised via** — `IPublisher.PublishAsync` — sequential, registration order; a throwing handler aborts the rest
- **Location** — `Application/{Domain}/Events/`
- **Example** — `CodeCreatedEvent` (naming `{Domain}{Action}Event`)

### Comments

XML doc summaries — byte-identical to the SDK marker source.

- **Definition** (SDK marker / handler interface) → `Defines …`, keeping the `<typeparam>` lines.
- e.g. `Defines a query that returns TResult` · `Defines a handler for the TQuery query`.
- **Message** (concrete query/command/event) → `Represents a {query/command/event} to {action}`.
- e.g. `Represents a query to get all channels`.
- **Handler** (concrete) → `Handles <see cref="{Request}"/>.`

---

## The application request

> **Application request** — the mediator message a handler executes: a `Command` or a `Query`.
> It maps in from the presentation **api request** — the body ([api messages](../../api/api-messages.md)) — plus
> caller context.

- **Inputs ride the application request; collaborators come from DI.**
- replay test — *could a cold handler run it off a queue?* If yes it is an **input** → on the request.
- repos, clock, brokers are **collaborators** → handler ctor (DI), never inputs.
- **Caller context is an input** — the actor (`UserId`), source IP are server-authoritative, and ride the request.
- the handler never reads them from `ICurrentUser` / `HttpContext`.
- source them at the edge, merged in the mapping — never by a pipeline.
- it is still a `Command` / `Query` — **application request** is the role it plays opposite the **api request**.
- the `Api` / `Application` qualifier disambiguates; both implement `IRequest<T>`.
- naming → [application request](../../../constructs/data/application-request.md) § *Type name*.
- a domain prefix sorts a concern's messages together; a verb prefix scatters them.
- an **api request** is verb-first — it serves one controller action ([api messages](../../api/api-messages.md)).

### One model or two

- **Body == application request** (no server-only inputs) → **one model**.
- bind the `Command` / `Query` directly (`[FromBody] TCommand`); no api request.
- **Application request ⊃ body** (actor / source IP / a route id) → **two models**.
- declare an api request beside the `Command` / `Query`.
- the api request maps in at the edge — `request.ToCommand(...)` → [api messages](../../api/api-messages.md).

---

## Registration & usage

- `AddMediator(assembly)` **once per handler-bearing assembly** (typically Application).
- registers `IMediator` / `ISender` / `IPublisher` — `TryAdd`, safe across assemblies.
- scans closed `IRequestHandler<,>` / `INotificationHandler<>` as transient.
- adding a handler is adding the class — no DI edit.
- the parameterless overload scans `Assembly.GetCallingAssembly()` — pass it explicitly from another layer.

Never inject concrete `Mediator`. Pick the narrowest abstraction:

| Inject | Method | Use in |
|---|---|---|
| `ISender` | `SendAsync` | controllers, handlers issuing a sub-request |
| `IPublisher` | `PublishAsync` | raising domain events |
| `IMediator` (= `ISender` + `IPublisher`) | both | only when a type genuinely needs both |

- **Dispatch** — `ISender.SendAsync`; the `IRequest<TResponse>` overload returns `ValueTask<TResponse>`.
- the no-response `IRequest` overload returns `ValueTask<Unit>`.
- events → `IPublisher.PublishAsync` (`ValueTask`); handlers implement `HandleAsync`.
- controllers dispatch via `ISender.SendAsync` then `.Match` ([controller](../../../constructs/behavior/controller.md)).
- a query/command **is** an `IRequest<T>`, so `SendAsync` binds to it natively — no extension layer.

---

## Pipeline behaviors

- cross-cutting logic wrapping every request = `IPipelineBehavior<TRequest,TResponse>`.
- it is an open generic, `where TRequest : notnull`.
- implement `HandleAsync(request, RequestHandlerDelegate<TResponse> nextStep, ct)`.
- `await nextStep()` **exactly once** to continue.
- register via `AddMediatorBehavior(typeof(X<,>))`.

> **Registration order = execution order.** First registered runs first, wrapping the rest.
> Register logging before validation to log failed validations.

Built-ins — each registers as `AddMediatorBehavior(typeof(<Behavior><,>))`:

- `AddMediatorLoggingBehavior` → `LoggingBehavior<,>`, on every request.
  - logs request name + elapsed ms; failures at `Error`.
- `AddMediatorValidationBehavior` → `ValidationBehavior<,>`, when an `IValidator<TRequest>` is present.
  - `IValidator<T>.ValidateAndThrow`, throws on invalid.
- `AddMediatorIdempotencyBehavior` → `IdempotencyBehavior<,>`, opt in with `IIdempotent`.
  - dedups by `IdempotencyKey`, caches + replays the response.
- `AddMediatorAuthorizationBehavior` → `AuthorizationBehavior<,>`, opt in with `IRequireAuthorization`.
  - ASP.NET Core authz; throws `UnauthorizedAccessException` / `AuthorizationException`.

- **Idempotency** — opt in via `IIdempotent.IdempotencyKey`; an unmarked request passes through.
- the first call stores via `IIdempotencyStore`, and a repeat replays the response.
- wires the single-instance `InMemoryIdempotencyStore` — swap a distributed store for multi-instance.
- TTL via `IdempotencyBehavior<,>.Ttl` (default 24h).
- **Authorization** — `IRequireAuthorization.PolicyName`, nullable → the default policy.
- also wires `AddHttpContextAccessor()` + `AddAuthorization()`.
