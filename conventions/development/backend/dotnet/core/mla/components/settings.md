# Settings

*Last updated: 2026-08-18*

> The record a configuration section binds into.
> Purpose — configuration reaches code as a typed, immutable shape, validated once at startup.
> Use case — any value that differs per environment; behavior knobs passed in code are
> [`Options`](../constructs/constructs.md).

> Defined at [settings — the construct](../constructs/data/settings.md); this doc carries every condition for using one.

## Location

Where it sits is part of what it is → [settings](../constructs/data/settings.md) § *Location*.

---

## Declaration

What it is, how it is declared and what it is called → [settings](../constructs/data/settings.md) § *Declaration*.

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

Per-environment overrides and env-var naming → [host configuration](../../../shapes/service/platform/startup/host-configuration.md).
