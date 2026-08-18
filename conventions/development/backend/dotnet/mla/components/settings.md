# Settings

*Last updated: 2026-08-18*

> The record a configuration section binds into.
> Purpose — configuration reaches code as a typed, immutable shape, validated once at startup.
> Use case — any value that differs per environment; behavior knobs passed in code are [`Options`](../constructs/constructs.md).

## Location

### Folder
- must sit in a `Settings/` folder, one file per settings record.

### File
- must give each settings record its own file, named for the type.

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
- member shape (`{ get; init; }`, `required`) → [constructs](../../lla/constructs/constructs.md) § *Data components*.

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
