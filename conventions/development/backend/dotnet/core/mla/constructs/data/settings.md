# Settings

*Last updated: 2026-08-19*

> The record a configuration section binds into — one typed shape per section.
> Purpose — configuration read as strings fails at the point of use; bound as a record it fails at boot.
> Use case — any value that differs per environment or per deployment.

## Location

### Folder
- must sit in a `Settings/` folder under the domain the section configures.

### File
- must give it its own file, named for the type →
  [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Holds**, and name the section it binds.
- must state the section key when the type name does not give it away.

```csharp
// ✅ names the section
/// <summary>Holds the Postgres connection settings.</summary>
// ❌ describes the mechanism instead of the section
/// <summary>Settings bound from appsettings.</summary>
```

### Construct
- must declare a `sealed record` → [data](data.md) § *Declaration*.
- must declare `{ get; init; }` — the binder writes once, at startup.
- must carry no default value on any member — a missing setting fails the boot rather than running wrong.

### Type name
- must suffix with `Settings` — `PostgresSettings`, `GoogleAuthSettings`.
- must name the section, never the consumer — no `CodeServiceSettings` for a shared section.

---

## Neighbours

- [settings](../../components/settings.md) — binding, validation, and where the section is registered
