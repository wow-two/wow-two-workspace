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

## Handoff docs — write-once, read-once, delete [REQUIRED]

A handoff (`handoff.md`) exists for exactly one purpose: **loading a fresh chat with the context the previous chat is about to lose.** It is a courier, not a record. The track doc is the record.

- must write it only when a chat is ending with work in flight, and only for the chat that picks that work up.
- must not maintain it. A handoff updated turn by turn has become a second plan doc, and it will disagree with the track doc — the numbering drift that produced a phantom "Iteration 7.5" started exactly this way.
- **the chat that loads a handoff owns its disposal.** On load: move anything durable into the track doc (a settled fork, a measured figure, a trap worth keeping), then **delete the file**. Everything else was transport.
- must not let two chats load the same handoff. Once read, it is spent; a second reader is reading a stale snapshot of a tree that has moved.
- must delete it on load when nothing in it is durable — a handoff carrying only what the track doc already says has already done its job, and keeping it guarantees a later reader trusts the older of two records.
- must never cite a handoff as the source of a decision. If a decision only lives there, it was never recorded — move it to the track doc first.

**Precedence:** track doc > handoff, always. A handoff that contradicts the track doc is wrong by definition, whichever is newer.

Distinguish it from the version-track's **transient iteration plan** (`v{X.Y}/{iter-slug}.md`), which is also delete-when-done but serves the *current* chat's own build, not the next chat's start.

---

## Task form — shared by all tracks

- must write each task **verb-first** — a concrete action, never a noun phrase or an `X → Y` mapping. `Move api.ts to integration/`, not `api.ts → integration`.
- must keep **one action per bullet** — split a multi-part change into separate bullets. More bullets is fine; density comes from fewer words per task, not fewer tasks.
- must use the fewest words that name the action + its target; backtick identifiers, drop restatement.
- must cap a task line at **75 characters**, counting the `- [ ] ` marker. A task that will not fit is not one action, or it is carrying detail that belongs elsewhere.
  - over the cap → **split** it into two tasks, or **drop the detail**; move it into the doc's decision / architecture section only when it is still load-bearing.
  - **detail about work already done gets deleted, not relocated.** The compact task line is the record that the capability shipped; git holds how. Relocating it trades task sprawl for prose sprawl and the doc grows either way.
  - relocate only what a *future* reader needs to decide something: an open fork, a constraint that still binds, a rejected option and why. A version number, a test count, or a defect mapping for closed work is history — cut it.
  - never wrap a task across lines to satisfy the cap — the cap measures scope, and wrapping only hides that the scope is wrong.
- must not carry an em-dash clause, a parenthetical rationale, a quote, or a file:line reference in a task line. Those are the detail the cap is excluding; the section above the checklist is where they belong.
- may sit a `- [ ]` **sub-step** under a task, under the same cap, when the *how* needs itemizing.

```markdown
<!-- ❌ Wrong — 4 facts, a rationale, and a file ref on one line -->
- [ ] **Thin `CodePayload` down** *(shifted from Iteration 6)* — drop the `?? string.Empty` fallback once validation guarantees it; rehome `SlugPlaceholder` off the controller

<!-- ✅ Correct — one action each, rationale lives in the decision section -->
- [ ] Drop the `CodePayload` empty-string fallback
- [ ] Rehome `SlugPlaceholder` off the controller
```

Each track adds the task **grain** on top of this form — polish = a concrete file change, version = a user-facing capability, rough = a whole subsystem (a version's worth of work), vector = one concrete piece of a ladder stage.
