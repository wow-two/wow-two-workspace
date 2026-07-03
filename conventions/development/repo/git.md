# Git

*Last updated: 2026-07-03*

> Commit-message format for every repo under `wow-two-ws/`.
> Purpose — a uniform, scannable history whose subject reads as *what changed*, in the past tense.

## Message

- must write the subject as `{type}: {past-tense verb} {what}` — e.g. `feat: added billing checkout endpoints`, `chore: refactored the codes repository`, `fix: corrected the redirect device match`.
- must use a **past-tense** verb (`added` · `refactored` · `fixed` · `removed` · `renamed` · `updated` · `moved`) — not imperative (`add` / `refactor`).
- must name the concrete thing changed — precise + brief; lowercase except identifiers; no trailing period.
- must not be vague (`fix: fixed a bug`) or a run-on (`feat: added X and Y and also Z …`) — one named, cohesive change.

---

## Type

- `feat` - a new capability · `fix` - a bug · `refactor` - a behavior-preserving change · `chore` - tooling / deps / moves / config · `docs` · `test` · `perf`.
- must pick the type by the change's intent, not the files it happens to touch.

---

## Scope

- must scope one commit to one cohesive change (one lane / concern) — split unrelated work into separate commits.
- may add a body (blank line, then compact `- {area} - {what}` bullets) for a larger change — the *what* + *why*, never the *how*.

---

## Discipline

- must commit / push only when asked — the developer manages git.
- parallel-lane rules (assume-intentional · no-revert · stage only your own files): [../../agentic-workflow/agentic-workflow.md](../../agentic-workflow/agentic-workflow.md).
