# Documentation

*Last updated: 2026-08-15*

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

## Required tags per type-kind

`/// <summary>` is required on **every type and member, whatever its visibility**. A `private const` is not exempt: visibility says who may
call a thing, never whether its reason is obvious. Five exemptions, and no others — each one because the fact already lives somewhere better:

- **an implementation carrying `/// <inheritdoc/>`** — the contract's summary is the summary, and restating it puts one fact in two places
  that drift apart. Write `<inheritdoc/>`, never a paraphrase.
- **a test method** — no signature docs at all: no `<summary>`, no `<param>`, no `<remarks>`. `Create_WithBlankName_Returns400` is already
  the sentence, and a summary can only restate the name, which [documentation/summary.md](summary.md) § *Falsifiability* bans.
- **generated code** — `.Designer.cs`, scaffolded EF migrations, source-generator output. Never authored, so never swept.
- **an injected collaborator field** — `private readonly IClock _clock`. Same mechanism as `<inheritdoc/>`: the contract carries the doc, and
  a copy on the field drifts. Only a collaborator is exempt; a field holding a value or state is documented
  ([documentation/summary.md](summary.md) § *Fields — role decides, not visibility*).
- **a constructor that only assigns** — a DI primary constructor above all: no `<summary>`, and no `<param>` for its injected collaborators
  ([documentation/params.md](params.md) § *Every parameter, every time*). The type's own summary already states what it does, and
  each collaborator's contract carries its own doc. It earns both back the moment construction carries a **guarantee** — validation,
  normalization, a derived value, or a choice between overloads. That is the factory-shaped constructor, and it is documented in full.

| Type-kind | Required tags | Notes |
|---|---|---|
| Interface | `<summary>` | Interfaces define shape; describe the contract |
| Enum | `<summary>` (when/where used) | Plus `<summary>` on each value |
| Entity (record mapping to table) | `<summary>` (entity description) | Per-member `<summary>` |
| DTO | `<summary>` | Same as entity |
| Settings record | `<summary>` (appsettings section name) | Per-member `<summary>` |
| Service / Client / Broker / Repository | `<summary>` | Methods get a `<summary>` one-liner; `<remarks>` only when [remarks.md](remarks.md) § *What it carries* applies |
| Static class (constants, helpers, registries) | `<summary>` | Members per [documentation/summary.md](summary.md) § *Constants* |
| Extension class | `<summary>` (purpose of the extensions) | Each extension method gets its own `<summary>` |
| Configuration class (EF `IEntityTypeConfiguration<T>`) | `<summary>` one-liner | No `<remarks>` |
| Handler (query/command) | `<summary>` | Nothing else — starter in [documentation/summary.md](summary.md) |
| Result type (Success/Failure containers) | `<summary>` on the abstract base and each variant | Members per the entity rule |

## Per-block conventions

Each XML doc block has its own rules — start here:

| Block | Convention | Covers |
|---|---|---|
| `<summary>` | [documentation/summary.md](summary.md) | Starter table (mandated first word per type-kind), the falsifiability test, tone, property and constant summaries. **Canonical summary reference** |
| `<remarks>` | [documentation/remarks.md](remarks.md) | Never required; a directive, a spec reference, or genuine complexity — held to the same three gates |
| `<param>` | [documentation/params.md](params.md) | Compact noun-phrase per parameter |
| `<typeparam>` | [documentation/typeparams.md](typeparams.md) | Skipped for a conventional name; carried for a domain-meaningful one |
| `<returns>` | [documentation/returns.md](returns.md) | Required unless the return is `void` / `Task` / `ValueTask` |
| `<exception>` | [documentation/exceptions.md](exceptions.md) | Only exceptions the method throws itself |

## Three gates, in order [REQUIRED]

A doc block passes three gates, and **length is the last one**. An over-long block is usually a symptom — it earns its length by failing gate 1 or 2, so fixing it at the bottom (wrapping) hides the real defect.

1. **Convention** — does the block obey its per-tag rule? `<summary>` = the tightest accurate sentence, and it must pass the **falsifiability test** (`documentation/summary.md`); `<remarks>` = a directive, a spec reference, or genuine complexity, and never required (`documentation/remarks.md`); `<param>` / `<returns>` say what the name doesn't. Check it against § *Comment anti-patterns* and § *Where a fact belongs* — a block carrying rationale, tech-facts, or a restatement of the member name fails here, and the cut usually solves the length by itself.
2. **Compaction** — verb over nominalization (`performs validation of` → `validates`), actor as subject, one term per concept, and drop the em-dash appositive that restates the clause before it.
3. **Line length** — 120 chars (`code-organization.md` § *Line length*). Only a block that survives gates 1 and 2 and still exceeds 120 may go multi-line, with the tags on their own lines.

- **Multi-line is the earned exception.** It says "every word here is load-bearing and there are more than 120 characters of them" — a claim most blocks cannot make.
- **Cap it at 5 lines.** Past that it is a doc page, not a comment: move it to the module's `.standard.md` and leave the summary pointing at nothing. Clearing gates 1 and 2 buys length, not unlimited length.
- **Strike test.** Strike every line whose removal costs the caller nothing. One survivor earns the block; none collapses it. (The frontend's sibling rule — [../../frontend/code-style/documentation.md](documentation.md).)

```csharp
// ❌ Wrong — wrapped straight to gate 3; the appositive after the em-dash is the real defect
/// <summary>
/// Gets the storage table name for the code entity — the single source of truth for hand-written SQL.
/// </summary>

// ✅ Correct — gate 1 cut the appositive, and the sentence fits
/// <summary>Gets the storage table name for the code entity.</summary>
```

## Where a fact belongs [REQUIRED]

Most bad doc comments are true sentences filed in the wrong place. Route by **audience**, and the tag follows.

| The fact is | Audience | Goes in |
|---|---|---|
| What the member guarantees to a caller | consumer | `<summary>` |
| What a caller must do to use it correctly | consumer | `<remarks>`, imperative |
| Why the code is written this way; provenance of a format or a literal | maintainer | `//` next to the code it explains |
| A policy binding many types (naming, layering, "the single place we do X") | the team | a convention doc in `wow-two-ws/conventions/`, never a member's doc |

- **`<summary>` and `<remarks>` ship** — they land in the XML doc file and in IntelliSense. A maintainer note put there is broadcast to every consumer.
- **A member cannot know how it is used.** Any claim quantifying callers, uniqueness, or authority belongs one level up, in a convention.

## Declared fields only [REQUIRED]

A component doc names the doc fields its types carry, one sub-heading each. **A field the component does not declare is
forbidden on that component** — the omission is the ban, so no doc has to list what it excludes.

- must add a field only by declaring it in the component doc, with the rule it obeys there.
- must justify the addition in that sub-heading's first line — what the field carries that the declared ones cannot.
- must not read a missing field as an oversight; a component with no `<remarks>` sub-heading forbids `<remarks>`.

## Name the referent [REQUIRED]

A member name says *what* a value is, never *whose* it is. `Name` on a `CodeCreateCommand` could be the code's, its author's, or its owner's, and
the signature settles none of them. The referent is named exactly when it is **not** the enclosing type's own subject, so the presence of a domain
noun is a signal and its absence says *this belongs to the type you are reading*.

- must name the referent when the value belongs to something **other than** the enclosing type's subject — a related entity, an author, an owner, a target: `Gets the order of the rule that matched the scan.`
- must **omit** it when the value is the type's own — `ChannelEntity.Slug` takes `Gets or sets the kebab-case slug.`, never *of the channel*. Naming it there restates the declaration and drains the signal from every place the noun is load-bearing.
- must read the **subject**, not the type name — a `CodeDto` *is* the code, so `Name` omits; a `CodeCreateCommand` is a command *about* a code, so `Name` names the code.
- must apply in a `<summary>`, a `<param>`, and a `<returns>` alike.
- must not stretch it into who sets the value, when, or how — that is § *Where a fact belongs*.

The failure it names is an **unanchored value**: a doc that describes a value and leaves its owner to inference.

## Comment anti-patterns [REQUIRED]

Named failure modes, checked at **gate 1**. The name is the review vocabulary — say "nonlocal information", not "this feels off". Names marked *(Clean Code)* are Robert C. Martin's, ch. 4.

### Nonlocal information *(Clean Code)*

A local comment asserting a system-wide fact. The member has no way to know it, so the claim rots the moment a second caller appears.

```csharp
// ❌ the member cannot know how many places read it
/// <summary>Gets the storage table name — the single source of truth for hand-written SQL.</summary>

// ✅ states what it offers; the "only place" policy lives in a convention
/// <summary>Gets the storage table name for the code entity.</summary>
```

The same failure names a **delivery channel** a value object does not own. A value object states what it *holds*; how that reaches a device is the caller's concern, and usually more than one channel.

```csharp
// ❌ binds the type to one channel — a click-to-copy or share path makes it false
/// <summary>Represents a phone number dialed on scan.</summary>

// ✅ the value, and the capability it carries
/// <summary>Represents a telephone number to dial.</summary>
```

**Serialization is the same failure.** A value object's summary states what it holds, never how it encodes: the encoder picks the scheme, so a second encoder makes the claim false. The fact is local on `Encode()` or its extensions class, and nonlocal on the type.

```csharp
// ❌ nonlocal information — the encoder decides the scheme, not the value
/// <summary>Represents free-form text belonging to no scheme.</summary>

// ✅ the value
/// <summary>Represents free-form text.</summary>
```

### Too much information *(Clean Code)*

Spec provenance, standards history, format archaeology. Interesting to whoever wrote the encoder, irrelevant to whoever calls it.

```csharp
// ❌ archaeology — what the spec says, restated
/// <remarks>The <c>mailto:</c> scheme is registered (RFC 6068), and what follows the <c>?</c> is not an HTTP query.</remarks>

// ✅ name the spec, do not restate it
/// <remarks>Follows RFC 6068.</remarks>

// ✅ provenance is a maintainer fact — move it to a `//` beside the literal it explains, or drop it
```

**Conformance is not provenance.** *"This output conforms to RFC 6068"* is a contract the caller can rely on, so it ships — as a **spec reference in `<remarks>`** ([documentation/remarks.md](remarks.md) § *What it carries*), naming the spec and restating none of it. The `<summary>` keeps its purpose shape and does not absorb the citation. *"The format was never standardised; here is why the literals look like this"* is provenance, and it goes in a `//`.

```csharp
// ❌ restates the spec, and repeats the scheme RFC 6068 already names
/// <summary>Extends <see cref="EmailContentValueObject"/> to the RFC 6068 <c>mailto:</c> payload.</summary>

// ✅ purpose in the summary, the spec named once in <remarks>
/// <summary>Extends <see cref="EmailContentValueObject"/> for payload encoding.</summary>
/// <remarks>Follows RFC 6068.</remarks>
```

### Over-specification

Documenting internals the contract does not guarantee. It binds the implementation: changing what the method wires now breaks its documentation.

```csharp
// ❌ enumerates what the call happens to register today
/// <summary>Adds persistence — registers the DbContext, the interceptors, the migrator, and the health check.</summary>

// ✅ the guarantee, not the wiring
/// <summary>Adds Postgres persistence to the container.</summary>
```

**Cutting a failing block is not the same as relocating its sentence.** A fact that fails gate 1 in `<remarks>` usually fails in `<summary>` too — check it against this section again after the move, or the defect just changes tag.

### Redundant comment *(Clean Code)*

Restates the member name, so it costs a line and pays nothing.

```csharp
// ❌ the predicate is empty — the name already said "slug"
/// <summary>Gets or sets the slug.</summary>
public required string Slug { get; set; }

// ✅ the starter stays; the predicate carries the entity and the shape
/// <summary>Gets or sets the kebab-case slug of the channel.</summary>
```

The defect is the empty predicate, never the starter — a property summary must keep its `Gets` / `Gets or sets` ([summary.md](summary.md) § *Properties*). Say what the name cannot: the parent entity, units, range, or what null means. Not who sets it, when, or how.

### Mandated comment *(Clean Code)*

A doc written because a rule demands one, carrying nothing the declaration lacks — an empty `<summary>` on a self-evident private method, a `<returns>` restating the return type. **`<param>` is exempt**: [documentation/params.md](params.md) requires one per parameter on purpose, because a partial set reads as an omission.

### Inobvious connection *(Clean Code)*

A comment referring to something the reader cannot locate — "the sentinel", "as described above", "the usual flow". Either name the identifier with `<see cref="..."/>` or cut the sentence.

### Circumstance as definition

A `<summary>` describing today's arrangement rather than what the type is. It fails the **falsifiability test** in [documentation/summary.md](summary.md), which names the shapes it takes.

### Wrapped instead of cut

The process failure this catalogue came from: hitting the 120-char limit and wrapping to satisfy it, without running gates 1 and 2. A multi-line block is evidence the earlier gates were skipped until proven otherwise.

## Cross-references [REQUIRED]

A `<see cref>` is a **navigation aid**, not decoration. It earns its place when the reader has to go read the referenced type to use this one correctly. It costs 20–60 characters of the 120-char budget, so a decorative one displaces a real fact.

**Use a cref when the type is off-screen and load-bearing:**

- a sibling to prefer or a replacement — `For Postgres, prefer <see cref="IHasXmin"/>.`
- a registry, options bag, or contract the reader must keep in lockstep — `Keep <see cref="Subtypes"/> in lockstep with the frontend union.`
- the type a member delegates to, when the delegation is the point

**Do not use a cref when it links to something already in view:**

| Case | Why not |
|---|---|
| A type in this member's own signature | `Serialize(IReadOnlyList<CodeRuleValueObject>)` — the parameter already shows it |
| The declaring type, inside its own members | The file is the context |
| A type named only as a noun in prose | The sentence works without following the link; drop the tag, keep the word |
| Every type mentioned, out of completeness | That is the mandated-comment anti-pattern wearing a link |

**Pick the right tag:**

- `<see cref="X"/>` — a type or member that exists. The compiler checks it (`CS1574` on a broken link), so a cref is a rename-safe reference.
- `<c>x</c>` — a literal that is **not** a type: a wire token, a column name, a header, a JSON key, a shell value. `<c>content_json</c>`, `<c>Stripe-Signature</c>`, `<c>"vCard"</c>`.
- `<paramref name="x"/>` / `<typeparamref name="T"/>` — always correct for a parameter or type parameter; they bind to the signature rather than navigating away.

Never write a type name as bare prose when a cref would link it **and** the link earns its place by the rules above. When it does not, use the plain noun — *"the rule set"*, not `<see cref="CodeRuleSet"/>`.

## Terminology

- **Collection** — use "collection" in `<summary>` when referring to any grouping type (`List<T>`, `T[]`, `Dictionary<K,V>`, etc.). Keeps docs stable when the implementation type changes.
- **The {entity}** — refer to the owning entity by name (`the channel`, `the listing`), not by C# type name in prose. The type name belongs in `<see cref>`.

## Inline comments (within method bodies)

Explain a non-trivial step with an **imperative one-liner** in step/order tone — present-tense verb, essentials only, one line. Skip when the code is self-evident.

**One line, no exception.** A `//` or `/* */` inside a body has no earned-multi-line clause: the 5-line cap above governs `<summary>` / `<remarks>`, which ship to consumers, while an inline comment is a maintainer's marginal note. A note needing a second line is a note that belongs in the commit, the tracking issue, or the module's `.standard.md`.

```csharp
// Acquire the advisory lock so only one host migrates at a time.
await dialect.AcquireLockAsync(connection, ct);

// Fetch the applied set, then diff against the source.
var applied = await history.GetAppliedAsync(connection, ct);
```

- ❌ `// This loop iterates over the directories and for each one it checks whether…` (multi-line / restates code)

## What NOT to document

- Internal types and members — XML doc is generated by `<GenerateDocumentationFile>` but warnings are suppressed; brief one-liners only if context isn't obvious
- Auto-generated code — skip
- `Program.cs` 3-liner — skip
- Test classes / methods — name carries the meaning
- **`<example>` tags** — don't use them; they restate the obvious and go stale.
- **Change / refactor narration** — `// moved from X`, `// now uses Y`, `// renamed`, `// was inline`. Git owns the diff; comment the code's *intent*, never its edit history.
- **Rationale / justification essays** — `// UserId is server-set, so this only validates the enum`, `// stays in the handler because it's a business rule`, `// keep ours per D1`. Ask *who is this note for?* — a reader can scan the code, which is the source of truth and greppable. A genuinely non-obvious *why* is **one** terse line (see Inline comments above), never a multi-line note re-explaining a design the code already encodes.

## Wrapper / package docs

For a library that ships reusable wrappers (the SDK pattern) — docs ride the wrapper's own cadence, not the underlying lib's.

- **every wrapper ships ≥1 xUnit test that doubles as runnable docs** — even trivial wrappers; the test proves the registration call works and is the "Storybook for backend" (demonstrates intended usage AND catches regressions)
- **`<Module>.standard.md`** — RFC 2119 (`MUST` / `SHOULD` / `MAY`) behaviour contract only, not API; survives API churn
- **`<Module>.spec.md`** — concrete API surface + usage snippets; tracks the code, updated when the wrapper API changes

---

## See also

- [models.md](../../constructs/records.md) — record style + general property rules
- [entities.md](../../../mla/components/data/entity.md) — entity-specific doc rules
- [enums.md](../../components/enums.md) — enum value documentation
- [services.md](../../../mla/components/behavior/service.md) — service / client / factory naming
- [mediator.md](../../../mla/domains/messaging/mediator.md) — query/command/handler naming + docs
