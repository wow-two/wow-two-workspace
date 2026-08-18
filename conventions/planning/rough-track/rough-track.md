# Rough Track

*Last updated: 2026-08-05*

A per-version build doc — the subsystems a product stands up in one unbounded build pass, before anything is decomposed.

Named for the construction rough-in: every system run and working, nothing covered, nothing trimmed. The finish trades come later and they are different tracks.

## When to use it

- must use it to bring a product from nothing (or from a pivot) to a **whole working system**, fast, with no feature decomposition
- must hand off in order — `rough` → `polish` (optional) → `version`
- must not open a version track while a rough track is active — there is nothing stable to version yet
- must not use it for incremental work on a settled product — that is `version-track.md`

---

## Location & naming

- must place each version at `engineering/planning/rough-track/r{X.Y}/r{X.Y}.md` — one folder per version, file named after its folder
- must keep the lead doc `engineering/planning/rough-track/rough-track.md` — the active version + a link to this convention
- must start at `r0.1`; minor-increment `Y`; bump major `X` only at `Y = 100`
- must treat the latest folder as the active one

---

## Scope

- may change behavior freely — this track builds what does not exist yet
- must keep the platform **running at the end of every iteration**, never necessarily at the end of every task
- must not refactor for its own sake — reshaping existing code is `polish-track.md`
- must not extract to an SDK — extraction is decided at the seam, after the track closes
- must not decompose into user-facing features — that is the version track's grain

---

## Grain

The three tracks differ in grain. This is the whole distinction:

| Track | An iteration is | A task is |
|---|---|---|
| `polish` | a batch of related files | one concrete file change |
| `version` | a group of related capabilities | one user-facing capability |
| **`rough`** | **one feature** | **one concrete piece of that feature** |

- must size a rough **iteration** at one feature — a large feature may take 2–3 iterations, a small one never takes more than one
- must size a rough **version** at **5–15 iterations**, shipping **3–15 features** depending on their size
- a rough version is worth several version-track versions; the same feature that fills one rough iteration is a whole `v{X.Y}` later
- must not write sub-steps — the *how* is decided when the task is picked up, not when the doc is written
- must keep tasks flat, 2–5 per iteration
- must follow the shared **Task form** — verb-first, one action per bullet, fewest words ([planning-conventions.md](../planning-conventions.md))

---

## Structure

- must group `## Iteration {N} — {name}` → `- [ ]` **task**, one line, no nesting
- must name the iteration for its area — a bare noun, no `: {goal}` clause, no status tag
- must carry a **one-word** `**Status:** {Planned | In-Progress | Done}` and nothing more — no dates, no per-iteration summary
- may append a `> {note}` under an iteration for a dependency or a lane marker, never for rationale
- must not add a per-task status, ledger, or coverage map — git is the record

---

## Lifecycle

- `Planned` → `In-Progress` → `Done` — one word, no emoji, no dates
- must resolve each finished task to exactly one of three outcomes, decided with the developer:
  - **commit** — it stands, tick it
  - **verify** — it needs proving before it counts; it stays open
  - **move on** — it is good enough for rough; tick it and note nothing
- must not block the next task on the previous task's outcome — a rough track keeps moving
- must **verify completion with the developer** before marking an iteration done — Claude never self-declares it
- must not advance to the next version (`r0.2`) until the current is `Done` **and** the developer says to proceed
- may **drop a completed iteration's tasks** once the iteration is done — keep the bare `## Iteration N — Name` heading; git holds the detail

---

## Rules

- must order iterations by **dependency**, not by value — the ordering is what gets cut when the clock runs out
- must scope a version to a coherent slice that gets the app somewhere, never to the whole intended system
- may name the versions that follow in the lead doc, one line each — never write their docs ahead of need
- must not spin up a speculative `r0.2` ahead of need
- must not keep a `## Log` — git is the history
- must not frame the work as *closing* or *finalizing* — report per task (*built X, Y; Z remaining*)
- must write a handoff doc when the chat's context fills — the plan never carries session state

---

## Template — copy below the line

---

# r{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** Planned

---

## Iteration 1 — Layer registry

- [ ] Emit a manifest carrying delivery kind, style, provenance and zoom bands per layer.
- [ ] Switch the client loader on delivery kind.
- [ ] Drive level of detail from one aggregation rule rather than per-layer code.

---

## Iteration 2 — Coverage labels

> Depends on Iteration 1.

- [ ] Seed a multi-source shortest path from every stop at cost 0 and relax once.
- [ ] Cut at the bus and metro thresholds and store the label per node.
