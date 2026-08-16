*Last updated: 2026-08-13*

# Tasks

> Single source of truth for active `wow-two` work. Scored + pulled by [`session-planning.md`](../sessions/planning/session-planning.md) (`pln-w2`).
> **Grain: abstract.** A row states a capability — *finish codes functionality for smart-qr* — never its sub-steps. The breakdown lives in that repo's `engineering/planning/`.
> Calendar slots are not tracked here.

**Columns:** `Task ID` = `{cat}-t-{NNN}` · `Priority` = `high` 0.5 / normal 1.0 / `low` 2.0 · `Status` = `todo` / `wip` / `blocked` / `done` · `Repo` = owning repo, or `-` for workspace-level

Categories: `sdk` · `plt` · `app` · `ven` · `con` · `ws`

---

## Ventures

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `ven-t-001` | Record the ministry outcome + agreed next steps | `-` | `high` | `todo` | `ventures.tnis` | Presentation `2026-08-12`, 1:45–4 PM. Written nowhere yet. Home: `product/context.md` |
| `ven-t-002` | Advance `TNIS` per `follow-up-roadmap.md` | `-` | `high` | `wip` | `ventures.tnis` | ~6h15m `08-12`, brainstorms `08-13`. Roadmap holds the breakdown |
| `ven-t-003` | Name the active Micro-SaaS candidate | `-` | normal | `todo` | `-` | One block `08-12`. `10x-ws` tracks a matching task to give Micro SaaS a section there |

---

## Conventions

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `con-t-001` | Close the presentation-layer convention | `-` | `high` | `wip` | `-` | `request-models.md` + `response-models.md` + the doc-format pattern |
| `con-t-002` | Land the Dto-vs-`Response` naming cleanup | `-` | normal | `todo` | `-` | Convention states it; renaming is per-app work |

---

## Workspace

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

---

## Backlog

Not started, ordered, top = next. Pulling one promotes it above and mints its ID.

### → beta SDK (`wow-two-sdk.backend.beta`)

| Item | Type | Notes |
|---|---|---|
| `IClock` + `DateTimeOffset` clock → `Foundation.Time` | feature | adopting = a pure delete in products |
| `FailureCategory` union (`+402` / `+503`) → canonical enum | feature | bake at extract time |
| `ApiResponse<T>` envelope → `Web.Contracts` | feature | products drop the inline copy |
| Remaining v0.2 extract items | feature | 13-item list, detail in drydock's backlog |
| `ToCommand` / `ApiRequest` support | idea | evaluate once apps adopt the convention |

### Conventions

| Item | Type | Notes |
|---|---|---|
| Domain-first example rename in `controllers.md` | issue | examples are verb-first; `mediator.md` mandates domain-first |
| Adopt the doc-format pattern across all convention docs | check | keyword · ✅/❌ · sparing `MUST` / `SHOULD` |

---

## Detail pointers

Not tasks — where a promoted capability gets broken down.

| Source | Holds |
|---|---|
| `workbench/{org}/{repo}/engineering/planning/` | that repo's roadmap, backlog, versions |
| `workbench/ventures/ventures.tnis/follow-up-roadmap.md` | `TNIS` breakdown |
| `workbench/wow-two/wow-two.refinement` | live ecosystem state + roadmap |

---

## Done

Completions land here, then get pruned once a version doc or git carries them.

- (none yet)
