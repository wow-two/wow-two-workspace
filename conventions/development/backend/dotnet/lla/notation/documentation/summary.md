# Summary

*Last updated: 2026-08-18*

> The `<summary>` block — the mandated first word per type-kind, plus tone. The canonical summary reference.

## Starter table [REQUIRED]

The first word of every `<summary>` is fixed by what the thing is.

- must take a **type's** starter from its component doc — [lla components](../../components/components.md)
  or [mla constructs](../../../mla/constructs/constructs.md).
- must take a **member's** starter from [constructs](../../constructs/constructs.md), which fixes them by role.
- must take a **construct's** starter from the same file, which rules on every C# form.
- must not reintroduce a table here — a starter belongs with the thing it starts.

---

## Summary — tightest accurate sentence

- One sentence. Start with the mandated starter word.
- For **capability interfaces** (entity traits with members), prefer `Defines a/an {noun} {that|with} {capability}`
  over `Defines the contract for {types} that {verb}…`
  - ✅ `Defines an entity with creation and update timestamps.`
  - ❌ `Defines the contract for entities that participate in timestamp auditing, CreatedAt and UpdatedAt.`
- For an **empty marker interface** (no members, tags a category not a shape), use `Defines the marker for {X}`
  - don't call it a "shape" — a marker has none; when the tagged concept is broad, define it inline with an em-dash
  - ✅ `Defines the marker for an entity — a type persisted to a data store.`
- **`the contract for` is banned after `Defines`** — the verb already declares one; name the capability directly
  - ✅ `Defines audit-field stamping on save.` ❌ `Defines the contract for stamping audit fields on save.`
- For **behavior interfaces** (handlers, stampers, service-shaped contracts), name the action as a noun phrase —
  `Defines JWT issuance for an admin session.`
- Don't spill member-level detail into the type summary — the members carry it.
- Drop filler: `the SDK convention`, `with a custom X type` (the type parameter is already visible in the signature).
- An **indexer** takes the property starter its accessors name; its summary states **what the key selects**
  - ✅ `Gets the routing rule at the given order.` ❌ `Gets the rule.`
  - the key is a value, so it also carries a `<param>` ([params](params.md))

---

## The falsifiability test [REQUIRED]

One question decides whether a `<summary>` is a definition or a description of today's arrangement:

> **Could this sentence go false without the type changing?**

If yes, it is not a definition — it records a circumstance, and a circumstance rots while the type stays put.

The companion rule: **a summary states the referent (what the thing *is*), never an affordance (what a consumer can
*do* with it)** — an affordance is a fact about callers, and callers change.

### The six shapes that fail it

- **Circumstance as definition** — `The domain model, wire DTO and stored shape in one.` → wire model splits off
- **Affordance as identity** — `Represents a phone number dialed on scan.` → a click-to-copy path ships
- **Implementation as identity** — `A contact card — encodes to a vCard 3.0 payload.` → the encoding changes
- **Inventory or count** — `The 10 content variants.` → an eleventh arrives
- **Relationship as identity** — `The counterpart of <see cref="CodeRuleSet"/>.` → the sibling is renamed or deleted
- **Status or lifecycle** — `The new replacement for the old resolver.` → "new" stops being true, immediately

### Applying it

- **Run it on every `<summary>` you write or touch.** It costs one question and it is the cheapest of the three gates.
- **A failing sentence is not always deleted** — ask where the fact belongs
  - `documentation.md` § *Where a fact belongs* routes it, often to `<remarks>` (a directive) or a `//`
- **It composes with the anti-pattern catalogue, not duplicates it** — the catalogue asks *does this belong here*,
  the test asks *is this a definition at all*; a sentence can pass one and fail the other
- **`<remarks>` is exempt** — a directive may describe the present, and is expected to stop being true
  - `Swap in MaxMind GeoLite2 to make country rules match.`

---

## Properties on entities + DTOs

- Start with `Gets` or `Gets or sets` — always state what the property holds, even if obvious from name
- **`{ get; init; }` takes `Gets`** — the setter closes after construction, so a consumer only ever gets
- **Applies to every C# model kind**, value objects included — never carry the frontend's bare noun phrase across
  - `The network name.` is the TypeScript style; C# has properties, and the accessor is what the starter names
- **A method producing a formatted payload gets `<inheritdoc />` + `<remarks>`, not a re-described `<summary>`**
  - a summary spelling the format out (`Builds the <c>WIFI:T:…;S:…;;</c> payload`) restates the code and goes stale
  - `<remarks>` carries only what the code doesn't show — escaping rules, an omitted segment, a spec quirk
- **Name the referent** ([documentation](documentation.md) § *Name the referent*) — only when the value is not the
  type's own: `Gets the order of the rule that matched the scan`, while `ChannelEntity.Slug` takes a bare
  `Gets or sets the kebab-case slug`
- PKs / FKs: `<summary>` like every other member — state what the key identifies
- **State what the value is** — not who sets it, when, or how; no "stamped by the interceptor", "populated by the DB"
  - an entity-trait contract describes the field; the population mechanism is the implementer's choice
  - ✅ `Gets or sets the timestamp when the entity was created.`
  - ❌ `Gets or sets the UTC timestamp when the entity was created. Stamped by the audit interceptor on insert.`
- **Don't restate type-implied facts** — `DateTimeOffset` is already a timestamp, so never "UTC timestamp";
  `IHasXmin` already implies Postgres, so never "Postgres xmin" on the member

---

## Fields

`const` · `static readonly` · `readonly` take **`Holds`**; a field whose state changes takes **`Keeps`**. What
splits a field that earns a summary from one that does not is the **role it plays**, never the access modifier:

- **a value** — a `const`, a compiled `Regex`, a timeout, a format string, a table name; the summary names the
  authority that fixes the choice ([constants](../../components/constants.md)).
- **state the type mutates** — a cache, an accumulator, a live-execution map; the summary names what it holds and
  the invariant that keeps it correct.
- **an injected collaborator** — `private readonly IClock _clock`, an `ILogger<T>`, a repository. **No summary** —
  its contract carries the doc, and restating it on the field is a Redundant comment by construction.

The test: **does the declaration leave a "why this?" unanswered?** A value and a state field do; a collaborator's
type name is the whole answer.

---

## Extract a format string when the literal has structure

A literal with fixed structural parts is a **contract shape**, not an implementation detail.

- must lift a payload / URI / template literal into a named `const` built with `string.Format` once it carries any
  constant segment beyond a single prefix
- the constant then shows the whole shape in one place, which interpolation scatters across the expression
- a bare prefix (`$"tel:{phone}"`) stays inline — there is no shape to see
- keep the segments that appear conditionally as their own constants, so the parent shape stays readable

---

## Expression body vs block

- **block body by default** — an expression body is for a single trivial delegation or a direct member return, and
  only on a component that permits one ([style](../style/style.md) § *The body*)
- ✅ `public override string Encode() => this.ToPayload();` — a value object, permitted
- ✅ `public string Slug => _slug;`
- ❌ the same delegation on a `Service` or `Repository` — block body from the start
- ❌ an expression body that wraps across lines, takes several parameters, or contains a conditional
- the tell: if the `=>` expression needs line breaks to read, it is a method body pretending to be an expression
