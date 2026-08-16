# Enums

*Last updated: 2026-08-16*

> A closed set of named options, declared once and referred to everywhere.
> Purpose — replace a magic value with a name the compiler checks, before any store or service exists.
> Use case — reach here whenever a field may hold one of a fixed, known set.

## Location

### Folder
- must sit in an `Enums/` folder beside the code that declares it.

### File
- must give each enum its own file, named for the type.

## Declaration

### Type doc

#### [Summary](../notation/documentation/summary.md)
- must start with **Defines**.
- must name the question the enum answers, never its answers.
- must survive a new member — a summary that lists values goes false the moment an eleventh arrives.

```csharp
// ✅ the axis
/// <summary>Defines the execution status of a pipeline run.</summary>
// ❌ an inventory, false on the next member
/// <summary>Defines Pending, Running, Completed and Failed.</summary>
```

### Type name
- must be singular — `ChannelType`, never `ChannelTypes`.
- must carry the domain noun and nothing else — `PipelineRunStatus`, never `PipelineRunStatusEnum`.

## Content

### Member docs

#### [Summary](../notation/documentation/summary.md)
- must start with **Refers to**, then state what the option means.

```csharp
// ✅ the member names one option
/// <summary>Refers to a run that finished successfully.</summary>
Completed,

// ❌ Represents claims the member carries its referent
/// <summary>Represents a completed run.</summary>
```

#### [Remarks](../notation/documentation/remarks.md)
- must carry `<remarks>` only for a constraint a consumer would otherwise get wrong.

### Members
- must be PascalCase — `Supply`, `ApartmentRent`.
- must take the default `int` backing type.
- must use `[Flags]` only when the members are genuinely bitwise.
- must place a default or unset member first.
- must order the rest by their own level when one exists, ascending or descending, and by declaration order otherwise.

```csharp
// ✅ default first, then ascending severity
None,
Low,
Medium,
High,

// ❌ no order a reader can predict
High,
None,
Medium,
```

## See also

- [../notation/documentation/summary.md](../notation/documentation/summary.md) — the starter table
- [../../mla/domains/persistence/database.md](../../mla/domains/persistence/database.md) — how a stored enum maps to a column
