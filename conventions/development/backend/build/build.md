# Backend — Build

*Last updated: 2026-07-06*

> The MSBuild layer of a backend solution — the two solution-root files that hoist every shared setting out of the `.csproj` files.
> Purpose — one place for package versions, one place for framework/language settings; a `.csproj` then carries only what is *unique* to that project (its references).
> Use case — reach for it whenever you add a project, add/bump a NuGet package, or find a property (`TargetFramework`, `Nullable`, a package `Version`) repeated across `.csproj` files.

## Files

Both live at the backend solution root — beside `{slug}.backend-services.slnx` — and are inherited by every `.csproj` beneath (MSBuild walks up the tree). Repo layout: [../../repo/structure/repo-structure.md](../../repo/structure/repo-structure.md) §5.

| File | Governs | Doc |
|---|---|---|
| `Directory.Packages.props` | every NuGet **version** — Central Package Management | [central-package-management.md](central-package-management.md) |
| `Directory.Build.props` | every shared MSBuild **property** — framework, language, nullability | [directory-build-props.md](directory-build-props.md) |

---

## Invariant

- **must place both files at the solution root** (`codebase/{slug}.backend-services/`) — never per-project, never per-layer.
- **must keep a `.csproj` minimal** — references (`PackageReference` by name, `ProjectReference`) + only genuinely project-specific properties (e.g. the `Api`'s `Sdk="Microsoft.NET.Sdk.Web"` + `BuildSpa` target); everything shared is inherited, never restated.
- **must not repeat** a `TargetFramework` / `Nullable` / `LangVersion` / package `Version` in a `.csproj` — a repeated value is drift waiting to happen; hoist it.
- reference implementation: `wow-two-sdk-beta.product-template` (`create-repo` stamps it) + `sift` + `arcade`. The richer publish-oriented variant is the beta SDK's `src/Directory.{Build,Packages}.props`.
