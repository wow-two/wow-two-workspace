# Git

*Last updated: 2026-07-05*

> Commit-message format **and** the agent⇄human commit protocol, for every repo under `wow-two-ws/`.
> Purpose — a uniform, scannable history whose subject reads as *what changed* (past tense); and one unambiguous rule for who commits (the human, always).

## Message

- must write the subject as `{type}: {past-tense verb} {what}` — e.g. `feat: added billing checkout endpoints`, `chore: refactored the codes repository`, `fix: corrected the redirect device match`.
- must use a **past-tense** verb (`added` · `refactored` · `fixed` · `removed` · `renamed` · `updated` · `moved`) — not imperative (`add` / `refactor`).
- must name the concrete thing changed — precise + brief; lowercase except identifiers; no trailing period.
- must not be vague (`fix: fixed a bug`) or a run-on (`feat: added X and Y and also Z …`) — one named, cohesive change.
- must keep the subject **50–70 characters**, type prefix included — GitKraken truncates past 70, and the subject is what the developer reads in the graph.
- must ship the **subject alone, never a body** — a change that will not fit one 70-character line is two commits, not a paragraph.

---

## Type

- `feat` - a new capability · `fix` - a bug · `refactor` - a behavior-preserving change · `chore` - tooling / deps / moves / config · `docs` · `test` · `perf`.
- must pick the type by the change's intent, not the files it happens to touch.

---

## Scope

- must scope one commit to one cohesive change (one lane / concern) — split unrelated work into separate commits.
- must not add a body — a subject that cannot carry the change means the commit is too big; split it.

---

## Large files

A binary in git is permanent. Every later version of it stays in the pack forever, and every clone pays for all of them. The decision is made **before the first commit that introduces it**, because after the first push the only fix is a history rewrite.

Route a file over **1 MB** by asking one question — *can it be regenerated?*

| The file | Route |
|---|---|
| Regenerable from a script in the repo (a bake, a build, a dump) | gitignore it; the script is the source of truth |
| Regenerable, but the product promises a clone that runs with no bake and no network | **LFS** |
| Not regenerable — a supplied export, a licensed asset, a captured fixture | **LFS** |
| Text that diffs and compresses — `.sql`, `.csv`, `.jsonl`, `.json` | plain git, whatever the size |
| Under 1 MB | plain git — LFS is not worth its client dependency at that size |

- must run `git lfs install` and `git lfs track` **before** staging the file, never after — `.gitattributes` only governs what has not been committed yet
- must commit `.gitattributes` in the same commit as the first tracked binary
- must track by extension, not by path — `*.pmtiles`, not `public/tiles/*.pmtiles`; a moved file silently leaves LFS otherwise
- must state the LFS requirement in the repo `README.md` — a clone without `git-lfs` checks out **pointer text**, and the failure is silent until something reads the file
- must watch the GitHub free tier — 1 GB storage and 1 GB/month bandwidth per account, and every CI checkout spends bandwidth
- should keep a large artefact out of git entirely when a release asset or an object store will do — LFS is the answer when the file must be *in the tree*, not merely *available*

Repairing a binary already in pushed history:

- must treat it as a rewrite, never a `.gitattributes` add — the blobs are in the pack and adding a pattern changes nothing
- must run it **before parallel lanes open** — a rewrite mid-flight strands every other chat's local branch
- must expect every SHA from the first affected commit onward to change, and must re-point the commits cited in the repo's own docs
- must measure first — `git lfs migrate info --everything --above=1MB` names the patterns and their weight
- the rewrite itself is `git lfs migrate import --everything --include="…"` followed by a force-push, and it is the **developer's** to run (see *Discipline*)
- must run **`git lfs checkout`** after the migrate — it leaves every tracked file in the working copy as a 133-byte pointer, and nothing warns you; the app 404s its own assets until the smudge runs
- must not trust a backup ref through a rewrite — `--everything` rewrites `backup/*` too, and a following `gc --prune=now` deletes the originals; clone the repo elsewhere first if a rollback is wanted
- must re-point every commit SHA the repo's own docs cite — map old to new by commit subject, `git log --oneline --grep`

---

## Discipline

- **must not** ever run `git commit`, `git push`, `git reset --hard`, force-push, or `git stash drop/pop` — the human is the **only** one who commits + pushes. Enforced by the `guard-git` PreToolUse hook ([../../../../.claude/hooks/guard-git.py](../../../../.claude/hooks/guard-git.py)).
- **may** run `git add`, `git restore --staged`, `git status`, `git diff`, `git log` — staging + inspection are the agent's job.
- must not stage unprompted — finishing work is not the cue. Report the changed paths and stop; the human asks when they want an index.
- must treat "commit this" / "push it" / "stage it" as the cue to **prepare** (stage + draft the message), **not** authorization to run the command.
- parallel-lane rules (assume-intentional · no-revert · stage only your own files): [../../../agentic-workflow/agentic-workflow.md](../../../agentic-workflow/agentic-workflow.md).

---

## Protocol (agent ⇄ human)

Per commit, in this order:

1. agent **carves the index** — `git add <explicit paths>`, `git restore --staged <paths>` to drop strays.
2. agent prints the **staged path list** + the commit message (`{type}: {past-tense} {what}`), then **stops**.
3. human reviews, commits, and pushes.
4. repeat from 1 until the tree is clean.

- **carve** = shape the index so the staged set is exactly one lane's cohesive change, nothing else.
- read the result with `git status --short` — staged column commits, unstaged column stays behind.
- must not `git add -A` / `-u` / `.` — a pathless add sweeps in another lane's half-done work.
- must print the staged paths, not only the message — a shared index makes the message alone unprovable.
- must re-check `git status` right before printing — a concurrent lane can stage between add and report.
- must not `git restore --staged` a path it did not stage this session — that de-carves another lane's commit.
- found foreign paths staged → report them; don't quietly unstage.
- must keep each commit buildable where practical; flag a split that can't be (e.g. rename-only) before staging.
