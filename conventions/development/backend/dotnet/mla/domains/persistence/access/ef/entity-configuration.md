# Entity configurations

*Last updated: 2026-08-16*

> The EF Core mapping for one entity, declared away from the entity itself.
> Purpose — keep the ORM out of the Domain assembly, so an entity stays a plain record.
> Use case — reach here when a persisted type needs a table, a column type, a conversion or a relation.

## Location

### Folder
- must sit in a `Configurations/` folder in the Persistence layer.

### File
- must give each configuration its own file, named for the type.
- may share one file with a sibling configuration when the two entities are tightly coupled.

---

## Declaration

### Type doc

#### [Summary](../../../../../lla/notation/documentation/summary.md)
- must start with **Configures**.
- must name the entity it maps and the table that entity lands in.

```csharp
// ✅ the entity and its table
/// <summary>Configures the listing entity and its listings table.</summary>

// ❌ Represents belongs to the entity, and the table is left a guess
/// <summary>Represents the listing mapping.</summary>
```

### Type name
- must declare `{Entity}Configuration : IEntityTypeConfiguration<{Entity}>`.

---

## Content

### Member docs

#### [Summary](../../../../../lla/notation/documentation/summary.md)
- must carry `<inheritdoc />` on `Configure` — `IEntityTypeConfiguration<T>` already documents it.

#### [Remarks](../../../../../lla/notation/documentation/remarks.md)
- may carry `<remarks>` for a mapping the builder calls do not show — a JSON comparer, a
  provider column type, a storage casing the naming convention supplies.

```csharp
// ✅ the contract carries the summary, the remark carries what the calls hide
/// <inheritdoc />
/// <remarks>Columns resolve through the snake_case naming convention.</remarks>
public void Configure(EntityTypeBuilder<ListingEntity> builder)

// ❌ a re-described summary duplicates the interface and drifts from it
/// <summary>Configures the listing entity.</summary>
public void Configure(EntityTypeBuilder<ListingEntity> builder)
```

### Members
- must declare `Configure` as the type's only public member.
- must use a block body `{ }` from the start — the builder chain gains a call with every mapping added
  ([style](../../../../../lla/notation/style/style.md) § *The body*).
- must configure what changes runtime behaviour — the table, the key, column types, conversions,
  relations ([ef mapping](ef-mapping.md) § *EF Core entity type configurations*).
- must leave the schema itself to the migration, which owns every DDL-only concern.
- must order the calls table and key, column types, conversions, then relationships.

---

## Neighbours

- [entity.md](../../../../constructs/data/entity.md) — the record this maps
- [database](../../database/database.md) — type mappings, conventions, interceptor wiring
- [constructs](../../../../constructs/constructs.md) — the `Configuration` row
