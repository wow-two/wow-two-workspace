# Documentation

*Last updated: 2026-06-22*

> XML-doc index/baseline — the cross-cutting format + the required-tags table, with per-block conventions (`<summary>`, `<remarks>`, `<param>`, `<returns>`, `<exception>`) split into `documentation/`.

## XML doc format

- **One-liner by default** — `<summary>`, `<remarks>` content is a compact single line
- **Inline tags** — opening and closing tags on the same line as the content
- **`and`, not `+`** — write `and` in prose (summaries, remarks, inline comments); never `+`, which reads as a code operator — `PG and SQLite`, not `PG + SQLite`

```csharp
// ✅ Correct — compact one-liner, tags inline
/// <summary>Defines a handler for extracting phone numbers from a listing via HTTP.</summary>
/// <remarks>Single responsibility — no image extraction, no browser dependency.</remarks>

// ❌ Wrong — multi-line summary for content that fits on one line
/// <summary>
/// Defines an extraction handler for browser-based data.
/// Each channel implements its own logic.
/// </summary>
```

## Three gates, in order (REQUIRED)

A doc block passes three gates, and **length is the last one**. An over-long block is usually a symptom — it earns its length by failing gate 1 or 2, so fixing it at the bottom (wrapping) hides the real defect.

1. **Convention** — does the block obey its per-tag rule? `<summary>` = the tightest accurate sentence (`documentation/summary.md`); `<remarks>` = directive, not explanatory (`documentation/remarks.md`); `<param>` / `<returns>` say what the name doesn't. Check it against § *Comment anti-patterns* and § *Where a fact belongs* — a block carrying rationale, tech-facts, or a restatement of the member name fails here, and the cut usually solves the length by itself.
2. **Compaction** — verb over nominalization (`performs validation of` → `validates`), actor as subject, one term per concept, and drop the em-dash appositive that restates the clause before it.
3. **Line length** — 120 chars (`code-organization.md` § *Line length*). Only a block that survives gates 1 and 2 and still exceeds 120 may go multi-line, with the tags on their own lines.

- **Never wrap to satisfy gate 3 without running gates 1 and 2 first.** Wrapping is the last resort, not the fix.
- **Multi-line is the earned exception.** It says "every word here is load-bearing and there are more than 120 characters of them" — a claim most blocks cannot make.

```csharp
// ❌ Wrong — wrapped straight to gate 3; the appositive after the em-dash is the real defect
/// <summary>
/// Gets the storage table name for the code entity — the single source of truth for hand-written SQL.
/// </summary>

// ✅ Correct — gate 1 cut the appositive, and the sentence fits
/// <summary>Gets the storage table name for the code entity.</summary>
```

## Required tags per type-kind

`/// <summary>` is required on every public type and member.

| Type-kind | Required tags | Notes |
|---|---|---|
| Interface | `<summary>` | Interfaces define shape; describe the contract |
| Enum | `<summary>` (when/where used) | Plus `<summary>` on each value |
| Entity (record mapping to table) | `<summary>` (entity description) | Per-member `<summary>` |
| DTO | `<summary>` | Same as entity |
| Settings record | `<summary>` (appsettings section name) | Per-member `<summary>` |
| Service / Client / Repository | `<summary>` + `<remarks>` (flow / key behavior) | Methods get `<summary>` one-liner |
| Static class (constants, helpers, registries) | `<summary>` | Members may or may not need `<summary>` depending on visibility |
| Extension class | `<summary>` (purpose of the extensions) | Each extension method gets its own `<summary>` |
| Configuration class (EF `IEntityTypeConfiguration<T>`) | `<summary>` one-liner | No `<remarks>` |
| Handler (query/command) | `<summary>` = `Handles <see cref="{Q|C}"/>.` | Nothing else |
| Result type (Success/Failure containers) | `<summary>` on the abstract base and each variant | Members per the entity rule |

## Per-block conventions

Each XML doc block has its own rules — start here:

| Block | Convention | Covers |
|---|---|---|
| `<summary>` | [documentation/summary.md](documentation/summary.md) | Starter table (mandated first word per type-kind) + tone + property summaries. **Canonical summary reference** |
| `<remarks>` | [documentation/remarks.md](documentation/remarks.md) | Directive tone + multi-line numbered-flow exception |
| `<param>` | [documentation/params.md](documentation/params.md) | Compact noun-phrase per parameter |
| `<returns>` | [documentation/returns.md](documentation/returns.md) | Skipped by default; only when summary can't carry it |
| `<exception>` | [documentation/exceptions.md](documentation/exceptions.md) | Only exceptions the method throws itself |

## Cross-references

- `<see cref="X"/>` for inline references inside `<summary>` and `<remarks>` — the IDE resolves the link
- Never paste a type name as plain text when a `<see cref>` would link it

## Terminology

- **Collection** — use "collection" in `<summary>` when referring to any grouping type (`List<T>`, `T[]`, `Dictionary<K,V>`, etc.). Keeps docs stable when the implementation type changes.
- **The {entity}** — refer to the owning entity by name (`the channel`, `the listing`), not by C# type name in prose. The type name belongs in `<see cref>`.

## Inline comments (within method bodies)

Explain a non-trivial step with an **imperative one-liner** in step/order tone — present-tense verb, essentials only, one line. Skip when the code is self-evident.

```csharp
// Acquire the advisory lock so only one host migrates at a time.
await dialect.AcquireLockAsync(connection, ct);

// Fetch the applied set, then diff against the source.
var applied = await history.GetAppliedAsync(connection, ct);
```

- ✅ `// Skip the Dev folder — it holds unpromoted drafts.`
- ❌ `// This loop iterates over the directories and for each one it checks whether…` (multi-line / restates code)

## What NOT to document

- Internal types and members — XML doc is generated by `<GenerateDocumentationFile>` but warnings are suppressed; brief one-liners only if context isn't obvious
- Auto-generated code — skip
- `Program.cs` 3-liner — skip
- Test classes / methods — name carries the meaning
- **`<example>` tags** — don't use them; they restate the obvious and go stale.
- **Change / refactor narration** — `// moved from X`, `// now uses Y`, `// renamed`, `// was inline`. Git owns the diff; comment the code's *intent*, never its edit history.
- **Rationale / justification essays** — `// UserId is server-set, so this only validates the enum`, `// stays in the handler because it's a business rule`, `// keep ours per D1`. Ask *who is this note for?* — a reader can scan the code, which is the source of truth and greppable. A genuinely non-obvious *why* is **one** terse line (see Inline comments above), never a multi-line note re-explaining a design the code already encodes.

## Where a fact belongs (REQUIRED)

Most bad doc comments are true sentences filed in the wrong place. Route by **audience**, and the tag follows.

| The fact is | Audience | Goes in |
|---|---|---|
| What the member guarantees to a caller | consumer | `<summary>` |
| What a caller must do to use it correctly | consumer | `<remarks>`, imperative |
| Why the code is written this way; provenance of a format or a literal | maintainer | `//` next to the code it explains |
| A policy binding many types (naming, layering, "the single place we do X") | the team | a convention doc in `wow-two-ws/conventions/`, never a member's doc |

- **`<summary>` and `<remarks>` ship** — they land in the XML doc file and in IntelliSense. A maintainer note put there is broadcast to every consumer.
- **A member cannot know how it is used.** Any claim quantifying callers, uniqueness, or authority belongs one level up, in a convention.

## Comment anti-patterns (REQUIRED)

Named failure modes, checked at **gate 1**. The name is the review vocabulary — say "nonlocal information", not "this feels off". Names marked *(Clean Code)* are Robert C. Martin's, ch. 4.

### Nonlocal information *(Clean Code)*

A local comment asserting a system-wide fact. The member has no way to know it, so the claim rots the moment a second caller appears.

```csharp
// ❌ the member cannot know how many places read it
/// <summary>Gets the storage table name — the single source of truth for hand-written SQL.</summary>

// ✅ states what it offers; the "only place" policy lives in a convention
/// <summary>Gets the storage table name for the code entity.</summary>
```

### Too much information *(Clean Code)*

Spec provenance, standards history, format archaeology. Interesting to whoever wrote the encoder, irrelevant to whoever calls it.

```csharp
// ❌ RFC archaeology in a shipped doc
/// <remarks>The <c>mailto:</c> scheme is registered (RFC 6068), and what follows the <c>?</c> is not an HTTP query.</remarks>

// ✅ provenance is a maintainer fact — move it to a `//` beside the literal it explains, or drop it
```

### Over-specification

Documenting internals the contract does not guarantee. It binds the implementation: changing what the method wires now breaks its documentation.

```csharp
// ❌ enumerates what the call happens to register today
/// <summary>Adds persistence — registers the DbContext, the interceptors, the migrator, and the health check.</summary>

// ✅ the guarantee, not the wiring
/// <summary>Adds Postgres persistence to the container.</summary>
```

### Redundant comment *(Clean Code)*

Restates the member name, so it costs a line and pays nothing. `<summary>Gets the name.</summary>` on `Name`. Say what the name cannot: units, range, null meaning, or the moment it is set.

### Mandated comment *(Clean Code)*

A doc written because a rule demands one. Produces `<param name="ct">The cancellation token.</param>` across a codebase. If the parameter name says it, omit the tag.

### Inobvious connection *(Clean Code)*

A comment referring to something the reader cannot locate — "the sentinel", "as described above", "the usual flow". Either name the identifier with `<see cref="..."/>` or cut the sentence.

### Wrapped instead of cut

The process failure this catalogue came from: hitting the 120-char limit and wrapping to satisfy it, without running gates 1 and 2. A multi-line block is evidence the earlier gates were skipped until proven otherwise.

## Wrapper / package docs

For a library that ships reusable wrappers (the SDK pattern) — docs ride the wrapper's own cadence, not the underlying lib's.

- **every wrapper ships ≥1 xUnit test that doubles as runnable docs** — even trivial wrappers; the test proves the registration call works and is the "Storybook for backend" (demonstrates intended usage AND catches regressions)
- **`<Module>.standard.md`** — RFC 2119 (`MUST` / `SHOULD` / `MAY`) behaviour contract only, not API; survives API churn
- **`<Module>.spec.md`** — concrete API surface + usage snippets; tracks the code, updated when the wrapper API changes

---

## See also

- [models.md](models.md) — record style + general property rules
- [entities.md](../persistence/entities.md) — entity-specific doc rules
- [enums.md](../persistence/enums.md) — enum value documentation
- [services.md](../architecture/services.md) — service / client / factory naming
- [mediator.md](../messaging/mediator.md) — query/command/handler naming + docs
