# Adapters

*Last updated: 2026-08-16*

> A type that implements our contract by delegating to a foreign one we do not own.
> Purpose — keep a third-party type out of every consumer, so swapping the library edits one file.
> Use case — reach here when a library already does the work but speaks a shape our code must not import.

## Shape

- must suffix the type with `Adapter` and prefix it with the **foreign** side —
  `FluentValidationAdapter<T> : IValidator<T>` (`src/Foundation/Validation/`), `HybridCacheRepository : ICacheRepository`
  (`src/Caching/Hybrid/`), `FeatureManagerAdapter : IFeatureFlags` (`src/FeatureFlags/Core/`).
- must implement one of our interfaces and add nothing to it — an adapter translates, it does not decide.
- must keep the foreign type inside the adapter: no consumer references it, and the `.csproj` reference stays local.
- must be `sealed`, and take the foreign collaborator through the constructor.
- must start the `<summary>` with **Adapts**, and name both contracts
  ([summary](../../../lla/notation/documentation/summary.md)).
- must translate the foreign failure into our model — an exception becomes an `AppError`
  ([result](../data/result.md)).

```csharp
// ✅ our contract out, the library's type in, nothing added
/// <summary>Adapts FluentValidation validators to the <see cref="IValidator{T}"/> contract.</summary>
public sealed class FluentValidationAdapter<T> : IValidator<T>
{
    public ValidationError? Validate(T instance) { /* fans out over the registered validators */ }
}
```

---

## Use

- must reach for an adapter when a library's contract and ours differ but the capability is the same.
- must reach for it when two libraries must be interchangeable behind one contract
  ([swappable modules](../../../../../../swappable-modules.md)).
- must reach for it at a framework hook we cannot rename — an EF interceptor, a hosted service.

---

## Limits

- must not adapt when we own both sides — change the contract instead.
- must not put policy in an adapter — caching, retry and degradation belong to the `Broker` or the `Client`
  ([broker](../behavior/broker.md)).
- must not widen our contract to fit the library; the contract is ours, and an adapter that cannot satisfy it
  is the wrong library.
- must not stack an adapter over an adapter — the second one means the contract is wrong.

---

## Components

- [broker](../behavior/broker.md) — the app-side seam that *names* an outside capability; an adapter only translates.
- [client](../behavior/client.md) — the provider-facing half, which speaks the provider's model on purpose.
- [validator](../behavior/validator.md) — the worked case: `FluentValidationAdapter<T>` behind the SDK
  `IValidator<T>`.
- [swappable modules](../../../../../../swappable-modules.md) — contract plus adapters plus one conformance suite.
