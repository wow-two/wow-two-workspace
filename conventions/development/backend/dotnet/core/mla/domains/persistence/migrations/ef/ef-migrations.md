# EF Core Migrations

*Last updated: 2026-08-18*

> EF Core code-first strategy — `DbContext` owns the schema, generated C# migrations ship in `Migrations/`,
> applied on boot by a hosted runner.
> Purpose — schema co-evolves with the model: one edit-regenerate-ship loop covers both, no hand-written DDL drift.
> Use case — a C#-first product with a single owning context and no external schema-first DB dictating shape.

---

## When to pick

- rapid C#-first product where the schema **co-evolves with the model** — edit entities, regenerate, ship.
- single owning `DbContext`; no external/legacy schema-first DB driving the shape.
- opposite of the raw-SQL strategy in `migrations.md`.
  - there, schema-first: `Migrations/*/Apply.sql` is the owned truth and EF only maps over it.
- **One repo picks one** — code-first OR schema-first, never both.

---

## Register

- one call wires a startup runner per context — `AddEfMigrationsRunner<TContext>`
  in `EfMigrationsServiceCollectionExtensions`:

```csharp
services.AddEfMigrationsRunner<AppDbContext>();                       // defaults
services.AddEfMigrationsRunner<AppDbContext>(o => o.Enabled = false); // out-of-band apply
```

- registers `EfMigrationsHostedService<TContext>` (an `IHostedService`).
- validates `EfMigrationsOptions` on start — `AddOptions<EfMigrationsOptions>().ValidateOnStart()`.
- `TContext : DbContext` — the context that owns the schema and carries the generated `Migrations/` C# files.

---

## Apply on boot

- `EfMigrationsHostedService<TContext>.StartAsync` calls `context.Database.MigrateAsync(...)`.
  - applies all pending migrations; idempotent, an already-applied one no-ops.
- resolves `TContext` from a fresh DI scope (`CreateScope`); logs per attempt.
- connect-race resilient — retries up to `MaxConnectAttempts`, sleeping `ConnectRetryDelay` between tries.
  - covers the classic "DB not ready yet" Docker startup race; the final attempt rethrows.
- `Enabled = false` short-circuits before any DB touch — logs "disabled" and returns.

---

## `EfMigrationsOptions`

| Flag | Default | Purpose |
|---|---|---|
| `Enabled` | `true` | Master switch. Flip `false` in prod when migrations apply out-of-band (CI step, ops job). |
| `MaxConnectAttempts` | `10` | Connect tries before giving up — mitigates Docker DB-not-ready race. |
| `ConnectRetryDelay` | `2s` (`TimeSpan`) | Wait between attempts. |

- `init`-only record — set inline in `configure` or bind from config.

---

## Authoring a migration

- the `DbContext` + entity config (`OnModelCreating` / `IEntityTypeConfiguration<T>`) is the source of truth.
- must **edit the model, never the DB by hand**.
- generate the diff against the current model, then ship the C# migration files:

```bash
dotnet ef migrations add AddServiceColumn   # diffs model → Migrations/<ts>_AddServiceColumn.cs
dotnet ef migrations remove                  # undo the last unapplied migration
```

- must run from the project owning the `DbContext`; CLI tool wiring → `migration-tooling.md`.
- must not hand-author SQL — let the model diff produce `Up`/`Down`.
  - raw SQL is an escape hatch only for what EF can't express, inside the generated migration.
- apply happens automatically at boot via the runner above.
  - no separate `dotnet ef database update` step for dev/runtime hosts.

---

## Dev auto vs prod explicit

- dev: `Enabled = true` → schema follows the model on every boot.
- prod: set `Enabled = false` and apply out-of-band, so a deploy never silently mutates schema on startup.
  - mirrors the SQL strategy's dev-auto / prod-explicit split in `migrations.md`.
