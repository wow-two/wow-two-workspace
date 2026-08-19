# Background services

*Last updated: 2026-08-19*

> A type the host starts and stops, doing its work off the request path.
> Purpose — give boot work and long-running loops a lifetime the host owns rather than a request's.
> Use case — reach here for a migration run at startup, a poller on a timer, or a queue drain.

## Location

### Folder
- must sit in a `BackgroundServices/` folder in the layer that owns the work it runs — never among the
  request-path `Services/`.

### File
- must give it its own file, named for the type →
  [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Runs** for work the host executes itself, once or continuously.
- must start with **Schedules** for work that decides when *other* work runs.
- must name what triggers the next run — startup, an interval, or an arriving message.

```csharp
// ✅ the work and its trigger
/// <summary>Runs EF Core migrations on application startup with connect-retry.</summary>
/// <summary>Schedules the classification sweep on the configured interval.</summary>

// ❌ names neither the work nor what starts it
/// <summary>Runs in the background.</summary>
```

### Type name
- must suffix with `BackgroundService`, whatever the work's shape — a loop and a one-shot boot task are
  the same role, registered the same way and stopped the same way.
- must not suffix with `HostedService` — every service the host runs is hosted, and a singleton is pinned
  too, so the word discriminates nothing.
- must prefix the suffix with what it watches — `ChannelObserveBackgroundService`.

---

## Content

### Member docs

#### [Summary](../../../lla/notation/documentation/summary.md)
- must carry `<inheritdoc />` on `ExecuteAsync` and `StartAsync` — the base already documents them.

#### [Remarks](../../../lla/notation/documentation/remarks.md)
- may carry `<remarks>` for the failure policy a reader has to act on — a retry budget, or a
  boot the host aborts.

```csharp
// ✅ the base carries the summary, the remark carries the policy
/// <inheritdoc />
/// <remarks>Retries the connection five times, then stops the host.</remarks>
protected override async Task ExecuteAsync(CancellationToken stoppingToken)

// ❌ a re-described summary duplicates the base and drifts from it
/// <summary>Executes the background work.</summary>
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
```

### Members
- must derive from `BackgroundService` and override `ExecuteAsync` for a long-running loop.
- must implement `IHostedService` and do the work in `StartAsync` for a one-shot boot task.
- must pass the stopping token to every await, so shutdown stays prompt.
- must resolve a scoped collaborator from `IServiceScopeFactory` per run — the host holds this
  type as a singleton.
- must use a block body `{ }` from the start — a run loop gains a guard, a scope, and a log line
  ([style](../../../lla/notation/style/style.md) § *The body*).
- must order the members `ExecuteAsync` or `StartAsync` first, then the private steps it calls.

---

## Neighbours

- [service.md](service.md) — the type it resolves per run
- [components](../constructs.md) — the `BackgroundService` row, and the `Scheduler` / `Observer` folds
- [host configuration](../../platform/startup/host-configuration.md) — registered in its own domain's `Add{Domain}()`
