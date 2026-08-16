# Summary

*Last updated: 2026-08-16*

> The `<summary>` block — its mandated first word per type-kind (the starter table) + tone. The canonical summary reference; every convention links here.

## Starter table [REQUIRED]

The first word of every `<summary>` is fixed by what the thing is, and this file no longer holds the roster.

- must take a **type's** starter from its component doc — [`lla/components/`](../../components/components.md) or [`mla/components/`](../../../mla/components/components.md).
- must take a **member's** starter from [`constructs.md`](../../constructs/constructs.md), whose data and behavior sections fix them by role.
- must take a **construct's** starter from the same file, which rules on every C# form.
- must not reintroduce a table here — a starter belongs with the thing it starts, and one roster is what made this file grow.

## Summary — tightest accurate sentence

- One sentence. Start with the mandated starter word.
- For **capability interfaces** (entity traits with members), prefer `Defines a/an {noun} {that|with} {capability}` over `Defines the contract for {types} that {verb}…`. Shorter, same meaning.
  - ✅ `Defines an entity with creation and update timestamps.`
  - ❌ `Defines the contract for entities that participate in timestamp auditing — CreatedAt populated on insert, UpdatedAt on every update.`
- For an **empty marker interface** (no members — it tags a category rather than imposing a shape), use `Defines the marker for {X}`. Don't call it a "shape" — a marker has none. When the tagged concept is broad, define it inline with an em-dash.
  - ✅ `Defines the marker for an entity — a type persisted to a data store.`
- **`the contract for` is banned after `Defines`.** The verb already says a contract is being declared, so the phrase pays characters for meaning the reader has. Name the capability directly: `Defines audit-field stamping on save.`, never `Defines the contract for stamping audit fields on save.`
- For **behavior interfaces** (handlers, stampers, service-shaped contracts), name the action as a noun phrase — `Defines JWT issuance for an admin session.`
- Don't spill member-level detail into the type summary — the members carry it.
- Drop filler: `the SDK convention`, `with a custom X type` (the type parameter is already visible in the signature).
- An **indexer** takes the property starter its accessors name, and its summary states **what the key selects** — `Gets the routing rule at the given order.`, never `Gets the rule.` The key is a value, so it also carries a `<param>` ([params](params.md)).

## The falsifiability test [REQUIRED]

One question decides whether a `<summary>` is a definition or a description of today's arrangement:

> **Could this sentence go false without the type changing?**

If yes, it is not a definition. It records a circumstance, and a circumstance rots while the type stays put — nobody re-reads the doc when the circumstance changes, so the summary quietly becomes a lie.

The companion rule: **a summary states the referent (what the thing *is*), never an affordance (what a consumer can *do* with it).** An affordance is a fact about callers, and callers change.

### The six shapes that fail it

| Shape | Example | Goes false when |
|---|---|---|
| **Circumstance as definition** | `The domain model, wire DTO and stored shape in one.` | the wire model splits off |
| **Affordance as identity** | `Represents a phone number dialed on scan.` | a click-to-copy path ships |
| **Implementation as identity** | `A contact card — encodes to a vCard 3.0 payload.` | the encoding moves or changes version |
| **Inventory or count** | `The 10 content variants.` | an eleventh arrives |
| **Relationship as identity** | `The counterpart of <see cref="CodeRuleSet"/>.` | that sibling is renamed or deleted |
| **Status or lifecycle** | `The new replacement for the old resolver.` | "new" stops being true, which is immediately |

### Applying it

- **Run it on every `<summary>` you write or touch.** It costs one question and it is the cheapest of the three gates.
- **A failing sentence is not always deleted.** Ask where the fact belongs — `documentation.md` § *Where a fact belongs* routes it, and often the answer is `<remarks>` (a directive to the consumer) or a `//` (a maintainer's note).
- **It composes with the anti-pattern catalogue rather than duplicating it.** The catalogue asks *does this belong here*; the falsifiability test asks *is this a definition at all*. A sentence can pass one and fail the other.
- **`<remarks>` is exempt.** A directive is allowed to describe the present — `Swap in MaxMind GeoLite2 to make country rules match.` is true today and expected to stop being true.

## Extension classes

Moved — see [extensions](../../components/extensions.md).


## Properties on entities + DTOs

- Start with `Gets` or `Gets or sets` — always state what the property holds, even if obvious from name
- **`{ get; init; }` takes `Gets`** — the setter closes after construction, so a consumer only ever gets
- **Applies to every C# model kind**, value objects included. A bare noun phrase (`The network name.`) is the TypeScript style — TS has fields, C# has properties, and the accessor is what the starter names. Don't carry the frontend's phrasing across
- **A method that produces a formatted payload gets `<inheritdoc />` + `<remarks>`, not a re-described `<summary>`.** The format string lives in the code; a summary spelling it out (`Builds the <c>WIFI:T:…;S:…;;</c> payload`) restates it and goes stale. `<remarks>` carries only what the code doesn't show — escaping rules, an omitted segment, a spec quirk
- **Name the referent** ([documentation](documentation.md) § *Name the referent*) — name it only when the value is not the type's own: `Gets the order of the rule that matched the scan`, but `ChannelEntity.Slug` takes a bare `Gets or sets the kebab-case slug`
- PKs / FKs: `<summary>` like every other member — state what the key identifies
- **State what the value is — not who sets it, when, or how.** No "stamped by the interceptor", "populated by the DB", "set at construction". An entity-trait contract describes the field; the population mechanism (interceptor, trigger, app code) is the implementer's choice and must not leak in.
  - ✅ `Gets or sets the timestamp when the entity was created.`
  - ❌ `Gets or sets the UTC timestamp when the entity was created. Stamped by the audit interceptor on insert; preserved on every subsequent update.`
- **Don't restate type-implied facts** — `DateTimeOffset` is already a timestamp (don't write "UTC timestamp"); an interface named `IHasXmin` already implies Postgres (don't repeat "Postgres xmin" on the member)

## Fields — role decides, not visibility

`const` · `static readonly` · `readonly` · a plain instance field all take **`Holds`**, at every visibility. What splits a field that earns a
summary from one that does not is the **role it plays**, never the access modifier:

- **a value** — a `const`, a compiled `Regex`, a timeout, a format string, a table name. Someone chose it, so the summary names the authority
  that fixes the choice (§ *Constants* below).
- **state the type mutates** — a cache, an accumulator, a live-execution map. The summary names what it holds and the invariant that keeps it
  correct; the type alone shows neither.
- **an injected collaborator** — `private readonly IClock _clock`, an `ILogger<T>`, a repository. **No summary.** Its contract carries the doc,
  and restating it on the field duplicates a fact that then drifts — the same mechanism that makes `<inheritdoc/>` an exemption
  ([documentation](documentation.md) § *Required tags per type-kind*). A summary here is a Redundant comment by construction.

The test: **does the declaration leave a "why this?" unanswered?** A value and a state field do; a collaborator's type name is the whole answer.

## Constants

Moved — a `Constants` class is an LLA role, so its doc rules live with it ([constants](../../components/constants.md)).


## Extract a format string when the literal has structure

A literal with fixed structural parts is a **contract shape**, not an implementation detail.

- must lift a payload / URI / template literal into a named `const` and build it with `string.Format` once it carries any constant segment beyond a single prefix
- the constant then shows the whole shape in one place, which interpolation scatters across the expression
- a bare prefix (`$"tel:{phone}"`) stays inline — there is no shape to see
- keep the segments that appear conditionally as their own constants, so the parent shape stays readable

## Expression body vs block

- **block body by default.** An expression body is for a single trivial delegation or a direct member return, **and only on a component that permits one** — the list is in [members.md](../../constructs/constructs.md) § *The body*
- ✅ `public override string Encode() => this.ToPayload();` — a value object, permitted
- ✅ `public string Slug => _slug;`
- ❌ the same delegation on a `Service` or `Repository` — block body from the start
- ❌ an expression body whose expression wraps across lines, takes several parameters, or contains a conditional — that wants a block
- the tell: if the `=>` expression needs line breaks to read, it is a method body pretending to be an expression
