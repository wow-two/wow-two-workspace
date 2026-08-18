# DbUp

*Last updated: 2026-08-18*

> Forward-only embedded-`.sql` migrations applied on host boot via DbUp — journaled, no rollback, no checksum.
> Purpose — a battle-tested journal table for additive schemas, without the bespoke checksum/drift/rollback engine.
> Use case — reach for it when every change is additive, or for legacy standalone `.sql` sets;
> otherwise use `AddDatabaseBespokeMigrations` (`migrations.md`).

## When to pick

- simple forward-only schema: every change is additive, you never roll back in place.
- legacy / existing script sets already authored as standalone `.sql` files.
- you want a battle-tested journal table, not the bespoke `migration_history` + checksum-drift engine.
- multi-provider out of the box (Postgres / SqlServer / MySql) with one switch.
- **not** for checksum drift detection, rollback symmetry, advisory-lock coordination, dev on-disk live-edit.
  - that is `AddDatabaseBespokeMigrations` (`migrations.md`); DbUp is the lighter, dumber choice.

---

## Register

- one call wires options + the hosted service — `AddDbUpRunner(this IServiceCollection, Action<DbUpOptions>)`:

```csharp
services.AddDbUpRunner(o =>
{
    o.ConnectionString = cfg.GetConnectionString("Default")!;
    o.UpgradeEngineFactory = DbUpProviderFactories.Postgres;
    o.ScriptsAssembly = typeof(SomePersistenceMarker).Assembly;   // defaults to entry assembly
    o.ScriptsNamespacePrefix = "App.Migrations.Scripts.";          // optional filter
});
```

- `AddDbUpRunner` calls `AddOptions<DbUpOptions>().Configure(configure).ValidateOnStart()`.
  - plus `AddHostedService<DbUpHostedService>()`.
- both args null-guarded (`ArgumentNullException.ThrowIfNull`).

---

## Apply on boot

- `DbUpHostedService` (an `IHostedService`) runs in `StartAsync`.
  - pending scripts apply as the host starts, before requests.
- `DbUpOptions.Enabled == false` → logs `"DbUp runner is disabled — skipping"`, no-ops. Default `true`.
- resolves the scripts assembly (`ScriptsAssembly ?? Assembly.GetEntryAssembly()`); throws if neither resolves.
- calls `WithScriptsEmbeddedInAssembly`, then `.LogToConsole().Build()`.
  - with the `ScriptsNamespacePrefix` filter when set, unfiltered otherwise.
- `upgrader.PerformUpgrade()` — on `!result.Successful` logs `result.ErrorScript?.Name`.
  - it then throws `InvalidOperationException` — fail-fast, boot aborts on a bad script.
- on success logs the applied `result.Scripts.Count()`.
- `StopAsync` is a no-op.

---

## Options

`DbUpOptions` is a sealed `record` — set via the `init` properties inside the `configure` delegate:

- `Enabled` — gate the runner (default `true`).
- `ConnectionString` — target DB; required, blank throws at `StartAsync`.
- `UpgradeEngineFactory` — `Func<string, UpgradeEngineBuilder>` selecting the provider.
  - required; null throws at `StartAsync`.
- `ScriptsAssembly` — assembly to scan for embedded `.sql`; null → entry assembly.
- `ScriptsNamespacePrefix` — optional embedded-resource name-prefix filter (e.g. `"App.Migrations.Scripts."`).

---

## Provider selection

- `UpgradeEngineFactory` picks the engine; use the `DbUpProviderFactories` shortcuts:

| `DbUpProviderFactories` | Engine |
|---|---|
| `Postgres` | `DeployChanges.To.PostgresqlDatabase(cs)` |
| `SqlServer` | `DeployChanges.To.SqlDatabase(cs)` |
| `MySql` | `DeployChanges.To.MySqlDatabase(cs)` |

- Sqlite is intentionally omitted — the dbup-sqlite engine takes a connection object, not a string.
  - set `UpgradeEngineFactory` yourself:
    `cs => DeployChanges.To.SQLiteDatabase(new SharedConnection(new SQLiteConnection(cs)))`.

---

## Scripts & journal

- migrations are embedded `.sql` resources in the scripts assembly.
  - mark each `<EmbeddedResource>` in the product `.csproj`.
- **Forward-only** — DbUp runs each script once, in name order; there is **no rollback**.
  - to undo, ship a new forward script.
- DbUp records applied scripts in its own journal table (`SchemaVersions` by default).
  - a journaled script is skipped, which makes boot idempotent across hosts/restarts.
- must name scripts so lexical order = apply order — zero-padded `0001_*.sql`.
  - a script's name is its journal identity; **never rename an applied script**, it re-runs.
- edits to an already-applied script are **not** detected — no checksum, DbUp trusts the journal.
  - need drift detection? use `AddDatabaseBespokeMigrations` instead (`migrations.md`).
