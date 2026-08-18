# Services

*Last updated: 2026-08-18*

> The fallback behavior component — business logic, orchestration or compute with no narrower role.
> Purpose — every verb that is not another component's is still a named responsibility.
> Use case — reach here only after the [gate](../constructs.md) § *Adding a new suffix* returns four `no`s.

## Location

### Folder
- must sit in a `Services/` folder under the domain that owns the work.

### File
- must give each service its own file, named for the type.

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Provides**, and name the work it does for its caller.
- must carry `<remarks>` only for a directive, a spec reference, or a constraint the signature hides.

```csharp
// ✅ names the work, not the type
/// <summary>Provides channel and pipeline seeding on application startup.</summary>
// ❌ restates the suffix, so the responsibility stays unsaid
/// <summary>Provides the channel service.</summary>
```

### Construct
- must declare a `sealed class` with a primary constructor for its collaborators.
- must use a block body `{ }` from the start — a guard, a retry or a log line arrives later
  ([style](../../../lla/notation/style/style.md) § *The body*).

### Type name
- must suffix with `Service`, prefixed by the work — `ChannelsSeedService`.
- must reach for the narrower suffix when one fits — a `Service` that only maps is a `Mapper`.
- must return a `Result` carrying a [model](../data/model.md) — never a `Dto`, never a bare value.

```csharp
// ✅
public sealed class PipelineConfigService(IPipelineRepository repository)
// ❌ `Manager` names no verb
public sealed class PipelineManager
```
