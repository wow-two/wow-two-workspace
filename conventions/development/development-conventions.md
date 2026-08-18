# Conventions — Development

*Last updated: 2026-07-11*

> The **development** domain: how we structure repos and write code. Lookup table, not auto-loaded.
> Each area has its own `{area}-conventions.md` index.

| Area | Covers |
|---|---|
| [repo/](repo/repo-conventions.md) | Repo shape — layout & naming ([repo-structure](repo/structure/repo-structure.md)) · version control · tech stack |
| [backend/](backend/dotnet/dotnet-conventions.md) | .NET code style — documentation, code-org, entities, enums, services, architecture, db, API, launch-profiles |
| [frontend/](frontend/frontend-conventions.md) | TypeScript conventions, cut by scope — `lla/` one symbol · `mla/` one app · `hla/` between apps |

**Cross-area:** [dev-cycle.md](dev-cycle.md) — the 2-cycle app↔SDK maturation rhythm: implement a version in-app → extract stable blocks to the SDK + conventions → adopt across the active apps.

**Cross-area:** [swappable-modules.md](swappable-modules.md) — engine-wrapping SDK modules: contract-first, adapter subpaths with optional peers, one conformance suite, one-line app engine pin.

**Cross-area:** [sdk-extraction.md](sdk-extraction.md) — the extraction **threshold**: what earns a place in either SDK (carries logic + ecosystem-worth) vs stays inline in the product (pure DRY / layout wrappers — duplicate freely); an atom that carries logic is never product-local.

Versioning moved to the sibling **planning** domain → [`../planning/`](../planning/planning-conventions.md).

## Using & evolving conventions

- develop **against** the conventions — read the relevant one before / while writing the code, and follow it
- found a gap or a clearly better way? don't silently diverge — implement, then **propose the convention add / update with the reason(s)**, after the implementation
- the convention change rides in with the work that motivated it — so we keep shipping while closing convention gaps
