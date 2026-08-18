# Migration Tooling

*Last updated: 2026-08-15*

> The bespoke migrator shipped as a `dotnet tool` CLI — packaging, verb tree, exit codes, destructive-op guard.
> Purpose — a version-pinned, scriptable migration command that branches on outcome and refuses destructive ops.
> Use case — wiring a bespoke-migrator repo's CLI host; `smart-qr-migrate` first consumer, `wow-migrate` SDK target.

---

## Shape

- the CLI is a **thin host** over the migrator engine — one of three, with an HTTP endpoint and a hosted service.
- owns arg parsing · config resolution · composition root · exit codes · confirmation prompts — **nothing else**.
- the engine owns the migration operation and is resolved from DI — `AddDatabaseBespokeMigrations`,
  `IMigrationRunnerService` ([bespoke-migrations.md](bespoke-migrations.md)).

---

## Packaging

Pack as a tool, not a published app. The csproj head:

```xml
<PropertyGroup>
  <OutputType>Exe</OutputType>
  <PackAsTool>true</PackAsTool>
  <ToolCommandName>{verb-noun}</ToolCommandName>            <!-- the invoked command, e.g. smart-qr-migrate -->
  <PackageId>{Brand}.{Domain}.Cli</PackageId>               <!-- dotted, matches the ecosystem -->
  <!-- .NET 10: keep one platform-agnostic package -->
  <CreateRidSpecificToolPackages>false</CreateRidSpecificToolPackages>
</PropertyGroup>
```

- `ToolCommandName` = the shell command (`smart-qr-migrate`); `AssemblyName` SHOULD match it.
- `PackageId` carries the dotted brand (`{Brand}.{Domain}.Cli`).
- `CreateRidSpecificToolPackages=false` — on .NET 10, `dotnet pack` with **any** `RuntimeIdentifiers` present emits
  RID-specific tool packages, not the framework-dependent platform-agnostic one (documented breaking change).
- must set it false and keep `RuntimeIdentifiers` out of the csproj → one `dotnet-tools.json` entry works on every OS.
- use `ToolPackageRuntimeIdentifiers` only if multi-RID is wanted.
- CPM — with `ManagePackageVersionsCentrally=true`, a versionless `<PackageReference>` resolves only when a
  `<PackageVersion>` exists in `Directory.Packages.props`.
- must add the CLI's deps (`System.CommandLine`, any standalone provider), pinned to exact lines, never `2.0.0-beta*`.

---

## Manifest

- must distribute via a repo-local `.config/dotnet-tools.json` manifest, mirroring `dotnet ef`.
- version-pinned per repo · `dotnet tool restore` on clone · no global pollution · CI-friendly.

```jsonc
// .config/dotnet-tools.json
{ "version": 1, "isRoot": true,
  "tools": { "{Brand}.{Domain}.Cli": { "version": "0.0.*", "commands": ["{verb-noun}"] } } }
```

- manifest discovery walks up from the **cwd**.
- invoking outside the manifest tree silently fails to restore — run from the repo subtree, or pass the path flags.

---

## Command tree (System.CommandLine 2.0)

Build the tree in a `static CliCommands.Build()`; keep command **bodies** in a separate `CliRunner`.

- **Root** carries the **global, recursive** options — `new Option<string?>("--name") { Recursive = true }`.
- a recursive option applies to every subcommand without re-declaring.
- **Verbs** are `Command` objects added to `root.Subcommands`; declare verb-local options / arguments on the verb.
- **`SetAction`** reads parsed values and **delegates to the runner** — the command knows nothing about the operation:

```csharp
var command = new Command("apply", "Ensure the target exists, then apply pending work.");
command.SetAction((parseResult, ct) =>
    CliRunner.ApplyAsync(parseResult.GetValue(connectionOption), parseResult.GetValue(sqlDirOption), ct));
```

- `SetAction`'s delegate receives a `CancellationToken` — thread it through the runner and the engine.
- a sync body wraps in `Task.FromResult(...)`.
- must disable the default exception handler — exceptions surface as a clean one-liner, not a stack trace, and map
  to exit codes:

```csharp
var configuration = new InvocationConfiguration { EnableDefaultExceptionHandler = false };
return await CliCommands.Build().Parse(args).InvokeAsync(configuration);
```

- must pin an exact `System.CommandLine` 2.0 line — the package churned through `2.0.0-beta*`, breaking across betas.
- must write handler signatures against the **final 2.0 API**, not a beta tutorial.
- the copy inside the `dotnet` muxer is un-referenceable — add the NuGet package explicitly.

---

## Exit codes — three tiers

Map exceptions to codes in the top-level `catch`. A consumer (CI, a script) branches on the tier:

| Code | Meaning | Sources |
|---|---|---|
| `0` | success | normal operation |
| `1` | **validation** | bad config · missing file/dir · drift (`MigrationDriftException`) |
| `2` | **execution** | runtime/DB failure · **destructive-op guard tripped** |

```csharp
catch (Exception ex)
{
    Console.Error.WriteLine($"✗ {ex.Message}");
    return ex switch
    {
        MigrationDriftException                              => 1,   // validation: drift is a validation failure
        DirectoryNotFoundException or FileNotFoundException  => 1,
        _                                                    => 2,   // execution
    };
}
```

- drift / precondition mismatch is `1`, not `2` — a validation failure, not an execution failure.
- must not blanket-map every non-zero outcome to `2`.
- the **guard-tripped** path returns `2` directly from the runner, without throwing.

---

## Destructive-op guard

A verb that mutates or removes state (rollback, repair, truncate, force-reset) MUST gate on the **target resource**,
not on the environment.

- must gate on the target, not `ASPNETCORE_ENVIRONMENT` — a standalone tool runs under whatever the shell has (often
  unset → looks non-prod) while the connection flag may point straight at production.
- env is at most an **additional** block, never the sole axis.
- must require **`--i-understand-this-is <target>`** to match the operation's actual target.
- derive the target from the resolved input — e.g. `new NpgsqlConnectionStringBuilder(conn).Database`.
- compare with `StringComparison.Ordinal`, and refuse on mismatch.
- must then prompt **`[y/N]`** unless **`--force`** is passed.
- on refusal, write the correct re-run hint and **return the execution code (`2`)** — do not throw.

```csharp
private static bool ConfirmDestructiveTarget(string? connection, string? confirmTarget, bool force)
{
    var target = new NpgsqlConnectionStringBuilder(ResolveConnection(connection)).Database ?? "(unknown)";

    if (!string.Equals(confirmTarget, target, StringComparison.Ordinal))
    {
        Console.Error.WriteLine($"✗ Destructive op refused. Re-run with --i-understand-this-is {target} to confirm.");
        return false;   // caller returns 2
    }
    if (force) return true;

    Console.Write($"This will modify '{target}'. Continue? [y/N] ");
    return Console.ReadLine()?.Trim() is "y" or "Y" or "yes" or "YES";
}
```

- must scope the guard to the path that actually mutates.
- a read-only verb with a destructive sub-mode (`verify` vs `verify --repair`) guards **only** the destructive flag,
  leaving the read path prompt-free.
- the engine's destructive surface stays disabled by default — the host opts in per call, on the guarded verbs only:
  `AddDatabaseBespokeMigrations(dir, o => o.AllowRollback = true)`.
- must never hard-wire the engine open.

---

## Secret hygiene

- must never echo the connection / password — not in logs, not in error output, not in the fail-fast searched-list.
- must redact before printing.
- should prefer env or stdin over a plaintext flag — a `--connection` value lands in shell history and `ps`.
- offer `--connection-env NAME` / `--connection-stdin`.
- treat the raw `--connection` flag as a one-off convenience, not the recommended path.
- must commit only **templates** with `${ENV}` interpolation.
- an **unset `${VAR}` is a hard fail**, never a silent empty password.

---

## Config resolution order

Resolve each input **flag → env → discovered default**, highest precedence first, in a single helper per input.
Fail fast on a true miss with the **full searched list** (password redacted):

```csharp
public static string ResolveConnection(string? flag) =>
    flag
    ?? Environment.GetEnvironmentVariable("{TOOL}_DB_CONNECTION")
    ?? DefaultConnection;                               // localhost default for the canonical dev layout only
```

| # | Source | Notes |
|---|---|---|
| 1 | CLI flag (`--connection`, `--sql-dir`) | one-offs; secrets prefer env/stdin (above) |
| 2 | Env var (`{TOOL}_DB_CONNECTION`, `{TOOL}_SQL_DIR`) | preferred for secrets |
| 3 | Discovered default | localhost default, **canonical layout only** — overridable, never universally hardcoded |

- when discovery is ambiguous (multi-project repo, manifest root ≠ source dir), the flag is **required**, not guessed.

---

## Composition root + cancellation

The CLI brings the concrete DI container; the engine references only `*.Abstractions`. Build a `ServiceProvider` per
invocation, register the engine via `AddDatabaseBespokeMigrations`, resolve `IMigrationRunnerService`, run:

```csharp
await using var provider = new ServiceCollection()
    .AddSingleton(dataSource)
    .AddLogging()
    .AddDatabaseBespokeMigrations(ResolveSqlDir(sqlDir), options => options.AllowRollback = allowRollback)
    .BuildServiceProvider();

return await provider.GetRequiredService<IMigrationRunnerService>().ApplyPendingAsync("cli", ct);
```

- `await using` the provider — engine resources (data sources, connections) dispose on exit.
- must honor Ctrl-C — System.CommandLine supplies the `CancellationToken` to `SetAction`.
- thread it through the runner into every engine call, so an interrupt cancels cleanly instead of tearing down
  mid-write.
- must keep `Program.cs` thin — provider-wide knobs, build + parse + invoke, map exit codes.
- e.g. `DefaultTypeMap.MatchNamesWithUnderscores = true` for Dapper snake_case.
- tree shape lives in `CliCommands`; bodies + DI in `CliRunner`.
