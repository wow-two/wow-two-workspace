# Services

*Last updated: 2026-08-15*

Application and infrastructure services that contain business logic, data access, or integration code.

## Location

Services live in the layer that matches their responsibility (see [service-architecture.md](../layers/layers.md)):

| Layer | Folder | Examples |
|---|---|---|
| Application | `Application/Services/` | `IChannelStatsService` (interface) |
| Infrastructure | `Infrastructure/Services/` | `PipelineSeedService`, `PipelineConfigService` |
| Common (shared across services) | `{Repo}.Common/...` | `PipelineRegistry`, shared services |

Interface in `Application/`, implementation in `Infrastructure/` — the Clean Arch dependency rule.

## Modeling

### Class shape

- **Non-static** class
- **Primary constructor** for DI injection (allowed exception to the body-property rule for records — see [models.md](../../lla/models.md))
- **Sealed** unless intentionally designed for inheritance — `sealed` should be the default

### Lifetime

Register in the appropriate `HostConfigurationExtensions` method (see [host-configuration.md](../platform/host-configuration.md)):
- **Singleton** — stateless, thread-safe, expensive to construct
- **Scoped** — request-scoped state, holds DbContext or similar
- **Transient** — lightweight, no caching benefit

## Naming

The canonical suffix→role vocabulary — keep-list, folds, banned list, and the new-suffix gate — is
[component-names.md](components.md), and it is the only authority. This doc adds no rows and restates none;
a suffix question is answered there.

This doc governs what a `Service` **is** and how it is shaped, not what the suffix set contains.

## Documentation

Per the starter table in [documentation/summary.md](../../lla/documentation/summary.md):

### Service class

- `/// <summary>` starts with **Provides**
- `/// <remarks>` only when a caller needs a directive, a spec reference, or a non-obvious constraint ([remarks.md](../../lla/documentation/remarks.md) § *What it carries*) — never required

```csharp
/// <summary>Provides channel and pipeline seeding on application startup.</summary>
/// <remarks>
///   1. Read channels from the seed file
///   2. Upsert channels and sources via EF Core
///   3. Insert missing pipeline rows with code defaults
/// </remarks>
public class ChannelsSeedService { }
```

### Factory class

- `/// <summary>` starts with **Creates**

```csharp
/// <summary>Creates AI clients keyed by provider and model tier.</summary>
public class AiClientFactory { }
```

### Registry / tracker / constants class

- `Registry` → **Binds** · `Tracker` → **Tracks** · static constants class → **Contains**

```csharp
/// <summary>Binds each pipeline slug to its handler type.</summary>
public class PipelineRegistry { }

/// <summary>Tracks live pipeline executions keyed by pipeline id.</summary>
public class PipelineExecutionTracker { }

/// <summary>Contains the canonical kebab-case slugs for every channel.</summary>
public static class ChannelSlugs { }
```

### Method docs

- `/// <summary>` one-liner — start with a verb (`Gets`, `Sends`, `Creates`, `Builds`)
- Multi-step methods may add `/// <remarks>` with a numbered flow — capped at 5 lines, tags included, and only after gates 1 and 2
  ([remarks.md](../../lla/documentation/remarks.md) § *Multi-line — the same three gates*)

## See also

- [clients.md](client.md) — HTTP API wrappers
- [data-access.md](repository.md) — Dapper repositories
- [host-configuration.md](../platform/host-configuration.md) — DI registration
- [documentation/summary.md](../../lla/documentation/summary.md) — the canonical `<summary>` starter table
- [documentation.md](../../lla/documentation.md) — XML doc format + the three gates
