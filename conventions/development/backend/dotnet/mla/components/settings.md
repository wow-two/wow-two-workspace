# Settings

*Last updated: 2026-08-18*

> The record a configuration section binds into.
> Purpose — configuration reaches code as a typed, immutable shape, validated once at startup.
> Use case — any value that differs per environment; behavior knobs passed in code are
> [`Options`](../constructs/constructs.md).

> Defined at [settings — the construct](../constructs/data/settings.md); this doc carries every condition for using one.

## Location

### Folder
- must sit in a `Settings/` folder, one file per settings record.

### File
- must give it its own file, named for the type →
  [one type, one file](../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../lla/notation/documentation/summary.md)
- must start with **Configuration for**, overriding the `Represents` default that data components carry.
- must name the behavior the section tunes, never the section's key.

```csharp
// ✅ names what the values steer
/// <summary>Configuration for AI classification pipeline behavior.</summary>
// ❌ names the config key, which the binding already states
/// <summary>Configuration for the Classification section.</summary>
```

### Construct
- must declare a `sealed record` — the binder writes once, and value equality is the correct claim.
- must carry no default value on any member — a missing setting fails the boot rather than running wrong.
- must declare `{ get; init; }` — the binder writes once, at startup.
- member shape (`required`, non-nullable) → [constructs](../../lla/constructs/constructs.md) § *Data components*.

### Type name
- must suffix with `Settings`, named for the section it binds — `ClassificationSettings`.
- must reach for `Options` instead when a caller supplies the values in code.

```csharp
// ✅
public sealed record ClassificationSettings
// ❌ knobs passed in code are `Options`, not a bound section
public sealed record HttpResilienceSettings
```

---

---

## Content

### Members
- must name each member for the value it steers, never for its config key — the binder matches by name,
  so the two stay identical without the summary repeating it.
- must carry a `<summary>` on every member stating **what the value changes**, plus its unit where one
  exists — `seconds`, `attempts`, `bytes`.
- must state the range or the allowed set when the value is bounded, so a wrong value fails review rather
  than production.
- must not carry a member no environment ever differs on — a constant belongs in
  [constants](constants.md).

---

## Registration

- must bind through `AddOptions<T>().Bind(section)` in `AddSettings()`, never by reading `IConfiguration` elsewhere.
- must name the section with `nameof` or a `SectionName` const, never a repeated string literal.
- must call `ValidateOnStart()` — a missing or invalid setting fails the boot, never the first request.
- must call `ValidateDataAnnotations()` when the record carries `[Required]` or `[Range]`.
- may prefer source-gen validation (`[OptionsValidator]`) when the record is complex.

```csharp
// ✅
builder.Services
    .AddOptions<ClassificationSettings>()
    .Bind(builder.Configuration.GetSection(nameof(ClassificationSettings)))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

Per-environment overrides and env-var naming → [host configuration](../platform/startup/host-configuration.md).
