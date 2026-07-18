# Models

*Last updated: 2026-06-22*

General rules for all C# models (entities, result types, DTOs, settings, value objects).

## Record style

Records use **body properties with `{ get; init; }`** — not positional constructors (primary ctors). Applies to entities, DTOs, results, and all data-carrying records.

**Why:** Positional constructor parameters don't support standard XML doc comments (`/// <summary>`). Body properties do.

**Exception:** Primary constructors are fine for **DI injection** (services, controllers, handlers) where XML docs on parameters aren't needed.

```csharp
// ✅ Correct — body properties with XML docs
public sealed record PipelineDto
{
    /// <summary>Gets the kebab-case pipeline id.</summary>
    public required string Id { get; init; }

    /// <summary>Gets the display name.</summary>
    public required string Name { get; init; }
}

// ❌ Wrong — positional ctor, XML docs don't attach to parameters
public sealed record PipelineDto(string Id, string Name);

// ✅ OK — primary ctor for DI injection (no XML docs needed)
public class ChannelsController(
    PipelineRegistry registry,
    PipelineExecutionTracker tracker) : ControllerBase
```

## `sealed record` everywhere

Default to `sealed record` for every data carrier. Open `record` (non-sealed) only when intentionally designed for inheritance — which is rare and usually a code smell.

## Member rules

### Required vs init defaults

- **`required`** on every non-nullable property whose value must come from outside the constructor (caller, EF, binder)
- **No default values** unless the property is genuinely optional — applies to **all** models; a generic-role model that genuinely needs a default is
  an **explicit override documented in its own convention** (e.g. a tuning `Options` type — see [component-names.md](../foundation/component-names.md)
  `Settings` vs `Options`), never an ad-hoc default sprinkled in
- **Init-only** (`{ get; init; }`) for immutable models — settings, DTOs, value objects
- **Get-set** (`{ get; set; }`) for entities — EF Core requires set accessors

### Nullability

- Non-nullable by default — use NRT (`string`, not `string?`)
- `?` on the type when the value is genuinely optional
- Never `string.Empty` or `[]` as a default for a non-nullable — leave it required

### Collections

- Always `List<T>` for collection-typed properties (EF Core compat, Npgsql array mapping, mutability for `Add`)
- Never `T[]`, `ICollection<T>`, `IEnumerable<T>`, `IReadOnlyList<T>` on entities
- Three patterns (see [entities.md](../persistence/entities.md) for entity-specific guidance):
  - `public required List<T> Prop { get; set; }` — always-populated value collections
  - `public List<T> Prop { get; set; } = null!;` — EF navigation properties
  - `public List<T>? Prop { get; set; }` — genuinely optional collections

## Documentation

Every public model gets `/// <summary>` (required). Properties get `/// <summary>` too.

Per the starter table in [documentation.md](documentation.md):

| Kind | Summary starter |
|---|---|
| Entity | **Represents** |
| DTO | **Represents** (or projection-shape description) |
| Settings | **Configuration for** |
| Result base | **Represents the outcome of** |
| Value object | **Represents** |

## Naming

- **Entities** — suffix with `Entity` when the type maps 1:1 to a DB table (`ChannelEntity` → `channels` table)
- **Value objects within entities** — no suffix (`PipelineRun`, `NodeRun`)
- **DTOs** — suffix with `Dto` (`ChannelDto`, `ChannelWithPipelinesDto`)
- **Settings** — suffix with `Settings` (`ClassificationSettings`)
- **Results** — suffix with `Result` (`ChannelGetAllResult`)
- **Query/Command** — suffix with `Query` / `Command` (`ChannelGetAllQuery`, `PipelineExecuteCommand`)

## Introducing a model — the exclusive-members bar

Reuse the model you have. A new type earns its place only by carrying **exclusive members** — data the existing model can't express. A type whose members are a **subset** of an existing one is a lean copy: it adds no information, and every field becomes a second place to change.

- must not introduce a model whose members are a subset of an existing model — pass the existing type — **unless the existing model can't fill that role**
- the bar targets a **second representation of the same instance** — a projection / lean copy that exists *instead of* the source at another boundary
- **role-distinct types are exempt**: siblings in a discriminated union co-exist *alongside* each other in one collection, as different things, not one thing twice
- the subset relation is then accidental; the discriminator is the load-bearing member
- test: could the existing type carry this instance? subset + **yes** → lean copy, delete it. subset + **no** → distinct role, keep it
- forcing the reuse would add nullable members that only exist to be absent — a signal the roles differ (e.g. a default rule needs no `Order` / `Condition`)
- must justify a new model by an **exclusive member**: a field the source lacks (a derived/resolved value, a precomputed order, a caller-supplied knob) — "fewer fields" / "a lighter shape" is not a justification
- **serialization is a real reason, but only once real** — a lean shape to cache / put on a wire earns its keep when something actually caches or sends it; a projection built for a store nothing writes to is speculative, delete it and reintroduce it with the cache
- prefer the **entity** on read paths that already load it; project only at a boundary that can't take the entity (the wire — that's a `Dto`; see § Naming)

Exempt example (smart-qr): `DefaultRule { Content }` is a strict subset of `ConditionalRule { Order, Condition, ConditionValue?, Content }`, and stays. They're siblings in the `CodeRule` union — a code holds both at once, so neither can carry the other's instance. Reusing `ConditionalRule` for a default would force `Order` and `Condition` nullable on a rule that is never matched and never ordered.

Counter-example (smart-qr, removed): `CodeRouteConfig` mirrored `CodeEntity` (`CodeId`·`IsActive`·`NeverExpires`·`ExpiresAt`·`Rules`) with no exclusive member — its `Slug`/`ScanCount` were dead in the resolver, and its stated reason (a Redis cache payload) never materialized: nothing wrote the key. The redirect resolves on `CodeEntity` instead. A routing model would have earned its place by carrying something the entity lacks — e.g. rules pre-ordered for the hot path.

## Polymorphic models

A discriminated union over a `type` field — never hand-author the discriminator strings in `[JsonDerivedType]` attributes; they drift from the enum (`nameof` yields PascalCase, a typed value goes stale, casing slips — `vCard` vs `vcard`).

- must drive the polymorphism from the discriminator **enum** — a `DefaultJsonTypeInfoResolver` modifier builds `JsonPolymorphismOptions.DerivedTypes`, each type's discriminator = its enum value serialized through the wire's string-enum converter (so `[JsonStringEnumMemberName]` overrides are honored — the enum member stays the single source)
- must not scatter `[JsonPolymorphic]` / `[JsonDerivedType]` on the base — the resolver is the one place
- reference impl: `SmartQr` `CodeContentPolymorphism`; extract the reusable resolver to `WoW.Two.Sdk.Backend.Beta` once a 2nd union appears

## See also

- [entities.md](../persistence/entities.md) — entity-specific modeling rules
- [enums.md](../persistence/enums.md) — enums
- [settings.md](../runtime/settings.md) — settings records
- [result-pattern.md](../foundation/result-pattern.md) — Result type structure
- [code-organization.md](code-organization.md) — file-per-type
- [documentation.md](documentation.md) — XML doc + starter table
