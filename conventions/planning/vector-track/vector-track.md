# Vector Track

*Last updated: 2026-08-12*

A per-vector build doc — one durable subject lane, the stage ladder it climbs, and the seams it exposes to the other lanes.

`rough`, `version` and `polish` decompose a product by **time**: iteration 1, then 2, then 3. That ordering is the plan, and it is also why the work resists parallel chats — a linear plan declares no seams, so nothing says what two workers may each touch. This track decomposes by **subject** instead. The axis is the vector; the cadence inside it is still one of the other three.

## When to use it

- must use it when a product has **3+ subsystems that advance independently** — surfaces, verticals, foundation
- must use it when work runs in **more than one chat at a time**
- must not use it on a single-subsystem product — one lane is a `rough` / `version` track with extra ceremony
- must not use it to replace `rough` / `version` / `polish` — a vector runs one of them internally

## Concurrency model

| Level | Shape | What it needs |
|---|---|---|
| across vectors | **parallel** — one chat each | disjoint `Owns:` sets |
| within a vector | **linear** — the stage ladder | nothing; this is what keeps a chat coherent |
| within a stage | **agent fan-out** | mechanically parallel · self-verifiable · disjoint files |

- must keep a vector's own progress linear — the chat's value is that its back-and-forth reads as one thread
- must not parallelise stages inside a vector to go faster — that rebuilds the mixed-subject chat this track prevents

## The cut

**A vector is a subsystem one person owns for weeks, not a topic the product contains.** Getting this wrong is the failure mode of the whole track: cut too fine and every real fix spans three lanes, so the seams outnumber the work and the developer reviews a coordination problem instead of a product.

- must cut by the **subsystem**: a surface, an end-to-end vertical, the foundation
- must not cut by **dataset, source, or domain group** — a dataset is a rung inside the vertical that consumes it
- must not cut by **layer** — `frontend` / `backend` / `pipeline` splits one subject across three chats
- must keep the **total ≤ 5**, In-Progress or not — a lane nobody will open is a label, and 5 is what one reviewer holds
- must fold a lane carrying no scope in the next two releases into the lane that consumes it
- must **confirm a vector outside the planned set with the developer before opening it** — a new lane takes files out of the sets the other lanes already hold, so adding one is a re-cut of the whole board, never an addition to it. Post the proposed `Owns:` set and what it removes from whom; a chat that needs files it does not own raises a seam instead
- must not let a chat create `{vector}/{vector}.md` for an unlisted vector — the folder existing is what makes the lane real
- must test a proposed cut against its seams: **no seam may span more than 2 vectors** — a 3-lane seam means the cut runs through the middle of one subject

## Scope

- must own an exclusive file-glob set, declared `**Owns:**` — no file belongs to two vectors
- must declare `**Consumes:**` — the artefacts it reads from other vectors, named
- must hold **≥ ~1 month** of work — anything smaller is a stage, not a vector
- must not open a vector that owns no files — with no `Owns:` it is a topic, not a lane
- must not open a vector for a one-off whole-tree job — a port, a rename, a framework bump runs single-lane first
- must leave docs that plan nothing off the board — research, marketing and pitch material are not engineering lanes

## Location & naming

- must place each vector at `engineering/planning/vector-track/{vector}/{vector}.md` — one folder per vector
- must keep the lead doc at `engineering/planning/vector-track/vector-track.md` — the table, the release cuts, the seams
- must name a vector for its **subject** — lowercase, one word where possible: `map`, `layout`, `simulation`, `platform`
- must not version a vector — a vector is durable; versions live inside it

## Archetypes

A vector's stages come from its archetype, never from the instance. Three ladders, and a product adds a fourth only when a vector fits none of them.

| Archetype | Stages | Is |
|---|---|---|
| `surface` | manifest → load → render → interact → perf | what the user looks at and touches |
| `system` | acquire → model → serve → render → verify | one vertical, source to screen, including its own rendering |
| `platform` | foundation → contract → expose | host, persistence, tooling, shared state, the build |

- must declare one archetype on the meta line
- may skip a stage the vector does not need; must not reorder them
- must add a new archetype **to this file** when a second vector wants the same ladder — never invent stages per vector
- must not carry a stage the vector will never reach
- must read `system`'s `render` as **the vertical's own output layers**, never the host surface's primitives — the surface owns the canvas, the icon set and the zoom logic, and publishes them as an API

## Grain

| Track | An iteration is | A task is |
|---|---|---|
| `polish` | a batch of related files | one concrete file change |
| `version` | a group of related capabilities | one user-facing capability |
| `rough` | one feature | one concrete piece of that feature |
| **`vector`** | **one rung of the ladder** | **one concrete piece of that rung** |

- must size an iteration at **2–6 tasks**
- must not write sub-steps — the *how* is decided when the task is picked up
- must carry the **catalogue id** on every task where the product keeps a catalogue — a task with no id is work the lane invented, and it is invisible to every other lane
- must not write a task into a lane doc **in place of doing it**, unless a named blocker stops it — writing it down reads as progress and the item is then found only by whoever reopens the doc
- must follow the shared **Task form** — verb-first, one action per bullet ([planning-conventions.md](../planning-conventions.md))

## Seams

A seam is the only way two vectors touch.

- must route a cross-vector need through the seam — post the artefact needed, the owning vector supplies it
- must declare the artefact's shape **before** the consuming vector builds against it
- must not edit outside `Owns:` — a break rooted in another vector is a hand-off ([agentic-workflow.md](../../agentic-workflow/agentic-workflow.md))
- must record an open seam under `## Seams` in **both** vector docs — the artefact + the stage waiting on it
- must resolve a file two vectors both want by **moving it into one `Owns:` set** — never by coordinating access
- must re-cut the vectors when a seam reaches 3 lanes — see § *The cut*

## Chats & agents

- must run **one chat per vector** — its questions share a subject, so the developer answers from one loaded context
- must not open a coordinator chat that reads every vector — the lead doc is the join, not a chat
- must fan out agents inside a stage only when the work is mechanically parallel, self-verifiable, and writes disjoint files
- must have each agent report in three lines — **changed · green · needs-decision**
- must queue a `needs-decision` to the vector doc, never answer it mid-fan-out

## Git

The index is a single shared object. Every chat in the tree writes to the same one, so two lanes staging at once produce a commit carrying both.

- must stage a single lane's files, only when the developer asks — paths from that vector's `Owns:` set and nothing else
- must hand the commit and the push to the developer ([git.md](../../development/repo/version-control/git.md))
- must leave an unexpected change alone and report it — it is another lane's in-flight work

## Build

**A tree with four lanes in it is red most of the time. Red is the resting state, not a failure.**

The deadlock this prevents: lane A pauses mid-task because its solution will not build and waits on lane B; B finishes, and now *its* build fails on A's half-written file. Both are blocked, and neither break is repairable by the lane that hit it.

- must complete the task in hand before building — implement → build → verify → implement the next
- must not pause mid-task to wait on another lane — a half-written file is what turns a wait into a deadlock
- must leave the lane's work compiling **the moment the other lane lands**, even while the solution is red
- must retry a failed build once after ~30 s; on a second failure rooted outside `Owns:`, carry on and retry later
- must read a break rooted outside `Owns:` as a lane in flight, never as a defect to repair

A retry fixes a compile failure. It cannot fix two builds racing one `obj/`. A **full-solution build or full test run takes a token first** — a directory, because `mkdir` creates or fails in one atomic step where a file can be read by both lanes.

```bash
mkdir .vector/build.lock 2>/dev/null || exit 1   # someone else is building
trap 'rmdir .vector/build.lock' EXIT
```

- must wrap the build in **one sanctioned script** — `scripts/build.sh` takes the token, builds, releases
- must release the token when the build ends, green or red; must reclaim one older than 10 minutes
- must put the token at `.vector/` in the repo root, gitignored — never inside the tracked `vector-track/`
- may run a lane-local check without the token — `tsc --noEmit`, a single project, the lane's own tests

## Shared state

| Shared thing | Rule |
|---|---|
| `Directory.Packages.props` · `*.slnx` · root `package.json` | owned by `platform`; another lane requests the change on the seam |
| Migrations | reserve the number on the seam before writing the file |
| DI registration, layer manifests, any append-only list | each lane appends its own line; never reorder another lane's |
| Dev server ports | one lane runs the app; the others read the running instance |
| Dependency bumps | `platform`'s call, announced on the seam before landing |

## Structure

- must group `## Iteration {N} — {rung}` → `- [ ]` **task**, one line, no nesting; `{rung}` is the ladder word
- must call the group an **iteration**, never a stage — every track names its group an iteration, and one word across the four is what lets a reader move between them. `{rung}` names *which* rung it climbs
- must carry meta `**Archetype:** … · **Status:** … · **Owns:** … · **Consumes:** …` — those four only
- must carry a **one-word** `**Status:** {Planned | In-Progress | Done}` — no dates, no per-iteration summary
- may append a `> {note}` under an iteration for a seam dependency or a lane marker, never for rationale
- must not add a per-task status, ledger, or coverage map — git is the record

## Lifecycle

- `Planned` → `In-Progress` → `Done` — one word, no emoji, no dates
- must **verify a rung's completion with the developer** — Claude never self-declares it
- must move a vector blocked on a seam to its next unblocked rung — a blocked chat never idles waiting
- must **reopen** an iteration for a deferred-but-in-scope item — it never justifies advancing
- may **drop a completed iteration's tasks**, keeping the bare heading — git holds the detail
- must retire a vector by marking it `Done` and leaving the doc — the `Owns:` set is the record of who held those files

## Releases

A release is a **cut line across vectors**, not a vector's own version.

- must name each release in the lead doc as `{version} = {vector}@{rung} · {vector}@{rung} · …`
- must cut a release only on rungs, never mid-rung
- must not hold every vector to the cut — a vector past its named rung keeps going

## Lead doc

- must carry every **unmet prerequisite** under `## Establishing`, each with an owning vector — the track is set up by whichever chat opens first, and it reads the gaps there
- must keep `## Establishing` while anything in it is open; it disappears when the last box ticks
- must carry every open seam under `## Seams` — the lead doc is the join between lanes
- must not carry diagnosis, defect narrative or demo notes — those live in the catalogue and the vector docs
- must not keep a `## Log` — git is the history
- must write a handoff doc when a chat's context fills — the plan never carries session state

## Template — lead doc

```markdown
# Vector Track

*Last updated: {YYYY-MM-DD}*

Convention: [`vector-track.md`](…/conventions/planning/vector-track/vector-track.md).

| Vector | Archetype | Rung | Status | Owns |
|---|---|---|---|---|
| [`map`](map/map.md) | `surface` | render | In-Progress | `presentation/map/**` · `public/tiles/**` |
| [`simulation`](simulation/simulation.md) | `system` | serve | Planned | `*/Simulation/**` · `data/*.py` |

## Establishing

- [ ] {prerequisite} — `{owning vector}`. {why the track is unusable without it}

## Seams

- `{artefact}` — {who declares it, who consumes it, which rung waits}.

## Releases

- `v0.3` = `map@perf` · `simulation@serve`
```

## Template — vector doc

```markdown
# {vector} — {Subject}

*Last updated: {YYYY-MM-DD}*

**Archetype:** `system` · **Status:** Planned · **Owns:** `{glob}` · **Consumes:** `{artefact}` (`{vector}`)

## Iteration 1 — Acquire

- [ ] {verb-first task}

## Iteration 2 — Model

> Blocked on `{artefact}` from `{vector}`.

- [ ] {verb-first task}

## Seams

- `{artefact}` — {shape}, needed before Iteration {N}. Owner: `{vector}`.
```
