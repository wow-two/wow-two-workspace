# Architecture

*Last updated: 2026-08-16*

> Which pattern splits a backend service into projects, and how those projects group inside the solution.
> Purpose — a pattern doc states the split and nothing else, so a layer inherits no component list it does not own.


## The arrangements

| Arrangement | Status |
|---|---|
| [clean](clean/clean.md) | what every service we ship uses |
| [onion](onion/onion.md) | shell |
| [hexagonal](hexagonal/hexagonal.md) | shell |
| [vertical slice](vertical-slice/vertical-slice.md) | shell |

- must use clean unless a service argues otherwise before it is written.
- must not read a shell as a permitted alternative — it names an arrangement, and rules nothing.

---

## Patterns

One folder per architecture, each with its own lead doc. A service names the one it follows.

| Pattern | Folder | Applies to |
|---|---|---|
| Clean Architecture | [clean](clean/clean.md) | every backend service |

- must give a second pattern its own folder beside `clean/`
- must not fold a pattern into another — a pattern is the unit a service chooses

---

## Scope

- must state the layer set, the dependency direction, and the project each layer maps to
- must not enumerate the components a layer holds — the domain that declares them states that, per domain
- must leave the folders inside a layer to [domain structuring](clean/domain-structuring.md)

---

## Solution organization

A backend solution (`{slug}.backend-services.slnx`) groups its projects into **solution folders** — virtual nodes,
not on-disk paths. Projects are named `{Brand}.{Domain}[.{SubDomain}]`, PascalCase.

| Folder | Holds | Examples (SmartQr) |
|---|---|---|
| `services/` | the product — deployable hosts and their domain / persistence / feature libs | `SmartQr.Api`, `SmartQr.Common.Domain`, `SmartQr.Codes` |
| `platform/` | SDK-bound extractables, named `{Brand}.Platform.*` | `SmartQr.Platform.Core`, `SmartQr.Platform.Migrations` |
| `libraries/` | product-level shared libs that are not service code | — |
| `tools/` | CLIs and dev utilities | `SmartQr.Migrations.Cli` |
| `tests/` | test projects | `SmartQr.Tests.Unit`, `SmartQr.Tests.E2E` |

- must reference `services → platform` and never the reverse — `platform/*` sees the kit and the BCL only
- must add a folder when a project needs it, and may declare one empty to signal a roadmapped extraction
- must keep the lift of `platform/*` into the SDK a move plus a namespace rename, never a rewrite —
  what qualifies is [extract / keep / remove](../../../../../sdk-extraction.md), not this doc

---

## Solution encoding

A solution folder is a virtual node; a project joins it by **GUID**, not by disk path.

- must use `.slnx` — XML `<Folder Name="/platform/"><Project Path="…csproj" /></Folder>`
- must nest a project in a classic `.sln` through `GlobalSection(NestedProjects)`, `{childGuid} = {folderGuid}`
- must leave a project's own GUID and its `ProjectConfigurationPlatforms` block untouched when it moves between folders
- an empty folder in a classic `.sln` omits its `NestedProjects` lines

---

## Where a folder is created

A construct names its folder — `Services/`, `Entities/`, `Controllers/` — and stops. This is the doc that
says which project holds it.

| Folder | Project |
|---|---|
| `Entities/` · `Enums/` · `Constants/` · `Extensions/` · value objects | `Domain` |
| `Commands/` · `Queries/` · `Events/` · `*Handlers/` · `Models/` (holds `Model`) · `Services/` · `Validators/` · `Settings/` | `Application` |
| `Repositories/` · `Brokers/` · `Adapters/` · `Integrations/{Provider}/` · `Mappers/` · `Factories/` · `Registries/` | `Infrastructure` |
| EF configurations · migrations · the `DbContext` | `Persistence` |
| `Controllers/` · `Requests/` · `Models/` (holds `Dto`) | `Api`, each under the domain — `Api/{Domain}/Controllers/` |
| `Configurations/` — `HostConfiguration` and its parts | `Api` |

- must read a folder's **name** off its construct doc, and its **project** off this table.
- must not restate a project in a construct doc — the same folder sits elsewhere in another shape.
- must place a `BackgroundServices/` folder in the project that owns the work, not always in `Api`.
- must read a repeated folder name by its project — `Models/` holds `Model` in `Application` and `Dto` in
  `Api`, and the two never mix.
- must keep `Controllers/` under its domain folder — ASP.NET Core discovers a controller by **type**, not by
  folder, so `Api/{Domain}/Controllers/` breaks nothing. Only Razor view lookup is folder-bound, and an API
  has no views.
- must split a domain into its own sub-folder inside each project →
  [domain structuring](clean/domain-structuring.md).
