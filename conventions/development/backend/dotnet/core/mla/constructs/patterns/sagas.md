# Sagas

*Last updated: 2026-08-16*

> A multi-step process with no distributed transaction, undone by compensating each completed step in reverse.
> Purpose — get atomic-looking outcomes across services, where a rollback is a message rather than a lock.
> Use case — reach here when one business outcome needs several services, each of which can fail on its own.

## Shape

Two forms, and the flow decides which:

- must use a **routing slip** — `EventSagaBuilder.Named(...).Step<T>()…Build()` — for a linear itinerary we drive
  (`src/Messaging/EventSaga/EventSaga.cs`).
- must use a **state machine** — `SagaStateMachine<TState>` — for a flow the world drives, living in a repository
  between messages ([state machines](state-machines.md)).
- must implement each slip step as an `IEventSagaStep`, or derive from `EventSagaStep` for the no-op compensation
  default.
- must make every step's `CompensateAsync` idempotent — compensation reruns after a partial failure.
- must declare each destination a step addresses with `SendsTo<TEvent>(destination)`; an undeclared address is
  unroutable, and the broker drops it silently.
- must return `EventSagaStepOutcome.Faulted` (or throw) to trigger compensation — a step never decides the
  rollback itself.

```csharp
// ✅ the itinerary is one declaration, compensation is per step
var definition = EventSagaBuilder.Named("order-fulfilment")
    .Step<ReserveInventoryStep>()
    .Step<ChargePaymentStep>()
    .SendsTo<ShipmentRequestedEvent>("shipping")
    .Build();
```

---

## Use

- must reach for a saga when a business outcome crosses a service boundary and a failure must undo prior work.
- must reach for the routing slip when the sequence is known up front and we own the ordering.
- must reach for the state machine when steps are triggered by events arriving minutes or days apart.

---

## Limits

- must not use a saga inside one service over one database — that is a transaction
  ([unit of work](unit-of-work.md)).
- must not treat compensation as a rollback — a charge is refunded, not un-charged; the record of both stays.
- must not write a step whose compensation is impossible; an irreversible step goes last, after everything reversible.
- must not carry business state on the saga context for a later step to re-read — the context is a slip, not a store.
- must not publish a saga step's event without an outbox where the step also writes rows ([outbox](outbox.md)).

---

## Components

- [state machines](state-machines.md) — the long-running form, its states and correlation.
- [handler](../behavior/handler.md) — the events steps consume and raise.
- [outbox](outbox.md) — how a step's write and its publish agree.
- [builders](builders.md) — the `EventSagaBuilder` shape, and where `Build()` validates.
