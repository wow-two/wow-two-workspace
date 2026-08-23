# Handoff — backend SDK conventions sweep

*Last updated: 2026-08-21*

> **Read once, act, delete.** Where the backend SDK sweep stands, what was settled, and the exact next move.
> Purpose — one session took the sweep from "the file is lost" to a green tree with a settled taxonomy.
> Use case — pick up `be-convention-sweep.md` and keep going without re-deriving any of it.

## State

`wow-two-sdk.backend.beta` — **328 tests passing, 0 failing**, build green, every options registration on one
recipe. The solution carries all 14 projects under `/Libraries/` and `/Tests/`; test runs execute as
`Development`, so the container validates on build and the IDE and terminal agree.

| Suite | Passing |
|---|---|
| `Data` · `Foundation` · `Identity` | 20 · 94 · 2 |
| `Mediator` · `Messaging` | 68 · 96 |
| `Migrations` · `Web` | 14 · 34 |

The sweep file is `wow-two-sdk.backend.beta/be-convention-sweep.md` — 88 rows, **32 open**. Rows carrying ✅
are shipped; the rest are the queue.

---

## Settled this session

Three docs hold it. Nothing below needs re-deciding.

- **`ideas/constructs-taxonomy-analysis.md`** — 34 logged iterations with what changed and why. Carries
  `operation · step · flow`, invertibility, the three service layers, the one location rule, and the
  product's four-project shape.
- **`conventions/development/backend/dotnet/core/mla/constructs/constructs.md`** — the keep-list plus the
  discriminators written this session: `Factory` vs `Mapper`, `static readonly` is a value, static-or-instance
  by two gates, role and shape, and the single `Repository` role.
- **`.../constructs/patterns/patterns.md`** — every pattern mapped to a role and a folder, 24 rows.

Decisions worth not relitigating:

- **`Repository` is the only store role.** Ownership, contract shape and composition were each tried and each
  read an implementation fact; a role carrying one renames when the engine swaps, which breaks the
  host-configuration swap the modular SDK is built on. The engine lives in the prefix.
- **`Result` is decided by failure mode, not role.** An operation with a failure mode wraps; one that cannot
  fail by construction returns bare. Config-at-boot and programmer errors stay exceptions, because the
  framework's own seams only catch what is thrown.
- **Options register one way** — `AddOptions<T>()` then project the record in the same `Add*`, so consumers
  take `T` and never `IOptions<T>`.
- **Foundation vocabulary is 12 role folders** and a pattern never gets a folder of its own.

---

## Next action

`N81` — **12 domain throws become `Result`**, one type at a time. Guards and the 9 config/programmer throws
(`N82`) are excluded and stay as they are.

```
Service 11 · Repository 6 · Mapper 1 · Adapter 1 · Validator 1 · Serializer 1   (21 total, 9 excluded)
ClaimCheckPayloadRepository 6 · MigrationRunnerService 5 · DbUpBackgroundService 4
```

Each conversion changes a contract and every caller, so they land one type at a time with the suite green
between them.

---

## The rest of the queue

- `N77` — smart-qr's solution folders are lowercase; the rule is now PascalCase.
- `N38` — 28 `// ── Section ──` banners become `#region`; the divider rule was replaced.
- `D3` · `D6` · `D7` — 143 `<para>` in 45 files, 119 `<remarks>` over the 5-line cap, 12 files using `<list>`.
- `N52` — 18 files carry `<example>`, which the notation rules ban.
- 26 product rows (`N1`-`N37`, `R6`, `C1`-`C7`) target smart-qr and belong to that repo's lane.

---

## Raised as tasks

In `10x-ws/system/planning/pln-tasks.md`, Career section:

- `car-t-012` — ProblemDetails creation behind an interface; the mapping will branch per error kind.
- `car-t-013` — one registration mechanism for `Options` and `Settings`, validation first.
- `car-t-011` — diagnostics construct doc, which `MessagingMeterConstants` no longer waits on.

---

## Working agreements

- **Refine in the chat, store settled points in the doc.** Iteration in a file is slower and hides the
  reasoning; a doc is where a decision lands afterwards.
- **Agents stage and commit; the developer publishes.** `git push` never, and the guard hook blocks worktree
  destruction and every `gh` write.
- The tree is dirty with this session's work across `wow-two-ws` and `wow-two-sdk.backend.beta`. Nothing is
  committed yet.
