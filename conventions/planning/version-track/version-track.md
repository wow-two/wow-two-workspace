# Version Track

*Last updated: 2026-07-11*

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
- may break a task into indented `- [ ]` **sub-steps** when the how needs itemizing — a sub-step is one concrete action (the *what* + *where*), never a paragraph
- must open each task with the Type verb — `Ability to` / `Fix`; `Extract … → SDK` / `Adopt …`
- must keep one capability per task on one line — no `— detail` clause; join closely-related with `and`, split unrelated
- must follow the shared **Task form** — verb-first, one action per bullet, fewest words ([planning-conventions.md](../planning-conventions.md))
- must stay capability-grained — never per-endpoint, per-field, or naming a table / class / file
- may close with a `### Verification` iteration — always last, bare noun, ordered `[ ] {action} → {expected}` checks
- must carry meta `**Status:** … · **Type:** … · **Started:** … · **Completed:** …` (those four only); declare a `Type`; title is a plain noun phrase

## Lifecycle

- `⏳ Planned` → `🚧 In Progress` → `✅ Complete`
- must open a version when planning it and close it when its tasks are done — set `Completed`, flip `Status`; one active at a time
- must not advance to the next version until the current is `✅ Complete` **and** the developer explicitly says to proceed — never pre-declare, queue, or auto-begin the next version (in chat or in the plan); finish, report, and stop
- must **verify completion with the developer** before marking a version / iteration complete — never self-declare it
- may **drop a completed iteration's tasks + steps** once verified — keep the bare `### Iteration N — Name` heading; git holds the detail

## Rules

- must write a transient plan at `engineering/planning/version-track/v{X.Y}/{iter-slug}.md` at iteration start (what + how), review before implementing, delete when done
- must record green (build / test counts) only in the `Verification` iteration — never on a build iteration
- must not put a status emoji on an iteration heading — the `[ ]` / `[x]` checkboxes carry done-state
- must keep the iteration heading a **bare name** — just the focus noun; no trailing `(done)` / `(final)` / parenthetical / status / version tag
- must not frame or report the work as *closing* / *finalizing* the version — report per iteration (*did X, Y; Z remaining*); a track is open-ended, extend it freely, never push it toward closure
- must cover only this repo — another app's rollout lives in that app's version doc
- must not keep a `## Log` — git is the history
- must **move** an item that changes iteration, never leave a forwarding stub (`→ moved to Iteration N`). The destination line is the record; a stub duplicates state and goes stale the moment the item moves again
- must not name the current iteration in the doc — it is the first one with open boxes. A `(current)` tag is a second source of truth that rots on every advance

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
