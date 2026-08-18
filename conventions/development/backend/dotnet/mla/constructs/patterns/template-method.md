# Template method

*Last updated: 2026-08-16*

> An abstract base that fixes the order of a flow and leaves named hooks for the parts that vary.
> Purpose — keep an order that must not vary out of every subclass, where each one could get it wrong.
> Use case — reach here when the framework or the SDK already owns the flow and only the steps are ours.

## Shape

- must make the base `abstract` and the fixed flow non-virtual; only the hooks are `virtual` or `abstract`.
- must suffix a hook with `Core` when it sits inside a member the framework already defines —
  `ConfigureConventionsCore` under EF's `ConfigureConventions` (`src/Data/EntityFrameworkCore/AppDbContextBase.cs`).
- must give a `virtual` hook a no-op default and an `abstract` hook none — the modifier states whether the step
  is optional.
- must state the contract the subclass owes in `<remarks>` on the base — *call `base.OnModelCreating` first*.
- must suffix the base `Base` only when it is a test or scaffold base — a shipped base is named for what it is.

```csharp
// ✅ the flow is fixed, the hook is named and optional
public abstract class EventSagaStep : IEventSagaStep
{
    public abstract ValueTask<EventSagaStepOutcome> ExecuteAsync(EventSagaContext context, CancellationToken ct);

    public virtual ValueTask CompensateAsync(EventSagaContext context, CancellationToken ct) => ValueTask.CompletedTask;
}
```

---

## Use

- must reach for it where a framework base already imposes the shape — `BackgroundService.ExecuteAsync`
  ([hosted service](../behavior/hosted-service.md)), a `DbContext`, a test fixture.
- must reach for it when a step's default is *do nothing* and most subclasses will keep it.
- must reach for it in a testing harness, where the setup and teardown order is the contract
  ([testing](../../architecture/clean/testing.md)).

---

## Limits

- must prefer composition when the varying part could be injected — a `Strategy` beats a subclass, and it is testable
  alone ([strategies](strategies.md)).
- must not go past one level of inheritance; a three-deep chain hides which override runs.
- must not leave a hook that a subclass **must** call at a particular point — make the base call it instead.
- must not use a template method to share utility code — that is an `Extensions` class
  ([components](../../components/components.md)).

---

## Components

- [hosted service](../behavior/hosted-service.md) — the most common base we derive from.
- [strategies](strategies.md) — the composition alternative, and the default when either would work.
- [entity configuration](../../domains/persistence/access/ef/entity-configuration.md)
  — the EF hooks the context base applies.
