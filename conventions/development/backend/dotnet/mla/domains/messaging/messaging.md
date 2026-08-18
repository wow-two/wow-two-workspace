# Messaging

*Last updated: 2026-08-16*

> How work is dispatched to the type that does it, in-process and across process boundaries.
> Purpose — a caller names the work, never the worker, so the two move independently.
> Use case — sending a command, publishing an event, or adding a transport.

## Contract

- must dispatch through an abstraction, never a concrete dispatcher type.
- must bind exactly one handler to a command and to a query, and 0..N to an event.
- must carry every input on the message; a collaborator arrives through the handler's constructor.
- the message and handler shapes are components → [application request](../../constructs/data/application-request.md)
  and [handler](../../constructs/behavior/handler.md).

---

## Naming

- must read `{Domain}{Action}{Kind}`, domain-first and singular — `CodeGetByIdQuery`, `ChannelGetAllQuery`.
- must be noun-first, because an application message is searched by domain rather than by action.
- must suffix the handler with `Handler` and name it for its message — `CodeGetByIdQueryHandler`.
- must suffix a returned payload with `Result` — `ChannelGetAllResult`.
- baseline declaration rules → [application request](../../constructs/data/application-request.md).

---

## Members

- must carry every input the handler reads as a property on the message.
- must take each collaborator through the handler's constructor — a repository is not an input.
- must order the message's properties as they arrive: route id, then body, then caller context.
- must return `AppResult<TSuccess>` from every handler → [result](../../constructs/data/result.md).
- must use a block body `{ }` in a handler from the start — a use case gains steps
  ([style](../../../lla/notation/style/style.md) § *The body*).

```csharp
// ✅ inputs on the message, collaborators on the handler
public sealed record CodeGetByIdQuery : IQuery<AppResult<CodeDto>>
{
    /// <summary>Gets the identifier of the code to load.</summary>
    public required Guid Id { get; init; }
}
// ❌ a collaborator as an input, which makes the message un-serializable
public sealed record CodeGetByIdQuery
{
    public required ICodeRepository Repository { get; init; }
}
```

---

## Member docs

- must start each message property with **Gets** — the members are `init`-only.
- must carry a `<param>` for every parameter of `HandleAsync`, the cancellation token included.
- must start the handler's summary with **Handles**, and `<see cref>` the message it takes.

---

## Dispatch

- must bind exactly one handler to a query and to a command; an event takes 0..N.
- must send through `ISender`, and publish an event through `IPublisher` → [mediator](../messaging/mediator/mediator.md).
- must not let a handler send another message — a use case that needs a second one is composing, not dispatching.


---

## Providers

| Provider | Carries | Docs |
|---|---|---|
| in-process mediator | a request to its one handler, inside the same process | [mediator](mediator/mediator.md) |
| event bus | an event to its subscribers, in-process or over a transport | — |
| outbox | an event staged in the business transaction, dispatched after commit | [outbox](../../constructs/patterns/outbox.md) |

- must keep transport choice out of the message — a message that names its transport cannot be re-routed.
