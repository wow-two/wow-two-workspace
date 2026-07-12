# Directory.Build.props

*Last updated: 2026-07-06*

> The shared MSBuild properties for a backend solution — framework, language, nullability — hoisted into one root file so every `.csproj` inherits them.
> Purpose — a single, uniform build surface: one edit moves the whole solution's `TargetFramework` / `LangVersion`; a `.csproj` never restates a shared setting.
> Use case — reach for it whenever you'd otherwise write `<TargetFramework>` / `<Nullable>` / `<ImplicitUsings>` / `<LangVersion>` in a `.csproj`, or want a solution-wide analyzer/warning policy.

## Baseline

The proven product-repo set — `wow-two-sdk-beta.product-template` (`create-repo` stamps it), byte-for-byte in `sift` + `arcade`:

```xml
<Project>

  <!--
    Solution-wide build defaults for every {Brand}.* project (Clean Architecture, .NET 10).
    Per-project .csproj files stay minimal: they declare only references, not these settings.
  -->
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>

</Project>
```

| Property | Value | Why |
|---|---|---|
| `TargetFramework` | `net10.0` | one framework across the solution — the stack floor ([../../repo/repo-conventions.md](../../repo/repo-conventions.md#tech-stack)) |
| `Nullable` | `enable` | nullable reference types on everywhere — no per-project opt-out |
| `ImplicitUsings` | `enable` | global usings for the common namespaces — less `.cs` header noise |
| `LangVersion` | `latest` | newest C# the SDK offers (collection expressions, primary constructors, …) |

- **must set these four in `Directory.Build.props` only** — never in a `.csproj`.
- **must not override a baseline property per-project** — if one project genuinely needs a different value, raise it (it usually signals the setting belongs in the SDK-style split, not a local override).

---

## csproj stays minimal

A `.csproj` carries only what is unique to it — references + project-specific properties. The `SmartQr.Domain` project entire:

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <ItemGroup>
    <PackageReference Include="WoW2.Sdk.Backend.Beta" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\SmartQr.Common.Domain\SmartQr.Common.Domain.csproj" />
  </ItemGroup>

</Project>
```

Legitimately project-specific (stays local): `Sdk="Microsoft.NET.Sdk.Web"` on the `Api`, its `<SpaRoot>` + `BuildSpa` target ([../../../deployment/hosting/single-host-serving.md](../../../deployment/hosting/single-host-serving.md)), a `FrameworkReference` ([central-package-management.md](central-package-management.md)).

---

## Analyzer + warning policy (opt-in, publish-oriented)

The baseline stops at the four properties. A repo that wants a strict build surface adopts the beta SDK's stance (`wow-two-sdk.backend.beta/src/Directory.Build.props`) — codified here so it's applied uniformly when reached for, not reinvented:

```xml
<TreatWarningsAsErrors>true</TreatWarningsAsErrors>
<AnalysisLevel>latest-recommended</AnalysisLevel>
<EnableNETAnalyzers>true</EnableNETAnalyzers>
<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
<WarningsNotAsErrors>$(WarningsNotAsErrors);CA1848;CA1873;CA1305;CA1000;CA1716;CA1822;CA1720;NU1510;NU1902;NU1903</WarningsNotAsErrors>
```

- **`TreatWarningsAsErrors=true`** — correctness warnings **fail the build**; the default is warnings-as-errors, exceptions are carved back individually.
- **`WarningsNotAsErrors`** — the escape hatch: perf/style/design analyzer IDs (`CA1848` logging-delegate, `CA1822` mark-static, `CA1720` identifier-contains-type-name, `CA1305`/`CA1716`/`CA1000`, …) and **NuGet advisories** stay **visible as warnings but non-blocking**. Correctness analyzers stay errors.
- **NuGet-audit codes** ride the same list: `NU1510` (framework-provided package not pruned on net10), `NU1902`/`NU1903` (transitive-dependency vulnerability advisories) — surfaced, not fatal, so a beta-forever surface isn't blocked by an advisory on a transitive it can't immediately move.
- **stance:** warnings-as-errors **on** by default, loosened per-ID with a comment justifying each carve-out; tighten (shrink the `WarningsNotAsErrors` list) as an area matures. A product repo may start from the four-property baseline and adopt this when its build surface is worth hardening.

---

## Packaging / versioning props — SDK-only

The beta SDK's `Directory.Build.props` also hoists **package-authoring** props (`IsPackable`, `PackageLicenseExpression`, `Authors`, `GenerateDocumentationFile`, source-link, deterministic-build, and the CI-bumped `Version`/`FileVersion`) because every project there ships a NuGet. A **product / venture** repo ships an **image, not packages** ([../../repo/structure/repo-structure.md](../../repo/structure/repo-structure.md) §13) — so it **must not** copy those props; they belong only to library/SDK repos.
