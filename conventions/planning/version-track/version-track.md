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

## Prose inside a version doc [REQUIRED]

The task-form rules govern task lines. This governs everything else on the page, which is where residue actually accumulates.

- must keep a **completed** iteration's prose to zero. Its compact task lines are the whole record; a `>` blockquote or a standing paragraph under a done iteration is residue whether it was written last week or at the start.
- must not carry a fact in a version doc that outlives the version. A version doc is time-scoped and gets archived; these are not, and each has a real home:

| Residual fact | Home |
|---|---|
| Design tokens, palettes, type scales | the design system / `@theme`, never a version doc |
| A deferred item and why | the backlog in `engineering-planning` |
| A known coverage gap or stub | the test suite's own doc, or an open task |
| A dated verification run | the `**Completed:**` meta field, which already holds it |
| An architectural constraint that still binds | `engineering/architecture/` |

- must not restate meta in the body — a run date, a status, or a completion date belongs in the `**Status:** …` line and nowhere else.
- must not keep **re-scoping history** — no `**Rescoped {date}** — X moved to v0.9`, no note that an item arrived from elsewhere, no record of what a version used to contain. A task moves between iterations and versions many times as priorities shift; each move would leave a note, and the notes outnumber the tasks. **The current task list IS the scope**, and git holds every earlier shape of it. This is the same rule as *must move an item, never leave a forwarding stub*, applied to the version as a whole.
- may keep prose under an **open** iteration when its open tasks need it, and must delete that prose when the iteration closes.

## Lifecycle

- `⏳ Planned` → `🚧 In Progress` → `✅ Complete`
- must open a version when planning it and close it when its tasks are done — set `Completed`, flip `Status`; one active at a time
- must not advance to the next version until the current is `✅ Complete` **and** the developer explicitly says to proceed — never pre-declare, queue, or auto-begin the next version (in chat or in the plan); finish, report, and stop
- must **verify completion with the developer** before marking a version / iteration complete — never self-declare it
- must treat a `Verification` iteration's checks as the **developer's manual pass** — they tick on the developer's word, not on evidence in the tree; every other task ticks only on shipped code
- must **move an unshipped task to the next version** when closing a version — a closed version's task list describes only what shipped. Carry it to the iteration whose focus it fits, or open a new one named for that focus; never name the new iteration after where the task came from, and never leave a note that it moved
- must not apply that rule **within** an open version — a closed iteration inside an in-progress version may sit beside open ones, since iterations are not worked in order
- must **strip a completed iteration's sub-steps** once verified — a sub-step itemizes *how* to build something already built, so it is spent the moment the iteration closes; git holds it
- must leave the completed iteration's **tasks** in place, one compact line each, as the record of what the version delivered — rewrite any that were never compact rather than carrying the sprawl forward
- may drop the tasks too once the whole version is `✅ Complete`, keeping the bare `### Iteration N — Name` heading

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
