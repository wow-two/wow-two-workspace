# Falsifiability

*Last updated: 2026-08-19*

> The one test separating a doc that defines the entity from a doc that records today's arrangement.
> Purpose — an arrangement rots while the entity stays put, and no compiler catches the sentence.
> Use case — run it on every doc block written or touched, ahead of the anti-pattern catalogue.

## The test [REQUIRED]

> **Could this sentence go false without the type changing?**

- must read a yes as a failure — the sentence records a circumstance, not a definition.
- must state the **referent** — what the thing *is*, never an **affordance**, what a consumer can *do* with it.
- an affordance is a fact about callers, and callers change.

---

## The six failing shapes

| Shape | Reads as | Goes false when |
|---|---|---|
| Circumstance as definition | `/** The domain model, wire DTO and form shape in one. */` | the form shape splits off |
| Affordance as identity | `/** The phone number dialled on tap. */` | a copy-to-clipboard path ships |
| Implementation as identity | `/** A contact card, encoded as a vCard 3.0 payload. */` | the encoder changes |
| Inventory or count | `/** The 10 content variants. */` | an eleventh arrives |
| Relationship as identity | `/** The counterpart of {@link CodeRuleSet}. */` | the sibling is renamed |
| Status or lifecycle | `/** The new replacement for the old resolver. */` | `new` stops being true |

---

## TypeScript riders

- must route an **inventory** sentence to [the redundancy rule](anti-patterns.md) when a literal union or an
  `as const` tuple already fixes the count.
  - the sentence cannot then go false without the type changing — it fails as a restatement instead.
- must hold a **relationship** sentence to this rule harder than C# does, not softer.
  - a `{@link}` is unchecked here, where a C# `<see cref>` fails the build; a stale link rots in silence.

---

## Exemption

- may describe the present in a line admitted by the multi-line exception's condition 2
  ([documentation](documentation.md) § *Format*) — a caller obligation is a directive, and directives expire.
- must not stretch the exemption onto the opening line — the entity's own sentence always takes the test.

---

## Applying it

- must not delete a failing sentence reflexively — ask where the fact belongs, then move it.
  - a maintainer fact goes to a `//` beside the code; a policy binding many entities goes to a convention.
- must compose it with [the anti-pattern catalogue](anti-patterns.md), never duplicate it.
  - the catalogue asks *does this fact belong here*; this test asks *is this a definition at all*.
  - a sentence can pass one and fail the other.

---

## Neighbours

- [documentation](documentation.md) — the format, and the verb that opens the sentence
- [anti-patterns](anti-patterns.md) — the named failures checked alongside this test
