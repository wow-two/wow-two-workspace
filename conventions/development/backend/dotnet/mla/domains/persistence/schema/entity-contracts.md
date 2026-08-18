# Entity contracts

*Last updated: 2026-08-16*

> The interfaces a persisted type implements — identity, audit, soft-delete, tenancy and concurrency.
> Purpose — contracts live in a zero-ORM package, so the Domain assembly never references EF Core.
> Use case — shaping a new [entity](../../../constructs/data/entity.md), or wiring an interceptor that stamps one.

## Identity

- must implement `IKeyedEntity<TId>` on every type that owns a row — `where TId : notnull, IEquatable<TId>`.
- must use `Guid` as the standard `TId`.
- must reserve the bare `IEntity` marker for keyless read shapes — a projection or a view-backed read.
- must not use bare `IEntity` on a type that needs an `Id`.

---

## Members

- must be non-nullable unless the column is genuinely optional.
- must be `required` with `{ get; set; }` when persistence always returns the value.
- must drop `required` and initialize with `null!` when the value is not always loaded — relations, joined fields.
- must use `List<T>` for a collection.
- must map a `List<TEnum>` to a PG enum array type (`tenant_type[]`), never `TEXT[]`.

---

## Traits

Single-purpose interfaces, never base classes — an entity composes exactly the traits it has.

| Concern | Interface | Adds |
|---|---|---|
| creation timestamp | `ICreationAuditable` | `CreatedAt` |
| update timestamp | `IModificationAuditable` | `UpdatedAt` |
| both timestamps | `IAuditable` | the union of the two |
| creation actor | `ICreationAuditableBy<TUserId>` | `CreatedBy` |
| update actor | `IModificationAuditableBy<TUserId>` | `UpdatedBy` |
| both actors | `IAuditableBy<TUserId>` | the union of the two |
| soft delete | `ISoftDeletable` | `IsDeleted`, `DeletedAt` |
| soft-delete actor | `ISoftDeletableBy<TUserId>` | `DeletedBy` |
| tenant scope | `IHasTenant<TTenantId>` | `TenantId` |

- must take creation-only audit on an append-only type — a phantom `UpdatedAt` claims a lifecycle it has not got.
- must let the interceptor stamp creation once and pin it on update; `CreatedAt` never changes after insert.
- must use a struct as `TUserId` — the `*By<TUserId>` interfaces constrain it, and `Guid` is the standard.
- must implement a composite only when both halves apply.

---

## Concurrency

Optimistic-concurrency tokens are mutually exclusive — an entity implements at most one, matching its store.

| Store | Interface | Token |
|---|---|---|
| provider-agnostic | `IVersioned` | `Version` (`uint`) |
| Postgres | `IHasXmin` | `Xmin` (`uint`) |
| SQL Server | `IRowVersioned` | `RowVersion` (`byte[]`) |

- must not stack two tokens on one entity.
