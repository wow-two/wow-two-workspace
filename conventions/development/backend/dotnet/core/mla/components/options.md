# Options

*Last updated: 2026-08-20*

> The class an `Add*` extension hands to the caller's delegate.
> Purpose — a knob reaches code as a typed shape with a working default, so an unconfigured call still runs.
> Use case — any value a host supplies in code; values an environment differs on are
> [`Settings`](../constructs/constructs.md).

> Defined at [options — the construct](../constructs/data/options.md); this doc carries every condition for using one.

## Location

Where it sits is part of what it is → [options](../constructs/data/options.md) § *Location*.

---

## Declaration

What it is, how it is declared and what it is called → [options](../constructs/data/options.md) § *Declaration*.

---

## Content

### Members
- must name each member for the behavior it steers, never for the extension that reads it.
- must carry a `<summary>` on every member stating **what the value changes**, plus its unit where one
  exists — `seconds`, `attempts`, `bytes`.
- must state the range or the allowed set when the value is bounded.
- must give an omittable member the value a caller who reads nothing would want — the delegate is optional,
  so that default is the shipped behavior.
- must not give a `required` member a default — the compiler already refuses to build the type without it.
- must not carry a member no caller ever changes — that value is a [constant](constants.md).

---

## Registration

- must take the delegate as `Action<T>? configure = null`, so the unconfigured call is the short one.
- must construct, invoke, register — `new`, `configure?.Invoke(options)`, then a singleton.
- must take a must-supply value as its own `Add*` parameter and assert it in a `.Validate()` clause —
  the parameter documents it, the clause enforces it at boot.
- must register through `AddOptions<T>()` — one recipe, so a consumer and a registration cannot disagree,
  and `.Validate()` is available on every type rather than on the ones somebody remembered.
- must project the record in the same `Add*` method — `AddSingleton(sp => sp.GetRequiredService<IOptions<T>>().Value)`,
  so a consumer takes `T` and never the wrapper.
- must not rely on `required` to enforce a value here — the pipeline builds the type through
  `Activator.CreateInstance`, which leaves a `required` member `null` instead of refusing, so a `.Validate()`
  clause is the only thing that catches an absent value.
- must not register a value the caller builds per call — a knob passed to a method is an argument, and an
  argument is never registered.
- may register through `AddOptions<T>()` when the value has to compose across registrations
  (`PostConfigure`) or validate at boot — that pipeline is the only thing it buys.
- must not declare a `required` member on a type registered through `AddOptions<T>()` — that pipeline
  constructs `T` itself and cannot supply one.
- must not read `IConfiguration` inside the extension — a value that comes from configuration is a
  [settings](settings.md) record the host binds and passes in.
- must apply the delegate before anything reads the instance, so no consumer sees the pre-delegate state.

```csharp
// ✅
public static IServiceCollection AddDapperConventions(
    this IServiceCollection services,
    Action<SqlNamingOptions>? configureNaming = null)
{
    var naming = new SqlNamingOptions();
    configureNaming?.Invoke(naming);
    services.AddSingleton(naming);
    return services;
}

// ✅ a required member arrives as a parameter, the delegate covers the rest
public static IServiceCollection AddOutbox(
    this IServiceCollection services,
    string connectionString,
    Action<OutboxOptions>? configure = null)
{
    var options = new OutboxOptions { ConnectionString = connectionString };
    configure?.Invoke(options);
    services.AddSingleton(options);
    return services;
}
```

---

## Neighbours

- [settings](settings.md) — the same values once a configuration section supplies them
- [extensions](extensions.md) — the `Add*` type that owns the delegate
