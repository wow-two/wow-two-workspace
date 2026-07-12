# Polish Track

*Last updated: 2026-07-11*

A per-iteration cleanup doc — behavior-invariant changes to existing code, grouped by the file they touch.

## Location & naming

- must place each iteration at `engineering/planning/polish-track/p{X.Y}/p{X.Y}.md` — one folder per iteration, file named after its folder
- must keep the lead doc `engineering/planning/polish-track/polish-track.md` — the active iteration + a link to this convention
- must start at `p0.1`; minor-increment `Y`; bump major `X` only at `Y = 100`
- must treat the latest folder as the active one

## Scope

- must not change observable behavior — same inputs, same outputs, before and after; the test suite is green on both sides
- may refactor at **any size, in-app** — rename, dedupe, split, move, re-layer, restructure folders / domains, rewrite at parity; the functionality already exists, polish just reshapes it
- must escalate anything that changes behavior, a bug included, to the backlog — never land it here
- SDK extraction (moving code out to a shared package) is polish only when **minor** (one small component); a large or interconnected extraction (a whole layer / many coupled components) is a version `Adoption`, not polish

## Structure

- must group `## Iteration {N} — {name}` → `- [ ]` **task** (abstract one-liner) → indented `- [ ]` **sub-steps** (the how — files, moves); the task is the *what*, a sub-step is one concrete action
- must write each sub-step as a terse action — the *what* + *where* (`CreateCodeRequest → integration/codes`), never a paragraph or the *why* (rationale → chat / commit, not the plan)
- must follow the shared **Task form** — verb-first, fewest words ([planning-conventions.md](../planning-conventions.md))
- must not add a per-step status, ledger, or coverage map — git is the record
- must carry a **one-word** `**Status:** {Planned | In-Progress | Done}` and nothing more — no dates, no per-iteration summary; that context belongs in a handoff doc (write one when the chat's context fills), not the plan

## Lifecycle

- `Planned` → `In-Progress` → `Done` — one word, no emoji, no dates
- must open an iteration when planning it and flip `Status` to `Done` when its tasks are done; one active at a time
- must not advance to the next iteration until the current is `Done` **and** the developer explicitly says to proceed — never pre-declare, queue, or auto-begin the next iteration (in chat or in the plan); finish the current scope, report, and stop
- a deferred-but-in-scope item **reopens** the current iteration (flip `Status` back) — it never justifies moving on; do not mark an iteration `Done` to unblock the next one
- must **verify completion with the developer** before marking an iteration / task done — Claude never self-declares it complete
- may **drop a completed iteration's tasks + steps** once verified — keep the bare `## Iteration N — Name` heading (the arc); git holds the detail. Keeps the doc lean

## Rules

- must run opportunistically — no cadence, no timebox; batch any number of files, or none for a long stretch
- must not spin up a speculative future *track doc* (`p0.2`, …) ahead of need — future iterations may be listed inside the active doc
- must not keep a `## Log` — git is the history
- must keep every iteration / section heading a **bare name** — just the focus noun; no `(done)` / `(final)` / parenthetical / status label; the `[ ]` / `[x]` checkboxes carry done-state
- must not frame or report the work as *closing* / *finalizing* the track — report per iteration (*did X, Y; Z remaining*); the track is open-ended (add iterations freely), never pushed toward closure

## Template — copy below the line

---

# p{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** Planned

## Iteration 1 — Content-type registry

- [ ] Slim the registry
  - [ ] drop the dead `fields` / `FieldKind` from `registry.ts`
  - [ ] split the monolithic type list per file
- [ ] Relocate the wire models
  - [ ] `CreateCodeRequest` / `UpdateCodeRequest` → `integration/codes/models`

## Iteration 2 — Design view

- [ ] Extract background controls
  - [ ] `BackgroundControls` out of `DesignView` → a `ControlGroup`
