# Schema

*Last updated: 2026-08-17*

> What the database holds, provider-free — columns, types, keys, and the contracts an entity implements.
> Purpose — the schema is the contract both EF and hand-written SQL answer to, so it outlives either.
> Use case — adding a table or a column, or choosing how a change reaches the database.

## What lives here

- [database](database.md) — the schema-first rule, column constraints, type mappings
- [entity contracts](entity-contracts.md) — identity, audit, soft-delete, tenancy, concurrency
- [migration strategies](migrations.md) — picking `Ef`, `DbUp` or `Sql`, and what they share

---

## Boundary

- must keep a provider's type out — a `DbContext` and a connection belong to their own folder.
- must treat the applied SQL as canonical; a model implies a schema, it never defines one.
