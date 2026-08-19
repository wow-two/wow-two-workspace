# Handoff — frontend conventions

*Last updated: 2026-08-19*

> **Read once, drain it, delete it.** The conventions reached their intended shape today.
> What is left is six decisions, a code sweep, and a compaction pass.

## State

`conventions/development/frontend/` — **360 docs**, and every mechanical check passes:

| Check | Result |
|---|---|
| relative links resolve | 0 broken |
| `§ *Section*` references | 82, 0 broken |
| reachable from the index | 360 / 360 |
| missing `*Last updated:*` | 0 |
| lines over 120 characters | 0 |

The tree splits **twice, orthogonally**, mirroring the backend:

```
frontend/
  frontend-conventions.md
  core/    core.md · lla/ · mla/ · hla/     — how far a rule reaches
  shapes/  shapes.md · app/ · library/      — what kind of thing is built
```

`core/mla/` splits again by **register**: `constructs/` defines a role, `components/` says which one to reach
for and with what values, and an instance's full surface stays in its `.spec.md` in the SDK repo.

---

## What changed today

- **Registers named.** definition · application · surface, stated once in `conventions.md` § *Three axes*.
  `layer` is reserved for `lla`/`mla`/`hla`; `bucket` and `register` are the other two axes.
- **One owner per rule** written into `conventions.md`, with the identity test: two docs may state different
  obligations about one topic, never the same one. 168 restatements removed across 75 docs.
- **`suffixes.md` dissolved.** Each kind doc owns its own `### Component name`; `visual.md` keeps the routing.
- **`mla/components/` rebuilt** as the application register — 232 component docs in 7 group folders.
- **`lla/components/` restored** on the backend's line: `lla/constructs` is the language form, `lla/components`
  is that form used end to end, `mla/*` is only what we invented.
- **All 7 backend forwards applied.** `fe-forwards.md` is drained.

---

## Open — needs a decision

Six rows in [fe-conventions-conflicts.md](fe-conventions-conflicts.md), each two live rules that disagree:

| # | What |
|---|---|
| 18 | `*State` — a component suffix and a hook's return type |
| 19 | `Skeleton` — claimed ✅ by both `state.md` and `feedback.md` |
| 49b | the primitive suffix — retiring `none` needs a suffix that does not exist |
| 56 | register bleed — 4 judgement rules sitting in definition docs |
| 62 | `*Field` provides the form context per the gate; all four consume it |
| — | `stepper` — the `forms/` lead says display, the body owns state |

---

## What is left, in order

1. **Compaction** — 279 `max-len` warnings in the SDK, by area: `router` 19 · `auth` 26 · `query` 26 ·
   `presentation` 64 · `foundation` 144. Gate first, compact second, wrap third — never wrap first.
2. **Code rows** — 27 in the SDK's
   [conventions sweep](workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/planning/ui-sdk-conventions-sweep.md).
   The largest: 134 components carrying no kind suffix, the result pattern (rows 12-14), 68 React-era specs.
3. **Instance content** — 14 role docs still document a specific instance's props or slots; that content
   belongs in each component's `.spec.md`.

---

## Uncommitted

`wow-two-ws` — the frontend conventions are staged, 115 files, message:
`docs: rebuilt the frontend conventions by scope and register`. The 240 new application docs are **not** yet
staged. Backend paths, `pln-tasks.md`, `active.sh` and the skills belong to other lanes — leave them.

The UI SDK repo carries the acronym renames (`JsonEditor` · `Fab` · `PdfViewer`), staged as renames.

---

## Do not

- **Do not `git push`.** The developer publishes.
- **Do not touch `conventions/development/backend/`** — another chat owns it. Two of its docs cite pre-move
  frontend paths (`serialization.md:7`, `launch-profiles.md:18`) and need that lane to repair them.
- **Do not restate a rule.** Grep the identifier first; link the owner instead.
