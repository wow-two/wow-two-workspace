# Remarks

*Last updated: 2026-08-15*

> The `<remarks>` block — the detail a one-sentence `<summary>` cannot carry. Never required, and held to the same three gates as a `<summary>`.

## Never required [REQUIRED]

`<remarks>` is **optional on every type-kind**. No table, no row, no component mandates one. A type earns a `<remarks>` by having something the summary cannot hold, and most types do not.

- must not add a `<remarks>` because a component-kind seems to warrant one — a `Service` or `Repository` with a sufficient summary carries none.
- must omit it entirely when the summary already says enough.

## What it carries

Three things, and nothing else:

- **a directive** — what a consumer must do to use this correctly. Open with an imperative: `Use with …`, `Wire via …`, `For X, prefer …`.
  - ✅ `For Postgres, prefer <see cref="IHasXmin"/> instead.`
- **a specification reference** — the RFC, spec, or vendor document the shape answers to. Name it; do not restate what it says.
  - ✅ `Follows RFC 5322 for the header set.`
- **genuine complexity** — an interaction, constraint, or ordering a reader cannot infer from the signature and would get wrong.
  - ✅ `Attach before mutating — attaching after snapshots the mutation as the original.`

Everything else is cut:

- ❌ rationale for how the code is written — that is a `//` beside the code
- ❌ provider or framework behavior stated as trivia — `Maps to SqlServer's 8-byte rowversion column; EF Core throws DbUpdateConcurrencyException when the stored value drifts from the original.`
- ❌ who sets the value, when, or how
- ❌ anything the `<summary>` already carries

`<remarks>` is exempt from the falsifiability test ([summary](summary.md) § *The falsifiability test*) — a directive is allowed to describe the present.

## Frames — the shapes that recur

Ten frames, each answering a different question the signature leaves open. Counts are occurrences across every repo in the workspace, so these
are the codebase's own idioms rather than invented ones. Reach for the frame whose question the reader is actually asking; a `<remarks>` that
fits none of them is usually rationale, which § *Everything else is cut* already removes.

| Frame | Opener | Answers | Carrier | n |
|---|---|---|---|---|
| Read-as | `Read … as` · `Treat … as` | how to interpret the value | directive | 69 |
| Invariant | `Every …` | what always holds | complexity | 36 |
| Default state | `Defaults to …` · `Off by default.` | what happens when nothing is set | complexity | 21 |
| Empty / null | `Returns … when …` · `Nothing …` | the boundary case | complexity | 20 |
| Display | `Render …` | how a UI must present it | directive | 17 |
| Wiring | `Register …` · `Call … before …` · `Set …` | what must be configured, and in what order | directive | 16 |
| Prohibition | `Never …` | the one thing that breaks it | directive | 12 |
| Selection | `Use … only for …` | which of several to reach for | directive | 10 |
| Re-run safety | `Idempotent — …` · `Re-run freely — …` | whether repeating is safe | complexity | 7 |
| Spec | `Follows {SPEC} …` | which standard binds the shape | spec reference | — |

**The corrective is a modifier, not a frame.** `…, never Y` / `…, not Y` runs 489 times and attaches to *any* frame above — it names the wrong
reading the sentence is displacing. `Read free-flow off the observed speed_90, never off the maxspeed tag.` is a Read-as carrying one.

- must open a **Prohibition** at the start of the sentence — `Never …`. A mid-sentence `, never …` is the corrective modifier, and the two mean different things: one forbids a call, the other corrects a reading.
- must keep `only` in a **Selection** — `Use for idempotent calls only` selects; `Use AddResilientClient` merely wires.
- must not aim a `<remarks>` at the next editor — `Keep … in lock-step` is a maintainer fact and ships to every consumer through IntelliSense. It belongs in a `//` beside the code ([documentation](documentation.md) § *Where a fact belongs*). 14 blocks in the workspace do this today.

## Multi-line — the same three gates [REQUIRED]

A `<remarks>` earns extra lines the way a `<summary>` does: it clears **convention → compaction → length**
([documentation](documentation.md) § *Three gates, in order*). Readability is not a ground, and a numbered flow is not a licence —
it is a block that still has to survive gates 1 and 2 before length is even asked.

- must not wrap a block that has not cleared gates 1 and 2 — a multi-line `<remarks>` is evidence they were skipped.
- must cap at **5 lines, tags included**. No exception, numbered flow or otherwise. A flow needing more is a doc page: move it to the
  module's `.standard.md` and reference it.
- must cut any step the caller cannot act on — the flow states what a consumer must know, never the implementation's itinerary. That cut
  is gate 1, and it is what brings most flows under the cap.

```csharp
// ✅ 5 lines, tags included — the "Seed flow:" preamble and the internal steps cut at gate 1
/// <summary>Provides channel and pipeline seeding on application startup.</summary>
/// <remarks>
///   1. Read channels from the seed file
///   2. Upsert channels and sources via EF Core
///   3. Insert missing pipeline rows with code defaults
/// </remarks>
```
