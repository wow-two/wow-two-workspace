# Behavior constructs

*Last updated: 2026-08-19*

> The constructs whose identity is what they **do** — the seams a component consumes, and the reactive state
> it owns.
> Purpose — nothing here renders, so the name is the only thing that says what the construct is responsible for.
> Use case — declaring an interface behind a capability, its implementation, or a `use*` that owns state.

`behavior` is the [backend's word](../../../../../backend/dotnet/core/mla/constructs/behavior/behavior.md) for the same
roles — `*Client` · `*Broker` · `*Adapter` · `*Policy` · `*Registry` name the same thing on both sides.

## The kinds

| Kind | Does |
|---|---|
| [headless suffixes](headless-suffixes.md) | names a role a component consumes and never renders |
| [hooks](hooks.md) | owns state, lifecycle and operations for a subtree — `use*` |

---

## Neighbours

- [constructs](../constructs.md) — the authoring pass and the coining gate every construct runs
- [visual](../visual/visual.md) — the kinds that render, and the suffix each one fixes
- [state and data](../../domains/data/state-and-data.md) — where the seams and hooks here are wired
- [naming](../../../lla/notation/naming/naming.md) — the file and export casing both kinds are spelled in
