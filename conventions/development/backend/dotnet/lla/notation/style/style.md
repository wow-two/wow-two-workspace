# Style

*Last updated: 2026-08-16*

> What the text inside a file looks like — its order, its wrapping, its width.
> Purpose — remove every per-file judgment call about layout so a diff shows meaning, not formatting.
> Use case — reach here while writing or reviewing the body of any file.

## One file per type [REQUIRED]

Every public type lives in its own `.cs` file. The file name matches the type name.

### Exception: generic + non-generic pair

When a non-generic type exists **only** as a convenience alias for a specific generic form, the pair lives in the same file:

```csharp
// ✅ IEntity.cs — non-generic + generic abstract pair
public interface IEntity : IEntity<Guid>;

public interface IEntity<TId>
{
    TId Id { get; }
}
```

Conditions for the same-file exception:
- The non-generic type is the **abstract** convenience form (`IEntity` is just `IEntity<Guid>` with no extra members)
- Both types are at the same abstraction level (both interfaces, or both abstract classes)
- Together they read as one concept with a default-type overload

### What does NOT qualify for the exception

| Case | Resolution |
|---|---|
| Concrete specialization (`public interface IFoo : IFoo<Guid> { string Name { get; } }`) — adds members | Separate file |
| Unrelated types in the same file (e.g. `IAuditable` + `IHasTenant` — independent traits) | Split |
| Sibling types around the same theme (`ISoftDeletable` + `ISoftDeletableBy`) | Split — they have different shapes |
| Result type with nested `Success`/`Failure` (nested classes inside one abstract base) | **Same file** — these are sealed inner classes of one type, not separate types |

### Nested types

Nested types (sealed inner classes, value-object records inside a parent) live in the parent's file when they exist **only** to model variants/states of the parent. Example: `Result<T>` with nested `Success` and `Failure` lives in `Result.cs`.

### File naming

- File name = primary type name + `.cs` (`Channel.cs`, `IEntity.cs`, `ChannelGetAllQuery.cs`)
- For the generic+non-generic exception, the non-generic name wins (`IEntity.cs`, not `IEntity{T}.cs`)
- Generic-only types use the simple base name (`Repository.cs` for `Repository<T>`)

## Section dividers

- **Never** use ASCII art dividers — no `// ═══`, `// ---`, `// ***`, or similar C/C++ block separators
- **Never** use dotted/dashed inline comments — no `// ---- Section name ----` or `// -- Section name --`. Use plain comments: `// Section name`
- **Use `#region` / `#endregion`** when a file has distinct logical sections that benefit from collapsing (e.g. internal row types, dimension queries, WHERE builder)
- **Use nothing** when sections are small or obvious — not every group of methods needs a divider
- **Lightweight inline labels are fine** — `// ── Tables ──` or `// ── Meta ──` for small field groups within a class

```csharp
// ❌ Wrong — C++ style block divider
// ══════════════════════════════════════════════════════════════════════════
// Internal row types
// ══════════════════════════════════════════════════════════════════════════

// ✅ Correct — #region for collapsible sections
#region Internal row types
// ...
#endregion

// ✅ Correct — lightweight inline label for field groups
// ── Tables ──
private static readonly string ListingsTable = ListingEntity.TableName;
```

## Parameter formatting

- **More than 2 parameters** — multiline (one parameter per line)
- **2 or fewer parameters** — single line
- Applies to: method signatures, method calls, constructor calls, `new` expressions

```csharp
// ✅ Correct — 2 params, single line
var (where, parameters) = BuildWhere(filter, exclude: "district");

// ✅ Correct — >2 params, multiline
var propertyTypesTask = QueryDimensionAsync(
    nameof(ListingEntity.PropertyType),
    filter,
    exclude: "propertyType",
    ct: ct);

// ✅ Correct — >2 params in nested call
var rows = await conn.QueryAsync<DimensionRow>(
    new CommandDefinition(
        sql,
        parameters,
        cancellationToken: ct));

// ❌ Wrong — >2 params on single line
var rows = await conn.QueryAsync<DimensionRow>(new CommandDefinition(sql, parameters, cancellationToken: ct));
```

## Raw string literals

- **Opening `"""`** always on its own line (never inline with `var sql =`)
- **Closing `"""`** on its own line, at the indentation level that controls the content's left margin
- Applies to: SQL, JSON, XML, any multiline string content

```csharp
// ✅ Correct — """ on its own line
var sql =
    $"""
     SELECT ...
     FROM ...
     """;

// ✅ Correct — in switch expression
var sql = kind switch
{
    DimensionKind.Integer =>
        $"""
         SELECT ...
         FROM ...
         """,
};

// ❌ Wrong — """ inline with assignment
var sql = $"""
    SELECT ...
    FROM ...
    """;
```

## Line length [REQUIRED]

**120 characters, hard.** Rider and ReSharper draw their right margin there by default, so the guide is already on screen; the limit is what keeps two files legible side by side on a 1920 display.

- Applies to every line — code, XML doc comments, string literals in source.
- **Doc comments break the limit most often, and this limit is the *last* gate they pass.** Run the three gates in `documentation.md` § *Three gates* first — convention, then compaction, then length. A block wrapped without that pass hides the defect that made it long.
- Only a block that survives both earlier gates and still exceeds 120 goes multi-line, tags on their own lines:

```csharp
// ✅ Correct — the block wraps, each line under 120
/// <summary>
/// Shared payload-encoding primitives for the static <see cref="CodeContent"/> types — escaping and formatting
/// helpers ported byte-for-byte from the frontend's <c>contentTypes.ts</c>, so a code encoded here decodes
/// identically to one the builder previewed.
/// </summary>

// ❌ Wrong — one 240-char line, unreadable in a split pane and in a diff
/// <summary>Shared payload-encoding primitives for the static <see cref="CodeContent"/> types — escaping and formatting helpers ported byte-for-byte from the frontend's <c>contentTypes.ts</c>, so a code encoded here decodes identically to one the builder previewed.</summary>
```

- **Code over 120** wraps at the natural boundary — one argument per line, one LINQ operator per line, one object-initializer member per line. No justification needed; the chain's shape is the reason.
- **Exempt:** a single string literal or URL that cannot be split without changing its value (a user-agent, a connection string, a token in a comment), and generated code. Concatenating one across lines to satisfy the limit costs more than it buys.
- No second, looser tier. 150 is outside every mainstream standard (Prettier 80 · Black 88 · Google Java 100 · rustfmt 100 · ktlint 120), and two 150-char panes no longer fit a 1920 display.

## SQL line length

- **Long SQL clauses** — break into one column/condition per line when a line exceeds ~120 chars
- **SELECT** — one column per line when >2 columns
- **JOIN ON** — one condition per line when >1 condition
- **WHERE** — one condition per line
- Keep SQL keywords (`SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `ORDER BY`) at the start of their line

```csharp
// ✅ Correct
var sql =
    $"""
     SELECT
         {Col("LandmarkId", Lls)} AS value,
         {Col("Name", Lm)} AS label,
         COUNT(DISTINCT {Col("Id", Sl)}) AS count
     FROM {ListingsTable} {Sl}
     JOIN {SignalsTable} {Lls}
         ON {Col("ListingId", Lls)} = {Col("Id", Sl)}
         AND {Col("SignalType", Lls)} = 'district'
         AND {Col("LandmarkId", Lls)} IS NOT NULL
     WHERE 1=1 {where}
     GROUP BY
         {Col("LandmarkId", Lls)},
         {Col("Name", Lm)}
     ORDER BY count DESC
     """;
```

## File-scoped namespaces

Required everywhere. Block namespaces are not used.

```csharp
// ✅ Correct
namespace WoW.Two.Sdk.Backend.Beta.Data.Abstractions;

public interface IEntity { Guid Id { get; } }
```

## `using` ordering

- `System.*` first, then `Microsoft.*`, then third-party, then project namespaces — IDE auto-sort handles this; do not hand-order
- No unused `using` statements (analyzer enforces)
- **`using static` is banned** — it strips the owning class off the call site; call through the class or make the method a real extension method. Rule + rationale: [naming.md](../naming/naming.md) § *`using static` is banned*


## Directives

Neither a construct nor a statement — a directive declares no type and runs nothing; it changes what a file can see.

| Directive | Verdict | Rule |
|---|---|---|
| `using {namespace}` | use | ordered per § *`using` ordering* |
| `global using` | use with care | one file per project owns them; a scattered `global using` is invisible at the call site |
| `using {alias} = {type}` | use with care | only to disambiguate two types with the same name in one file |
| `using static` | banned | write the type name at the call site — the call loses its subject otherwise |
| `extern alias` | banned | two assemblies exporting one type is a packaging fault, fixed upstream |

## Preprocessor

| Directive | Verdict | Rule |
|---|---|---|
| `#nullable` | use | only to enable; a per-file disable hides a real warning |
| `#if` · `#elif` · `#else` · `#endif` | use with care | a build-configuration branch, never a feature switch |
| `#region` · `#endregion` | use with care | per § *Section dividers* |
| `#pragma warning` | use with care | must name the warning and carry a `//` saying why |
| `#line` · `#error` · `#warning` | use with care | generator output and build-time assertions only |

## Banned

- `dynamic` — reach for generics or polymorphism.
- `BinaryFormatter` — unsafe deserialization, no supported replacement path.
- `using static` — write the type name at the call site ([../naming/naming.md](../naming/naming.md) § *`using static` is banned*).
- `.GetAwaiter().GetResult()` · `.Result` · `.Wait()` — `await`, or the async host hook
  ([../../mla/platform/host-configuration.md](../../../mla/platform/host-configuration.md) § *Async startup*).

## `var` — preferred, with one exception

- must use `var` when the initializer names the type — `var codes = new List<CodeEntity>();` repeats nothing.
- must write the type when the initializer does **not** show it — a method call returning an unobvious type, a ternary, a chained LINQ result.
- the rule is not a ban: `var` is the default, and spelling the type is the exception it earns.

## See also

- [../organization/organization.md](style.md) — which file the code goes in
- [../shape/shape.md](../../constructs/constructs.md) — what form the declaration takes
