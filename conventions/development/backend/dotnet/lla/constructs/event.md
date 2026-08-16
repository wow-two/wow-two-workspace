# Event

*Last updated: 2026-08-16*

> The C# `event` keyword — banned, and the declaration form that replaces it.
> Purpose — keep the fan-out shape on the mediator bus, where it is awaited, isolated and resolvable from DI.
> Use case — reach here when a type looks like it needs to notify more than one listener.

## `event` — the keyword

Zero occurrences across every repo in the workspace; the ban is what produced that, and until now no doc carried it.

Four failures, and a service host hits every one:

- **the handler cannot be awaited** — an event handler returns `void`, so `async void` is the only way to await inside it. The publisher cannot know when the work finished, its exceptions surface on the thread pool unobserved, and no cancellation token reaches it.
- **the lapsed listener** — the publisher holds a **strong** reference to every subscriber. One that never unsubscribes is never collected, which in a long-lived host is a leak that grows with uptime.
- **the null-invocation race** — `if (Changed != null) Changed(this, e);` throws when the last subscriber detaches between the check and the call. `?.Invoke` fixes it, and every author has to remember to.
- **one throwing handler aborts the rest** — a multicast delegate walks its invocation list in order, so the first exception stops every later subscriber from running.

- must not declare a C# `event` member, at any visibility.
- must publish an `IEvent` on the mediator bus instead — an event already has **0..N** handlers there
  ([mediator.md](../../mla/domains/messaging/mediator.md) § *Cardinality*), which is the fan-out a C# `event` would otherwise hand-roll. The bus answers all
  four: handlers return `Task` and are awaited, they resolve per dispatch from DI so nothing is retained, the dispatcher owns the empty-set
  case, and it isolates a throwing handler from the rest.
- an observer set injected as `IEnumerable<IObserver>` is the same shape as a C# `event` and folds the same way
  ([component-names.md](../../mla/components/components.md) § *Folds*, `Observer` row).

---
