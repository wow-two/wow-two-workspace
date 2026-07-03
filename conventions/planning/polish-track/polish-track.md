# Polish Track

*Last updated: 2026-06-27*

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

- must group `## {area}` → `### {file path}` → `[ ]` tasks; areas are `Backend` / `Frontend` / `Database`, include only the ones touched
- must write each task as the file's concrete change, any size — `Split the render switch into per-format handlers`, not an abstract capability
- must not add a per-file status, ledger, or coverage map — a file may recur across iterations; git is the record
- must carry meta `**Status:** … · **Started:** … · **Completed:** …` — those three only, no `Type`

## Lifecycle

- `⏳ Planned` → `🚧 In Progress` → `✅ Complete`
- must open an iteration when planning it and close it when its tasks are done — set `Completed`, flip `Status`; one active at a time

## Rules

- must run opportunistically — no cadence, no timebox; batch any number of files, or none for a long stretch
- must plan only the active iteration — no speculative future docs
- must not keep a `## Log` — git is the history

## Template — copy below the line

---

# p{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** ⏳ Planned · **Started:** {YYYY-MM-DD} · **Completed:** —

## Backend

### `Codes/CodeRenderer.cs`

- [ ] Split the format switch into one handler per code type.
- [ ] Drop the dead `LegacyRender` overload.

## Frontend

### `screens/CreateCodeScreen.tsx`

- [ ] Extract the form state into a `useCodeForm` hook.

## Database

### `migrations/0003-billing.sql`

- [ ] Rename the migration to match the `AddBilling` intent.
