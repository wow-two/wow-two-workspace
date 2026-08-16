# Enums

*Last updated: 2026-08-15*

> Domain enums — where they live, how they're documented, named, modeled, and mapped to a database column.
> Purpose — keep enums co-located with their entities and round-trip them losslessly across providers via shared SDK converters.
> Use case — reach for it when adding or persisting a domain enum (a closed set of states / categories / kinds).

---

## Location

- `{Repo}.Domain/{Subdomain}/Enums/{Name}.cs` — **one file per enum** (per [code-organization.md](../../lla/code-organization.md)).
- Lives alongside its entities in the Domain assembly, under the owning subdomain folder.

---

## Documentation

- The `/// <summary>` is the top line of the file — write it first, then the declaration below.

### Enum-level

- `/// <summary>` starts with **Defines** — per [documentation/summary.md](../../lla/documentation/summary.md) starter table
- **name the question the enum answers, never its answers.** An enum is an axis; the members are points on it, and they are already in the declaration two lines down
- **the test: does the summary survive a new member?** A value list goes false the moment an eleventh arrives — that is the *inventory* shape of the falsifiability test ([summary.md](../../lla/documentation/summary.md) § *The falsifiability test*)

The shape is `Defines the {axis} that {subject} {verb}s`:

```csharp
// ✅ the axis — still true when a member is added
/// <summary>Defines the category a channel falls into.</summary>
public enum ChannelType { Supply, Demand }

/// <summary>Defines how a code's symbol resolves.</summary>
public enum ContentMode { Static, Dynamic }

/// <summary>Defines the scan signal a routing rule matches on.</summary>
public enum RuleConditionType { Device, Country, Language, TimeOfDay }

/// <summary>Defines the lifecycle state of a subscription.</summary>
public enum SubscriptionStatus { … }

/// <summary>Defines the symbology a code renders as.</summary>
public enum BarcodeFormat { … }

// ❌ the answers — the em-dash clause is the value list, and it rots on the next member
/// <summary>Defines the category of a channel — supply (scraping listings) or demand (capturing inquiries).</summary>

// ❌ names the members outright
/// <summary>Defines url, text, wifi, vCard, calendar, phone, sms, email, geo and mobileApp.</summary>
```

### Value-level

- `/// <summary>` on each value starts with **Refers to** — a value holds nothing, it names one choice (per [documentation/summary.md](../../lla/documentation/summary.md) starter table) — then states what the value means
- **not `Represents`** — that starter claims the member *carries* its referent; an enum member only points at one option

```csharp
/// <summary>Defines the execution status of a pipeline run.</summary>
public enum PipelineRunStatus
{
    /// <summary>Refers to a run currently executing.</summary>
    Running,

    /// <summary>Refers to a run that finished successfully.</summary>
    Completed,

    /// <summary>Refers to a run that terminated due to an error.</summary>
    Failed,

    /// <summary>Refers to a run manually stopped before completion.</summary>
    Cancelled
}
```

---

## Naming

- **Singular** — no plural (`ChannelType` not `ChannelTypes`)
- **No `Enum` suffix** — `PipelineRunStatus` not `PipelineRunStatusEnum`
- **PascalCase values** — `Supply`, `Demand`, `ApartmentRent`

---

## Modeling

- **Backing type** — default `int`, no explicit values unless mapping to DB ordinals (rare; prefer PG enums)
- **No `[Flags]`** unless genuinely bitwise — most domain enums are not

---

## Database mapping

> **Standard:** native PostgreSQL enum types. Text columns are the fallback for non-PG providers (SqlServer / Sqlite) only — see *Text-column
> fallback*.

### Postgres (native enum types) — default

- **Storage** — PostgreSQL custom enum types (`CREATE TYPE listing_type AS ENUM (...)`).
- **C# ↔ PG case mapping** — PascalCase C# values map to snake_case PG labels (`ApartmentRent` ↔ `'apartment_rent'`).
- **Registration** — **one bulk call**, not per-enum, not per-property `.HasConversion()`. Call `MapEnums(CaseStyle.Snake, namespaceFilter,
  assemblies)` (`NpgsqlEnumMappingExtensions`) inside the `configure` delegate of `AddNpgsqlDataSource` (`PostgresServiceCollectionExtensions`).
- Npgsql requires enum mappings at the data-source (driver) level — `MapEnums` runs on the builder before `Build()`, scans the given assemblies, and
  registers every public non-nested enum that passes `namespaceFilter`.

```csharp
// Registration — once at startup
services.AddNpgsqlDataSource(builder =>
    builder.MapEnums(
        CaseStyle.Snake,
        ns => ns.StartsWith("Drydock.Domain"),
        typeof(ChannelType).Assembly));
```

**Why bulk, why a translator:**

- `MapEnums` derives the PG type name from the enum type name via `CaseConverter.ToCase(name, style)`.
- It routes both type and member names through a single `CaseStyleNameTranslator(style)` (an `INpgsqlNameTranslator`).
- Driver-level label mapping and any string-based mapping therefore agree *by construction* — they can't drift.
- No more listing each enum twice (`MapEnum<T>` on both `NpgsqlDataSourceBuilder` and `UseNpgsql`).
- **Per-enum PG type override** — pass the optional `pgTypeName` delegate to `MapEnums` (`Func<Type, string?>`; return `null` to keep the styled
  default).

---

### Text-column fallback (SqlServer / Sqlite)

- When the provider has no native enum types, store the enum as a **case-styled string** — reversibly, via the SDK converters.
- Never hand-roll `nameof(...).ToSnakeCase()` + `Enum.Parse`: that underscore-stripping pair is lossy on multi-word members. The SDK builds its
  reverse map from the enum's own members.
- **EF Core** — `EnumPropertyBuilderExtensions.HasEnumStringConversion<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
builder.Property(e => e.Status).HasEnumStringConversion();        // snake_case text column
```

- Applies `EnumCaseConverter<TEnum>` (a `ValueConverter<TEnum, string>`); reads are case-insensitive on the label, writes emit the configured style.
- **Dapper** — `DapperServiceCollectionExtensions.AddEnumTypeHandler<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
services.AddEnumTypeHandler<OrderStatus>();                       // registers EnumTypeHandler<OrderStatus>
```

- Both paths round-trip through `EnumNameConverter<TEnum>` (`ToLabel` / `Parse` / `TryParse`) — the single source of truth for label ↔ member,
  cached per `(enum, style)`.

> **Forward note:** a future text-enum-default mode (text as the standard, native PG opt-in) lands with the SQLite track. Until then, native PG
> enums are the standard and text columns are the non-PG fallback only.
