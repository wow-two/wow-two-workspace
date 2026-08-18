# Persistence

*Last updated: 2026-08-18*

> How a service stores and reads its own state, cut into the four things that swap independently.
> Purpose — an entity is not tied to an engine, an engine not to a mapper, neither to a migrator.
> Use case — adding a table, choosing how code reaches it, or changing the schema.

## Contract

- must treat the applied SQL as canonical — the schema is what shipped, never what a model implies.
- must keep the [entity](../../constructs/data/entity.md) free of any provider type.
- must express a schema change as a migration, never as a hand-edit against a live database.

---

## The four axes

| Axis | Answers | Lead |
|---|---|---|
| [entities](entities/entity-contracts.md) | what a persisted type implements | identity, audit, soft-delete, tenancy |
| [database](database/database.md) | which engine, and what it fixes | types, enum forms, column conventions |
| [access](access/access.md) | how code reaches a row | EF tracked, Dapper untracked |
| [migrations](migrations/migrations.md) | how the schema changes | `sql` · `dbup` · `ef` |

- must place a rule at the axis that owns it — a type mapping is the engine's, a configuration API is access's.
- must not assume one axis implies another; a Dapper service still needs an engine and a migrator.

---

## Testing

- [test databases](testing/test-databases.md) — the tiers a test picks from, and what each resets.
