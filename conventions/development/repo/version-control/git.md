# Git

*Last updated: 2026-07-05*

> Commit-message format **and** the agent⇄human commit protocol, for every repo under `wow-two-ws/`.
> Purpose — a uniform, scannable history whose subject reads as *what changed* (past tense); and one unambiguous rule for who commits (the human, always).

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

- **must not** ever run `git commit`, `git push`, `git reset --hard`, force-push, or `git stash drop/pop` — the human is the **only** one who commits + pushes. Enforced by the `guard-git` PreToolUse hook ([../../../../.claude/hooks/guard-git.py](../../../../.claude/hooks/guard-git.py)).
- **may** run `git add`, `git restore --staged`, `git status`, `git diff`, `git log` — staging + inspection are the agent's job.
- must treat "commit this" / "push it" / "get it pushed" as the cue to **prepare** (stage + draft the message), **not** authorization to run the command.
- parallel-lane rules (assume-intentional · no-revert · stage only your own files): [../../../agentic-workflow/agentic-workflow.md](../../../agentic-workflow/agentic-workflow.md).

---

## Protocol (agent ⇄ human)

Per commit, in this order:

1. agent stages exactly one cohesive change — `git add` / `git restore --staged` to carve the index by lane / path; never a blind `git add -A` that bundles unrelated work.
2. agent prints the commit message (`{type}: {past-tense} {what}` subject + optional body) in chat, then **stops**.
3. human reviews, commits, and pushes.
4. repeat from 1 for the next commit until the tree is clean.

- must keep each commit buildable where practical; when a split can't (e.g. a rename-only commit that won't build alone), say so before staging it.
