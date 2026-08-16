# Patterns

*Last updated: 2026-08-16*

> A design pattern we adopt as a component — no C# construct declares it, and no data/behavior split applies.
> Purpose — give a pattern one home, so its shape, naming and docs are settled once instead of per use.
> Use case — reach here when the thing being built is named after a pattern rather than after a layer role.

## Membership

- must be a pattern with a **settled name in the literature** — `Factory`, `Decorator`, `Adapter`, `Strategy`.
- must state what the pattern buys in this codebase, never what the book says it buys.
- must live in `mla/`, not `lla/`: a pattern needs collaborators to mean anything, so it fails the self-sufficiency gate
  ([../../../lla/components/components.md](../../../lla/components/components.md) § *The gate*).

## Adding a pattern

- must follow the component template — Location · Declaration · Content
  ([../../../lla/components/components.md](../../../lla/components/components.md) § *Adding a component*).
- must name the file for the pattern in the plural — `factories.md`, `decorators.md`.

## See also

- [../components.md](../components.md) — the suffix keep-list
- [../data/entity.md](../data/entity.md) · [../behavior/service.md](../behavior/service.md) — the layer-role components
