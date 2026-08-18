# Unit of work

*Last updated: 2026-08-16*

> One transactional boundary around every change a use-case makes, committed once at its end.
> Purpose — keep the commit point at the use-case, so a partial write is impossible rather than merely unlikely.
> Use case — reach here when a handler writes more than one row and both writes must land together.

## Shape

- must use the `DbContext` as the unit of work on the EF path — it tracks the changes, and `SaveChangesAsync`
  is the commit.
- must not declare an `IUnitOfWork` interface wrapping it; the wrapper adds a name and hides the tracker
  ([database](../../domains/persistence/schema/database.md)).
- must call `SaveChangesAsync` **once per use-case**, in the handler that owns it — never inside a repository method.
- must open an explicit transaction only when the work spans two contexts or mixes EF with raw SQL; otherwise
  `SaveChangesAsync` already runs in one.
- must accept that the Dapper path has **no** unit of work — one fresh connection per operation, so multi-statement
  atomicity is the SQL's job ([repository](../behavior/repository.md) § *Connections*).

```csharp
// ✅ the handler owns the commit point
await orders.AddAsync(order, ct);
await inventory.ReserveAsync(order.Items, ct);
await context.SaveChangesAsync(ct);
```

---

## Use

- must reach for the pattern in a command handler writing more than one aggregate.
- must reach for it when an outbox row must commit with the state change ([outbox](outbox.md)).
- must reach for an explicit transaction when a migration-time or admin operation spans several statements.

---

## Limits

- must not commit inside a repository — a repository that saves takes the commit point away from the use-case.
- must not span a transaction across an out-of-process call — a broker call inside one holds a lock on the network.
- must not share a `DbContext` across requests or across threads — it is scoped, and it is not thread-safe.
- must not use a transaction to make a query consistent; that is an isolation level, set deliberately.

---

## Components

- [repository](../behavior/repository.md) — the write side, and why the Dapper path owns no transaction.
- [database](../../domains/persistence/schema/database.md) — the `DbContext` contract and the schema-first rule.
- [outbox](outbox.md) — the messaging half that must share the same commit.
- [handler](../behavior/handler.md) — the handler that owns the boundary.
