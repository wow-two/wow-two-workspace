# Version Track

*Last updated: 2026-06-27*

A per-version progress doc — the iterations and capabilities a product ships in one version.

## Location & naming

- must place each version at `engineering/planning/version-track/v{X.Y}/v{X.Y}.md` — one folder per version, file named after its folder
- must keep the lead doc `engineering/planning/version-track/version-track.md` — the active version + a link to this convention
- must start at `v0.1`; minor-increment `Y`; bump major `X` only at `Y = 100` or a breaking change
- must treat the latest folder as the active one

## Scope

- must be exactly one type, declared on the meta line:

| Type | Scope | Task verb |
|---|---|---|
| `Feature` | a new user-facing capability, or a bug fix | `Ability to {capability}` · `Fix {behavior}` |
| `Adoption` | a large or interconnected extraction to / from the SDK (a whole layer / coupled set) | `Extract {thing} → SDK` · `Adopt {SDK thing}` |

- must hold ≤ 1 week of work — overflow goes to `engineering/planning/backlog.md`
- must plan only the next version — future work waits in the backlog
- a cycle is `Feature` → `Adoption`; 1 cycle = 2 versions (full model → `../../development/dev-cycle.md`)

## Structure

- must group `### Iteration {N} — {noun}` → `[ ]` tasks; the iteration name is its focus noun, no `: {goal}` clause
- must write each task as a capability the version delivers — abstract, user-POV: `Ability to log in as a guest`, not `Mint a guest cookie`
- must open each task with the Type verb — `Ability to` / `Fix`; `Extract … → SDK` / `Adopt …`
- must keep one capability per task on one line — no `— detail` clause; join closely-related with `and`, split unrelated
- must stay capability-grained — never per-endpoint, per-field, or naming a table / class / file
- may close with a `### Verification` iteration — always last, bare noun, ordered `[ ] {action} → {expected}` checks
- must carry meta `**Status:** … · **Type:** … · **Started:** … · **Completed:** …` (those four only); declare a `Type`; title is a plain noun phrase

## Lifecycle

- `⏳ Planned` → `🚧 In Progress` → `✅ Complete`
- must open a version when planning it and close it when its tasks are done — set `Completed`, flip `Status`; one active at a time

## Rules

- must write a transient plan at `engineering/planning/version-track/v{X.Y}/{iter-slug}.md` at iteration start (what + how), review before implementing, delete when done
- must record green (build / test counts) only in the `Verification` iteration — never on a build iteration
- must not put a status emoji on an iteration heading — the `[ ]` / `[x]` checkboxes carry done-state
- must cover only this repo — another app's rollout lives in that app's version doc
- must not keep a `## Log` — git is the history

## Template — copy below the line

---

# v{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** ⏳ Planned · **Type:** {Feature | Adoption} · **Started:** {YYYY-MM-DD} · **Completed:** —

### Iteration 1 — Listing ingest

- [ ] Ability to pull new listings on a schedule, skipping ones already saved.

### Iteration 2 — Match classification

- [ ] Ability to classify new listings and mark the matches.

### Iteration 3 — Verification

- [ ] Run a scrape → new listings stored, duplicates skipped.
- [ ] Run classify → each listing recorded, matches flagged.
