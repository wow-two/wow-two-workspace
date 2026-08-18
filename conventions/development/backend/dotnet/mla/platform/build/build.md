# Backend — Build

*Last updated: 2026-07-06*

> The MSBuild layer of a backend solution — the two solution-root files hoisting every shared setting
> out of the `.csproj` files.
> Purpose — one place for package versions, one for framework/language settings; a `.csproj` then carries
> only its own references.
> Use case — adding a project, adding/bumping a NuGet package, or finding a property repeated across
> `.csproj` files (`TargetFramework`, `Nullable`, a package `Version`).

## Files

Both live at the backend solution root — beside `{slug}.backend-services.slnx` — and every `.csproj` beneath
inherits them, because MSBuild walks up the tree.
Repo layout: [repo structure](../../../../../repo/structure/repo-structure.md) §5.

- `Directory.Packages.props` — every NuGet **version**, under Central Package Management.
  - [central package management](central-package-management.md)
- `Directory.Build.props` — every shared MSBuild **property**: framework, language, nullability.
  - [directory build props](directory-build-props.md)

---

## Invariant

- **must place both files at the solution root** (`codebase/{slug}.backend-services/`).
  - never per-project, never per-layer.
- **must keep a `.csproj` minimal** — references plus only genuinely project-specific properties.
  - references are `PackageReference` by name and `ProjectReference`.
  - project-specific means e.g. the `Api`'s `Sdk="Microsoft.NET.Sdk.Web"` + `BuildSpa` target.
  - everything shared is inherited, never restated.
- **must not repeat** a `TargetFramework` / `Nullable` / `LangVersion` / package `Version` in a `.csproj`.
  - a repeated value is drift waiting to happen; hoist it.
- reference implementation — `wow-two-sdk-beta.product-template` (`create-repo` stamps it) + `sift` + `arcade`.
  - the richer publish-oriented variant is the beta SDK's `src/Directory.{Build,Packages}.props`.
