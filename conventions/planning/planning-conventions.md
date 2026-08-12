# Conventions — Planning

*Last updated: 2026-06-10*

> How we **plan** — the shape of planning docs. The actual plans live per-repo
> (`engineering/versions/`, `engineering/planning/`); this domain owns their format.

| Area | Covers |
|---|---|
| [rough-track/](rough-track/rough-track.md) | Rough docs — `r{X.Y}` unbounded first build, one task per subsystem, no sub-steps + template |
| [version-track/](version-track/version-track.md) | Version docs — `v{X.Y}/v{X.Y}.md` folders, lifecycle, cadence, rules + iteration template |
| [polish-track/](polish-track/polish-track.md) | Polish docs — behavior-invariant cleanup, tasks per file, decoupled `p{X.Y}` line + template |
| [vector-track/](vector-track/vector-track.md) | Vector docs — one durable subject lane per chat, archetype stage ladders, seams, git + build contention, release cuts + template |
| [engineering-planning/](engineering-planning/engineering-planning-conventions.md) | The repo's main planning doc — versions · decisions · ordered backlog · log (Haven-proven shape) |

Track order on a new product: `rough` → `polish` (optional) → `version`. A settled product runs `version` + `polish` only.

Those three decompose by **time** and assume one chat. `vector` is the orthogonal axis — it decomposes by **subject** so lanes run in parallel chats, and each lane runs one of the three inside it. A product with 3+ independent subsystems opens vectors first, tracks second.

## Task form — shared by all tracks

- must write each task **verb-first** — a concrete action, never a noun phrase or an `X → Y` mapping. `Move api.ts to integration/`, not `api.ts → integration`.
- must keep **one action per bullet** — split a multi-part change into separate bullets. More bullets is fine; density comes from fewer words per task, not fewer tasks.
- must use the fewest words that name the action + its target; backtick identifiers, drop restatement.

Each track adds the task **grain** on top of this form — polish = a concrete file change, version = a user-facing capability, rough = a whole subsystem (a version's worth of work), vector = one concrete piece of a ladder stage.
