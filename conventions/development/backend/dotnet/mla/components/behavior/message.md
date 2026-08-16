# Messages

*Last updated: 2026-08-16*

> A dispatched use-case — a query, a command or an event, and the handler bound to it.
> Purpose — let a caller name the work it wants without naming who does it.
> Use case — reach here when a controller or a handler triggers work it does not own.

## Location

### Folder
- must sit in a `Queries/`, `Commands/` or `Events/` folder under the domain that owns the use-case.

### File
- must give the message and its handler one file each, named for the type.

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a marker or handler interface with **Defines**.
- must start a concrete message with **Represents**, and name the action it asks for.
- must start a concrete handler with **Handles**, and `<see cref>` the message it takes.

#### [Type params](../../../lla/notation/documentation/typeparams.md)
- must carry a `<typeparam>` for the result a marker is generic over.

```csharp
// ✅ the marker defines, the message asks, the handler answers
/// <summary>Defines a query that returns <typeparamref name="TResult"/>.</summary>
/// <summary>Represents a query to get every channel.</summary>
/// <summary>Handles <see cref="ChannelGetAllQuery"/>.</summary>

// ❌ Represents claims a value the marker carries nothing of
/// <summary>Represents a query returning a result.</summary>
```

### Type name
- must suffix with `Query`, `Command` or `Event`, and suffix its handler with `Handler`.
- must read `{Domain}{Action}{Kind}`, domain-first and singular — `CodeGetByIdQuery`.

## Content

### Member docs

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start each message property with **Gets**, since the members are `init`-only.

#### [Params](../../../lla/notation/documentation/params.md)
- must carry a `<param>` for every parameter of `HandleAsync`, the cancellation token included.

```csharp
// ✅ a complete parameter set, and the referent named
/// <summary>Gets the identifier of the code to load.</summary>
/// <param name="query">The query to handle.</param>
/// <param name="cancellationToken">The token that cancels the handling.</param>

// ❌ a partial set reads as an omission rather than a decision
/// <param name="query">The query to handle.</param>
```

### Members
- must carry every input the handler reads as a property on the message.
- must take each collaborator through the handler's constructor — a repository is not an input.
- must use a block body `{ }` from the start — a handler orchestrates a use case, and every one gains steps
  ([style](../../../lla/notation/style/style.md) § *The body*).
- must bind exactly one handler to a query and to a command; an event takes 0..N.
- must order the message's properties as they arrive: route id, then body, then caller context.

## See also

- [components](../components.md) — the `Handler` + `Command`/`Query`/`Event` row
- [mediator](../../domains/messaging/mediator.md) — dispatch, pipeline behaviors, registration
- [controller.md](controller.md) — the caller that sends one
