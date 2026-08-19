# SQL Migrator

*Last updated: 2026-06-16*

> Components, layout, lifecycle of the bespoke-SQL migrator — it runs `Apply.sql` / `Rollback.sql` verbatim.
> Purpose — own the schema as raw SQL the engine never rewrites: per-provider correctness is explicit, EF only maps.
> Use case — authoring migrations, or reasoning over apply order, drift, rollback.

> Engine internals (advisory-lock id, checksum algorithm, the `DbConnection`→`NpgsqlConnection` cast, the three-host
> model) → SDK `src/Data/Migrations/Bespoke/bespoke.md`. This doc is the product-facing contract; SQL idioms —
> quoting, rollback, `@no-transaction`, native enums → [migration-dialects.md](migration-dialects.md).

---

## File layout

One folder per migration, ordinal-prefixed, a raw `.sql` pair, under `{Repo}.Persistence/Migrations/`:

```
Migrations/
├── 001-baseline/{Apply,Rollback}.sql
├── 002-add-users-table/{Apply,Rollback}.sql
└── Dev/                       ← flat in-flight drafts, never embedded, never ordinal-named
    ├── .gitkeep
    └── 20260611T1030_add-service-column.sql
```

- folder `NNN-name` → `MigrationConventions.FolderPattern()` (`^(\d{3})-(.+)$`) → `MigrationDescriptor.Ordinal` +
  `.Name`; `.Label` renders `NNN-name`.
- fixed file names `Apply.sql` + `Rollback.sql` (`MigrationConventions.ApplyFileName` / `.RollbackFileName`).
- `Dev/` (`MigrationConventions.DevFolderName`) — flat editable drafts, both sections in one file, promoted at merge.
- must never embed a `Dev/` draft, and never read it as a numbered migration.
- **`Migrations/*/Apply.sql` is the schema-first canonical schema** — the owned `CREATE TABLE` truth
  ([database](../../database/database.md)).
- must read it before any model / query / EF config; EF maps over it, never generates it.

---

## Ordinals — allocated at merge

Engine/file-layout concern, **not** dialect. Ordinals order the apply loop and gate what's applied.

- new work → a flat `Dev/<utc-ts>_<slug>.sql`, **no ordinal**.
- assign the ordinal only at promote/merge on the integration branch — `next = max(NNN) + 1` (or `001`).
- two `Dev/` drafts on different branches merge cleanly.
- must never hand-create a `Migrations/NNN-name/` folder on a feature branch — that is the collision `Dev/` dodges.
- `MigrationScannerService.Scan()` throws on a malformed folder or a duplicate ordinal.

---

## Components

The engine depends only on a connection seam + `Npgsql` + `Dapper` + `ILogger` — zero domain / web / Hosting /
CLI deps. `AddDatabaseBespokeMigrations` registers all of them.

- `IMigrationSource` — `FileSystemMigrationSource` reads the raw `.sql` pairs from disk (CLI/dev),
  `EmbeddedResourceMigrationSource` from embedded resources (runtime).
- both return `RawMigration` and throw if a `Rollback.sql` is missing.
- `IMigrationScanner` / `MigrationScannerService` — parses `NNN-name`, computes the normalized checksum, returns
  `MigrationDescriptor`s ordered by ordinal.
- `MigrationDescriptor` — one validated migration: `Ordinal` · `Name` · `ApplySql` · `RollbackSql` · `Checksum` ·
  `NoTransaction` · `Label`.
- `IMigrationHistoryRepository` / `MigrationHistoryRepository` — owns `migration_history`: `EnsureTableAsync`,
  `GetAppliedAsync`, `RecordAsync`, `RemoveAsync` (rollback), `UpdateChecksumAsync` (repair) + `AcquireLockAsync` /
  `ReleaseLockAsync`.
- `MigrationHistoryEntry` — one applied row: `Ordinal` (PK) · `Version` · `Name` · `Checksum` · `AppliedAt` ·
  `AppliedBy` · `ExecutionMs`.
- `IMigrationRunnerService` / `MigrationRunnerService` — the host-facing engine: `ApplyPendingAsync`,
  `GetStatusAsync`, `RollbackAsync`, `RepairAsync`.
- `MigrationStatus` — snapshot: `Applied` · `Pending` · `Drifted` · `Orphaned`.
- `MigrationOptions` — per-host flags (below).
- `MigrationConventions` — file names, the `-- @no-transaction` directive, `Dev` folder name, `FolderPattern()`.

- `IMigrationRunnerService.ApplyPendingAsync(appliedBy, ct)` stamps `MigrationHistoryEntry.AppliedBy` with the host
  string — `"startup"` / `"cli"` / `"endpoint"`.
- `IMigrationDialect` / `PostgresMigrationDialect` — the engine's **internal** SQL seam (history DDL, advisory lock,
  `EnsureDatabaseExistsAsync`), selected by `MigrationOptions.Provider` (`DatabaseProvider`).
- it is **NOT** author-facing — authors write Apply/Rollback SQL ([migration-dialects.md](migration-dialects.md)).
- the dialect itself lives in the SDK `Bespoke/bespoke.md`.

---

## `MigrationOptions`

Set in code via the `AddDatabaseBespokeMigrations` configure hook; shared by every host.

- `AllowRollback` (default `false`) — gates `RollbackAsync` + `RepairAsync`.
- must enable it **per-operation** for a guarded rollback/repair — **prod included** (recovery), paired with the CLI's
  target-DB confirm.
- it is not an environment gate.
- `AllowOrphanedHistory` (default `false`) — tolerates applied rows with no source migration.
- must keep it `false` to fail closed when the binary predates the DB.
- `Provider` (default `Postgres`) — selects the `IMigrationDialect` (`DatabaseProvider`).
- `SchemaName` / `TableName` (default `public` / `migration_history`) — history-table location.
- `AdvisoryLockId` (default `4_855_178_001`) — the canonical lock id.
- every host of one DB **must** share it, or apply loops won't serialize.
- `Version` (default `v1.0`) — a free label on applied rows; `Ordinal` is the gate.

---

## Engine-level rules

- **Verbatim SQL** — the engine runs `Apply.sql` / `Rollback.sql` as written: no auto-quote, no rewrite (unlike EF).
- per-provider correctness is the author's job → [migration-dialects.md](migration-dialects.md).
- **`Rollback.sql` mandatory** — every migration ships one; `FileSystemMigrationSource` /
  `EmbeddedResourceMigrationSource` throw at scan if it's missing.
- rollback is a **guarded recovery op** — `RollbackAsync`, gated by `MigrationOptions.AllowRollback` + the CLI
  target-DB confirm.
- roll forward by default; use rollback in **prod** when a forward-fix isn't viable — apply succeeded, the deploy is
  broken, reverting fastest.
- **`-- @no-transaction` directive** — a leading `MigrationConventions.NoTransactionDirective` sets
  `MigrationDescriptor.NoTransaction`.
- the file runs outside a transaction and is **recorded separately**, so a crash mid-apply **re-runs the file**.
- its Apply SQL must therefore be idempotent.
- default (no directive) — a per-file transaction, so a failed file leaves zero partial schema.
- which statements force `@no-transaction` + the idempotency idioms → [migration-dialects.md](migration-dialects.md).

---

## Drift, orphans, checksum

- **Drift** — an applied `Apply.sql` edited after apply (disk checksum ≠ `MigrationHistoryEntry.Checksum`).
- reaction — `MigrationDriftException`, carrying the drifted `Label`s.
- prod → roll forward with a new migration; dev → rollback + re-apply, or `RepairAsync` to re-record.
- **Orphan** — a `migration_history` row whose source file is gone (older binary / deleted folder).
- reaction — fails closed with `MigrationOrphanException`, carrying the ordinals.
- must opt out via `MigrationOptions.AllowOrphanedHistory` only for an intentional older binary.

- checksum — SHA-256 over the **normalized** `Apply.sql`: CR/CRLF → LF, trailing whitespace trimmed.
- whitespace / line-ending edits don't false-trip; only real SQL edits do.
- `Rollback.sql` and the `@no-transaction` flag are **excluded** — a documented blind spot (SDK `Bespoke/bespoke.md`).
- `RepairAsync` re-records drifted checksums to the disk value.
- `RollbackAsync` removes the latest row, or every row above `targetOrdinal`.
- both are gated by `MigrationOptions.AllowRollback` — the engine throws if either runs while disabled.
- must never edit an applied migration in prod — roll forward with a new ordinal.

---

## Apply triggers — dev auto vs prod explicit

| Host | When apply runs | `AllowRollback` |
|---|---|---|
| Dev | on boot, gated to `IsDevelopment()` in the hosted-service adapter | `false` |
| Prod | **never auto on boot** — CLI / init step / HTTP endpoint only | `false` for apply; rollback opt-in |

- apply is idempotent under the advisory lock — the first host applies, the rest no-op.
- prod gates apply behind an explicit action, so a deploy never silently mutates schema on boot.
- the CLI is the build-now host — `ApplyPendingAsync("cli", ct)` from its composition root.
- CLI shape → [migration-tooling.md](migration-tooling.md).

---

## Registration & dual-ship

Two `AddDatabaseBespokeMigrations` overloads (`MigrationServiceCollectionExtensions`) wire the graph — source +
dialect + `IMigrationScanner` + `IMigrationHistoryRepository` + `IMigrationRunnerService`. An optional
`Action<MigrationOptions>` flips per-host flags.

- **Runtime hosts** embed SQL in the product assembly (ships in the binary, no deploy-time filesystem):

```csharp
services.AddDatabaseBespokeMigrations(typeof(SomePersistenceMarker).Assembly);
```

- **CLI / dev** reads on-disk (edit + apply live, no rebuild):

```csharp
services.AddDatabaseBespokeMigrations(migrationsRoot);   // "{Repo}.Persistence/Migrations"
```

One folder ships **two ways** — embedded for runtime, on-disk for the CLI; `Dev/` excluded from the binary:

```xml
<EmbeddedResource Include="Migrations\**\*.sql" Exclude="Migrations\Dev\**\*.sql">
    <LogicalName>Migrations/%(RecursiveDir)%(Filename)%(Extension)</LogicalName>
</EmbeddedResource>
```

- `<LogicalName>` yields `Migrations/001-baseline/Apply.sql` — what `EmbeddedResourceMigrationSource` parses.
- `folderPrefix` defaults to `"Migrations/"`.
- must keep the `Exclude` on `Migrations\Dev\**` — drafts are runtime-ignored anyway; never embed them.
