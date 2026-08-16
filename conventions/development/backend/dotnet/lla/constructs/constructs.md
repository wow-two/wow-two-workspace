# Language constructs

*Last updated: 2026-08-16*

> Every C# construct we may declare, what each one is for, and the constructs banned outright.
> Purpose — settle the *form* once, so no role doc has to re-argue `record` vs `class`.
> Use case — reach here before declaring a type, and whenever a construct is unfamiliar in this codebase.

## The constructs

| Construct | Use it for | Notes |
|---|---|---|
| `sealed record` | a data carrier — anything whose identity is its values | body properties, never positional ([models.md](records.md)) |
| `sealed class` | behaviour — anything whose identity is what it does | value equality would be wrong here |
| `interface` | a contract, data-shaped or behaviour-shaped | the role picks the starter ([../documentation/summary.md](../notation/documentation/summary.md)) |
| `enum` | a closed set of named options | one file per enum; the domain-mapping rules are MLA |
| `static class` | a `Constants` or `Extensions` role only | [constants.md](../components/constants.md) · [extensions.md](../components/extensions.md) |
| `struct` · `record struct` | a value type with a measured allocation reason | the default is a reference type — measure first |
| `delegate` | a callback shape a method group cannot express | prefer `Func<>` / `Action<>` unless the name earns itself |

## Banned constructs

A ban here is about the **construct**, whatever role holds it. A ban that depends on the role lives with that role in
[`mla/components/`](../../mla/components/components.md).

| Banned | Reach for instead | Why |
|---|---|---|
| `event` | an `IEvent` on the mediator bus | [event.md](event.md) — four failures a service host hits |
| positional records for data carriers | body properties with `{ get; init; }` | [models.md](records.md) |
| `dynamic` | generics or polymorphism | [../style/style.md](../notation/style/style.md) § *Banned* |
| `using static` | the type name at the call site | [../naming/naming.md](../notation/naming/naming.md) § *Banned* |

## See also

- [shape.md](constructs.md) — the lead, and the rule that form is chosen never defaulted
- [../../mla/components/components.md](../../mla/components/components.md) — the roles these constructs carry
