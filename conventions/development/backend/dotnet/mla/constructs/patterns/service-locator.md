# Service locator

*Last updated: 2026-08-19*

> Resolving a collaborator from the container at the point of use instead of taking it through the constructor.
> Purpose — record why this is banned, and the three places a container reference is still legitimate.
> Use case — reach here when a type is about to inject `IServiceProvider`.

## Shape

- must take every collaborator through the constructor — the ban is stated once in
  [constructs](../../../lla/constructs/constructs.md) and this doc is its pattern entry.
- must not inject `IServiceProvider` into a service, a handler, a controller, or a repository.
- must not call `GetRequiredService` from inside a member whose type could have declared the dependency.
- must not reach a collaborator through a static container accessor or a `ServiceLocator` type — neither exists here,
  and neither may be introduced.

```csharp
// ✅ the constructor states the dependency
public sealed class CodeCreateCommandHandler(ICodeRepository codes, IOutbox outbox) { }

// ❌ the dependency is invisible until the line runs
public sealed class CodeCreateCommandHandler(IServiceProvider services) { }
```

---

## Use

Three exceptions, and nothing else:

- must allow it at the **composition root** — `HostConfiguration.Extensions.cs` builds the graph, so it holds the provider
  ([host configuration](../../platform/startup/host-configuration.md)).
- must allow `IServiceScopeFactory` where the consumer outlives a scope — a `BackgroundService` creating one scope
  per iteration ([background service](../behavior/background-service.md)).
- must allow resolution inside a `Factory` that dispatches on a runtime key — that dispatch is the factory's whole
  reason to exist ([factories](factories.md)).

---

## Limits

- must not treat a factory-delegate registration as a licence to resolve elsewhere; the delegate runs at the root.
- must not use a scope factory to dodge a lifetime mismatch — a singleton holding scoped state is a lifetime error,
  and the scope factory only hides it ([singleton](singleton.md)).
- must not resolve an optional dependency conditionally; register a no-op instead ([null object](null-object.md)).
- must not keep a resolved instance past the scope that produced it — a captured `DbContext` outlives its transaction.

---

## Components

- [factories](factories.md) — the sanctioned per-key resolution, and its shape.
- [background service](../behavior/background-service.md) — the scope-per-iteration rule.
- [host configuration](../../platform/startup/host-configuration.md) — the only layer holding the provider by design.
- [ambient context](ambient-context.md) — the sibling: a hidden value rather than a hidden dependency.
