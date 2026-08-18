# Access

*Last updated: 2026-08-18*

> How code reaches a row — the path between a query and an object.
> Purpose — one schema is read two ways, each with its own rules; the schema stays out of both.
> Use case — writing a query, mapping a result, or picking a feature's path.

## Providers

| Provider | Reaches a row through | Docs |
|---|---|---|
| EF Core | a tracked `DbContext`, LINQ translated to SQL | [ef](ef/ef.md) · [ef mapping](ef/ef-mapping.md) |
| Dapper | an open connection, hand-written SQL, untracked | [dapper](dapper/dapper.md) |

- must not mix the two against one aggregate — a tracked write beside an untracked one loses the tracker's view.
- must keep engine facts out of both — a type mapping belongs to the [engine](../database/database.md).
