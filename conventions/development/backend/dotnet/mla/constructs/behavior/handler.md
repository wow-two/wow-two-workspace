# Handlers

*Last updated: 2026-08-18*

> The single receiver bound to one dispatched message.
> Purpose — the use case lives in one type, reachable without its caller knowing it.
> Use case — every `Command`, `Query` and `Event` that reaches a handler.

## Location

### Folder
- must sit in a `CommandHandlers/`, `QueryHandlers/` or `EventHandlers/` folder beside its messages.

### File
- must give each handler its own file, named for the type.

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Handles**, and `<see cref>` the message it takes.
- must start the handler interface with **Defines**.

```csharp
// ✅ names the message it is bound to
/// <summary>Handles <see cref="ChannelGetAllQuery"/>.</summary>
// ❌ describes the work instead of the binding
/// <summary>Gets every channel from the database.</summary>
```

### Construct
- must declare a `sealed class` — a handler has no value identity.
- must take collaborators through the constructor; an input belongs on the message →
  [constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Type name
- must suffix with `Handler` and name it for its message — `ChannelGetAllQueryHandler`.
- must return `AppResult<T>` carrying a [model](../data/model.md), never a `Dto`.

```csharp
// ✅
public sealed class ChannelGetAllQueryHandler(IChannelRepository repository)
// ❌ named for the work, so its message is unfindable
public sealed class ChannelReader
```
