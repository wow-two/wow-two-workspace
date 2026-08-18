# Sql

*Last updated: 2026-08-17*

> Reaching the database through hand-written, ordered SQL scripts — apply, roll back, the tooling.
> Purpose — a schema change is a reviewable artifact; the script that ran records what shipped.
> Use case — writing a migration, choosing a dialect idiom, or shipping the migrator as a CLI.

## What lives here

- [bespoke migrations](bespoke-migrations.md) — the migrator's components, layout, drift and orphans
- [migration dialects](migration-dialects.md) — writing Apply and Rollback SQL, quoting, `@no-transaction`
- [migration tooling](migration-tooling.md) — the `dotnet tool` CLI, exit codes, destructive-op guard

---

## Boundary

- must pair every Apply with a Rollback, or state in the script why none exists.
- must never edit a script that has already run — a correction is a new migration.
