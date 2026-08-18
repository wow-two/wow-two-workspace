# Persistence

*Last updated: 2026-08-16*

> How a service stores and reads its own state — the schema it guarantees, and the providers that reach it.
> Purpose — an entity is provider-free; a `DbContext` and a connection are not. The split keeps a model portable.
> Use case — adding a table, choosing a migration strategy, or reaching the database from code.

## Contract

- must treat the applied SQL as canonical — the schema is what shipped, never what a model implies.
- must keep the [entity](../../constructs/data/entity.md) free of any provider type.
- must express a schema change as a migration, never as a hand-edit against a live database.
- [schema](schema/database.md) — column constraints, type mappings, and the schema-first rule.
- [migration strategies](schema/migrations.md) — pick `Ef`, `DbUp` or `Sql`, and what they share.
- [test databases](test-databases.md) — the tiers a test picks from, and what each resets.

---

## Providers

| Provider | Reaches the database through | Docs |
|---|---|---|
| EF Core | a `DbContext`, mapped by `IEntityTypeConfiguration<T>` | [ef migrations](ef/ef-migrations.md) |
| Dapper | an `IDbConnectionFactory` and hand-written SQL | — |
| bespoke SQL | ordered `Apply.sql` / `Rollback.sql` scripts | [bespoke](sql/bespoke-migrations.md) · [dialects](sql/migration-dialects.md) · [tooling](sql/migration-tooling.md) |
| DbUp | forward-only scripts, no rollback | [dbup](dbup/dbup-migrations.md) |

- must pick one migration strategy per service, and not mix two against one database.
- must keep a provider's types inside its own folder's rules — a repository is not tied to EF by existing.
