*Last updated: 2026-08-21*

# Tasks

> Single source of truth for active `wow-two` work. Scored + pulled by [`session-planning.md`](../sessions/planning/session-planning.md) (`pln-w2`).
> **Grain: abstract.** A row states a capability — *finish codes functionality for forever-pin* — never its sub-steps. The breakdown lives in that repo's `engineering/planning/`.
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
| `ven-t-004` | Finish the Mintrans demo solution and share it | `2026-08-23` | `high` | `todo` | `ventures.tnis-mintrans` | Added `2026-08-17`. The deliverable sent to Mintrans — distinct from the venture (`ventures.tnis`) and from the hackathon demo, which lives in Yandex org. Gates `ven-t-005` |
| `ven-t-008` | Send the Mintrans project requirements | `-` | `high` | `done` | `ventures.tnis-mintrans` | ✅ `2026-08-19` — prepared 9:00 AM + 3:00 PM, sent 3:30 PM. Precedes the demo (`ven-t-004`) |
| `ven-t-005` | Complete the Mintrans integration | `2026-09-06` | `high` | `todo` | `ventures.tnis-mintrans` | Added `2026-08-17`. Breakdown belongs in the repo’s `engineering/planning/`, not here |
| `ven-t-006` | Advance forever-pin per its `engineering/planning/` | `-` | `high` | `wip` | `smart-qr-poc` | Added `2026-08-17`. 10h across `08-15`–`08-16`, the heaviest venture thread this month |
| `ven-t-007` | Rename smart-qr → forever-pin in code and package names | `-` | normal | `todo` | `smart-qr-poc` | Docs + `active.sh` key renamed `2026-08-17`; repo dirs stay `smart-qr-poc` / `smart-qr-promo` for now. Left: `smartqr.*` project names, `SmartQrPromo` / `SmartQrHero` Remotion ids, the `-poc` suffix. Domain `foreverpin.com` |

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
| `workbench/ventures/ventures.tnis/follow-up-roadmap.md` | `TNIS` venture breakdown |
| `workbench/ventures/ventures.tnis-mintrans/` | the Mintrans deliverable — demo + integration |
| `workbench/wow-two/wow-two.refinement` | live ecosystem state + roadmap |

---

## Done

Completions land here, then get pruned once a version doc or git carries them.

- (none yet)
