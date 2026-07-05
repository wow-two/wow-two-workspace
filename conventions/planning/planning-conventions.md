# Conventions — Planning

*Last updated: 2026-06-10*

> How we **plan** — the shape of planning docs. The actual plans live per-repo
> (`engineering/versions/`, `engineering/planning/`); this domain owns their format.

| Area | Covers |
|---|---|
| [version-track/](version-track/version-track.md) | Version docs — `v{X.Y}/v{X.Y}.md` folders, lifecycle, cadence, rules + iteration template |
| [polish-track/](polish-track/polish-track.md) | Polish docs — behavior-invariant cleanup, tasks per file, decoupled `p{X.Y}` line + template |
| [engineering-planning/](engineering-planning/engineering-planning-conventions.md) | The repo's main planning doc — versions · decisions · ordered backlog · log (Haven-proven shape) |

## Task form — shared by both tracks

- must write each task **verb-first** — a concrete action, never a noun phrase or an `X → Y` mapping. `Move api.ts to integration/`, not `api.ts → integration`.
- must keep **one action per bullet** — split a multi-part change into separate bullets. More bullets is fine; density comes from fewer words per task, not fewer tasks.
- must use the fewest words that name the action + its target; backtick identifiers, drop restatement.

Each track adds the task **grain** on top of this form — polish = a concrete file change, version = a user-facing capability.
