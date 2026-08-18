# State machines

*Last updated: 2026-08-16*

> A type declaring the states a long-running thing passes through and the event that moves it between them.
> Purpose — keep a lifecycle in one readable declaration instead of scattered flags each caller must interpret.
> Use case — reach here when a process has named stages, correlates across messages, and can time out.

## Shape

- must derive from `SagaStateMachine<TState>` (`src/Messaging/Saga/SagaStateMachine.cs`), declare every clause in the
  constructor, and register with `AddSaga<TStateMachine, TState>`.
- must hold no per-message state on the machine — it is a definition registered as a singleton, and a transition
  resolves what it needs from the message scope.
- must keep the instance state in a `TState : ISagaState`, persisted through the saga repository.
- must declare each state as a `const string` named for the condition it is in — `AwaitingPayment`, not `PaymentSent`.
- must declare correlation once per event type, on one `When<TEvent>(e => e.Key)` clause; later clauses use the bare
  `When<TEvent>()`.
- must terminate: every path reaches `Finalize()`, and a `Schedule` timeout carries the instance out of a stuck state.

```csharp
// ✅ states are named conditions, transitions are declared once
public sealed class OrderStateMachine : SagaStateMachine<OrderSagaState>
{
    public const string AwaitingPayment = "awaiting-payment";

    public OrderStateMachine()
    {
        Initially(When<OrderPlaced>(e => e.OrderId).TransitionTo(AwaitingPayment));
        During(AwaitingPayment, When<PaymentReceived>(e => e.OrderId).Finalize());
    }
}
```

---

## Use

- must reach for a state machine when a lifecycle spans messages arriving minutes or days apart, from anywhere.
- must reach for it when the process can time out, and the timeout is itself a transition.
- must reach for it when the states are a fact the product names — an order, an onboarding, a payout.

---

## Limits

- must not model a linear itinerary as a state machine — an ordered sequence we drive is a routing slip
  ([sagas](sagas.md)).
- must not carry a lifecycle as a status column plus a `switch`; the switch is where a missing transition hides.
- must not put I/O in a clause action — a clause changes state and publishes; a handler does the work.
- must not split one lifecycle across two machines; correlation is what makes it one process.

---

## Components

- [sagas](sagas.md) — state machine versus routing slip, and where each fits.
- [handler](../behavior/handler.md) — the events that drive transitions, and their handlers.
- [entity](../data/entity.md) — the persisted state row and its key contract.
