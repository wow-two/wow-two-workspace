# Conventions — Development — Repo

*Last updated: 2026-07-12*

> How a repo is shaped and equipped — repo **shape** splits by **archetype** (product / venture vs SDK / library),
> grouped under `structure/`; version control + the default tech stack are the shared, cross-archetype setup. Code
> style for each stack is in the siblings [../backend/](../backend/) + [../frontend/](../frontend/). Serving + dev-port
> allocation are a deployment concern → [../../deployment/deployment-conventions.md](../../deployment/deployment-conventions.md).

## Structure

Repo shape by archetype — product / venture (both stacks, one repo) vs SDK / library (one published package). Don't force one shape into the other.

| File | Covers |
|---|---|
| [structure/repo-structure.md](structure/repo-structure.md) | Product / venture — top-level `product/` + `engineering/`, code under `engineering/codebase/{slug}.{backend,frontend}-services`, naming, folder-docs (no README below root), archetypes, ecosystem naming, image-publish contract (§13), repo audit |
| [structure/sdk-structure.md](structure/sdk-structure.md) | SDK / library — `engineering/` + npm package nested under `engineering/codebase/{slug}/`, `src/` source-only + `tests/{unit,stories}`, config repoint, dist-only publish |

## Version control

| File | Covers |
|---|---|
| [version-control/git.md](version-control/git.md) | Commit-message format — `{type}: {past-tense verb} {subject}`, one cohesive change per commit — **+ the agent⇄human commit protocol** (agent stages + drafts; the human commits + pushes, hook-enforced) |

## Tech stack

> The default stack for wow-two product / venture repos; an SDK repo runs the same floor. Code-style per layer: [../backend/](../backend/) · [../frontend/](../frontend/).

- **Backend** — .NET 10 · ASP.NET Core · EF Core · MediatR (CQRS) · Clean Architecture. DB: SQLite (single-user / POC) → Postgres (when scaling / multi-instance). CI: GitHub Actions → GHCR.
- **Frontend** — React 19 · Vite · TypeScript (strict) · Tailwind v4 · `@wow-two-beta/ui`.
- **Beta SDKs** — consume these first; build-locally-then-migrate if a capability is missing.
  - `@wow-two-beta/ui` (npm) — React component library.
  - `WoW.Two.Sdk.Backend.Beta` (nuget.org) — backend wrappers (hosting, observability, mediator, …). Still maturing — adopt where stable.
