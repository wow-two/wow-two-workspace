# Central Package Management

*Last updated: 2026-08-15*

> Every NuGet version lives once, in `Directory.Packages.props` at the backend solution root; a `.csproj` references a package **by name only**.
> Purpose — one source of truth per package: no per-project version drift, one edit to bump the whole solution, one place to audit the dependency set.
> Use case — answers "why is the version in each project? — it shouldn't be; it's central." Reach for it whenever you add a package, bump one, or spot a `Version=` on a `PackageReference`.

## Rule

- **must set `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>`** in `Directory.Packages.props` — this turns CPM on for the tree.
- **must declare each version once** as `<PackageVersion Include="{id}" Version="{v}" />` in that file — never a version anywhere else.
- **must reference by name only** in a `.csproj` — `<PackageReference Include="{id}" />` with **no `Version` attribute**; the version resolves from the central `PackageVersion`.
- **must not put a `Version` on a `PackageReference`** — CPM errors (`NU1008`) if a project pins its own; that is the guard-rail, keep it.

---

## Why central (not per-project)

- **one source of truth** — a package's version is stated in exactly one place; a reader never has to reconcile N `.csproj` files.
- **no drift** — the failure CPM prevents: smart-qr (pre-CPM) inline-pins `WoW2.Sdk.Backend.Beta` at `10.0.43-beta` in its app/domain projects but `10.0.40-beta` on the `.Testing` / `.Testing.Data` packages — two versions of one SDK family, silently, across 11 `.csproj` files.
- **coordinated bump** — raising a version is a **one-line** edit to `Directory.Packages.props`; every consuming project moves together, no sweep.
- **auditable set** — the whole dependency surface is one file to scan (licence review, vulnerability triage, "do we even still use this?").

---

## Shape

The proven product-repo shape (`wow-two-sdk-beta.product-template`, mirrored by `sift` / `arcade`) — group with `<ItemGroup>` blocks (optionally `Label=`), floors chosen to satisfy the SDK's transitive minimums (no downgrades):

```xml
<Project>

  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>

  <ItemGroup>
    <!-- wow-two backend SDK (kit): mediator, Result/AppError, IKeyedEntity, web/problem-details. On nuget.org. -->
    <PackageVersion Include="WoW2.Sdk.Backend.Beta" Version="10.0.21-beta" />
  </ItemGroup>

  <ItemGroup>
    <!-- ASP.NET Core / EF Core (.NET 10). Floors satisfy the kit's transitive minimums (no downgrades). -->
    <PackageVersion Include="Microsoft.AspNetCore.OpenApi" Version="10.0.8" />
    <PackageVersion Include="Microsoft.EntityFrameworkCore" Version="10.0.3" />
    <PackageVersion Include="Microsoft.EntityFrameworkCore.Sqlite" Version="10.0.3" />
    <PackageVersion Include="Microsoft.Extensions.DependencyInjection.Abstractions" Version="10.0.9" />
    <PackageVersion Include="Microsoft.Extensions.Configuration.Abstractions" Version="10.0.9" />
  </ItemGroup>

  <ItemGroup>
    <!-- Test stack. -->
    <PackageVersion Include="Microsoft.NET.Test.Sdk" Version="17.12.0" />
    <PackageVersion Include="xunit" Version="2.9.2" />
    <PackageVersion Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>

</Project>
```

The `.csproj` side is bare — one `Arcade.*` project in full:

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.DependencyInjection.Abstractions" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\Arcade.Application\Arcade.Application.csproj" />
    <ProjectReference Include="..\Arcade.Domain\Arcade.Domain.csproj" />
  </ItemGroup>

</Project>
```

---

## Add / bump a package

- **add** — put a `<PackageVersion Include="{id}" Version="{v}" />` in the fitting `<ItemGroup>` (create a `Label`ed group if it's a new concern), then add `<PackageReference Include="{id}" />` (no version) to each project that uses it.
- **bump** — edit the single `Version` on that `PackageVersion`; the whole solution moves. No `.csproj` touched.
- **remove** — drop the `PackageVersion` only after the last `PackageReference` to it is gone (an orphan `PackageVersion` is harmless but noise).
- ordering inside a group is alphabetical-ish by id — keep new entries grouped by concern, not appended blindly.

---

## Beta SDK ref + `FrameworkReference`

- the one **required** package is the kit: `<PackageVersion Include="WoW2.Sdk.Backend.Beta" Version="{x.y-beta}" />` (on nuget.org) — bump it here to move the whole app onto a new SDK build.
- a project that `ProjectReference`s the SDK mono-lib (rather than the NuGet) **must add `<FrameworkReference Include="Microsoft.AspNetCore.App" />`** or restore hits `NU1109` (DI package downgrade). This lives in the `.csproj` (it is project-specific), not the central file.
- pick central `PackageVersion` **floors** at or above the SDK's transitive minimums so restore never has to downgrade a kit-required package.
- `CentralPackageTransitivePinningEnabled` (pins transitive deps to central versions too) is **optional** — the beta SDK sets it for a locked-down surface; a product repo may leave it off. Turn it on only when you want transitive versions frozen.
