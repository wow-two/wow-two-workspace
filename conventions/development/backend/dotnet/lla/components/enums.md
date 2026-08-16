# Enums

*Last updated: 2026-08-16*

> A closed set of named options, declared once and referred to everywhere.
> Purpose — replace a magic value with a name the compiler checks, before any store or service exists.
> Use case — reach here whenever a field may hold one of a fixed, known set.

## Location

### Folder
- must live in an `Enums/` folder beside the code that declares it.

### File
- `{Repo}.Domain/{Subdomain}/Enums/{Name}.cs` — **one file per enum** (per [code-organization.md](../notation/style/style.md)).
- Lives alongside its entities in the Domain assembly, under the owning subdomain folder.

---

## Declaration

### Type doc
- `/// <summary>` starts with **Defines** — per [documentation/summary.md](../notation/documentation/summary.md) starter table
- **name the question the enum answers, never its answers.** An enum is an axis; the members are points on it, and they are already in the declaration two lines down
- **the test: does the summary survive a new member?** A value list goes false the moment an eleventh arrives — that is the *inventory* shape of the falsifiability test ([summary.md](../notation/documentation/summary.md) § *The falsifiability test*)

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

### Type name
- **Singular** — no plural (`ChannelType` not `ChannelTypes`)
- **No `Enum` suffix** — `PipelineRunStatus` not `PipelineRunStatusEnum`
- **PascalCase values** — `Supply`, `Demand`, `ApartmentRent`

---

## Content

### Member docs
- `/// <summary>` on each value starts with **Refers to** — a value holds nothing, it names one choice (per [documentation/summary.md](../notation/documentation/summary.md) starter table) — then states what the value means
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

### Members
- **Backing type** — default `int`, no explicit values unless mapping to DB ordinals (rare; prefer PG enums)
- **No `[Flags]`** unless genuinely bitwise — most domain enums are not

---

## See also

- [../notation/documentation/summary.md](../notation/documentation/summary.md) — the starter table
- [../../mla/domains/persistence/database.md](../../mla/domains/persistence/database.md) — how a stored enum maps to a column
