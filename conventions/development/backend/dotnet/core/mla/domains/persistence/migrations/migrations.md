# Migrations

*Last updated: 2026-08-18*

> Picks a product's migration runner — `Bespoke` (default), `Ef`, or `DbUp` — and the contract all three share.
> Scoped to backend persistence, not schema design.
> Purpose — one runner per product, one DI call: uniform apply/rollback/journal, explicit schema ownership.
> Use case — wiring the migration host, or choosing the schema's home: raw SQL, the EF model, a forward-only journal.

---

## Strategy

Three runners ship under `src/Data/Migrations/` in the backend-beta mono-lib. Pick one per product; don't mix.

- **`Bespoke` (default)** — raw `.sql` `Apply`/`Rollback` pairs; schema owned by SQL, EF a pure mapper.
  - register `AddDatabaseBespokeMigrations(sqlAssembly)` — embedded.
  - register `AddDatabaseBespokeMigrations(migrationsRoot)` — filesystem, CLI/dev.
  - default for wow-two products — own the schema, dev rollback, embedded + filesystem off one folder.
- **`Ef`** — register `AddEfMigrationsRunner<TContext>()`; `DbContext` owns the schema, `MigrateAsync` at boot.
  - pick when the consumer is code-first and wants no raw-SQL ownership.
- **`DbUp`** — register `AddDbUpRunner(configure)`; forward-only embedded scripts, no rollback.
  - pick for the simplest legacy forward-only journal — no squash or dev rollback needed.

Registration detail:

- `Bespoke` → `AddDatabaseBespokeMigrations` — design-stage; engine proven in `smart-qr`, extraction pending.
  - contract in `bespoke-migrations.md`.
- `Ef` → `AddEfMigrationsRunner<TContext>` wires `EfMigrationsBackgroundService<TContext>`.
  - the service calls `context.Database.MigrateAsync(ct)`.
  - tuned by `EfMigrationsOptions` — `Enabled`, `MaxConnectAttempts`, `ConnectRetryDelay` (Docker boot-race retry).
- `DbUp` → `AddDbUpRunner(Action<DbUpOptions>)` wires `DbUpBackgroundService`.
  - `DbUpOptions` — `ScriptsAssembly`, `ScriptsNamespacePrefix`, `UpgradeEngineFactory`, `ConnectionString`.
  - provider via `DbUpProviderFactory.Postgres` / `.SqlServer` / `.MySql`.

---

## Shared concepts

Every strategy honors the same operational contract:

- **Apply + rollback** — every runner applies forward; rollback varies.
  - `Bespoke` ships explicit `Apply`/`Rollback` pairs · `Ef` uses `Up`/`Down` · `DbUp` is forward-only, no rollback.
  - *how* to write the SQL → `migration-dialects.md`.
- **Roll forward by default; rollback is a guarded recovery op.**
  - never *edit* an applied migration — that is drift; fix forward.
  - rollback, where supported, is allowed in **any** environment incl. prod, for when a forward-fix isn't viable.
  - gate it behind an explicit enable + a target-DB confirm.
- **History / journal table** — each runner records applied migrations in its own table, so re-apply is a no-op.
  - `Bespoke` → `migration_history` · `DbUp` → its journal · `Ef` → `__EFMigrationsHistory`.
- **Embedded vs filesystem source** — runtime hosts embed scripts in the product assembly, no deploy-time filesystem.
  - CLI/dev reads on-disk — edit + apply live, no rebuild.
  - `Bespoke` does both off one folder; `DbUp` is embedded-only (`ScriptsAssembly`).
- **Idempotent boot-apply under a lock** — apply is safe to call from every host.
  - a DB-level lock serializes concurrent applicants — first applies, rest no-op.
  - `Bespoke` uses a Postgres advisory lock; `Ef` / `DbUp` rely on `MigrateAsync` / journal idempotency.
- **Dev auto vs prod explicit** — dev applies on boot, gated to `IsDevelopment()` in the hosted-service adapter.
  - prod applies via an explicit action — CLI / init step / HTTP endpoint — never silently on boot.

---

## Leaf docs

This index routes; the leaf docs carry the detail.

- `bespoke-migrations.md` — `Bespoke` product contract: layout, registration, drift/orphans, dual-ship csproj.
- `migration-dialects.md` — authoring `Apply`/`Rollback` pairs.
  - reserved-word quoting, `-- @no-transaction` idempotency, native PG enums, ordinals.
- `ef-migrations.md` — `Ef` code-first runner: `AddEfMigrationsRunner<TContext>`, boot-race retry options.
- `dbup-migrations.md` — `DbUp` forward-only runner: `AddDbUpRunner`, provider factories, embedded scripts.
- `migration-tooling.md` — `dotnet tool` CLI host shape.
  - packaging, arg parsing, exit codes, confirmation guards; `smart-qr-migrate` is the first consumer.

> Engine internals — advisory lock, normalized checksum, one-engine/three-hosts — live in the SDK design doc
> `src/Data/Migrations/Bespoke/bespoke.md`.
