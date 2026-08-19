# Anti-patterns

*Last updated: 2026-08-19*

> The named ways a doc or a comment fails — one name per failure, and the names are the review vocabulary.
> Purpose — a review says "nonlocal information", not "this feels off", and the writer knows what to cut.
> Use case — check a doc against this list before it ships; names marked *(Clean Code)* are Martin's, ch. 4.

## Nonlocal information *(Clean Code)*

A local doc asserting a system-wide fact — the claim rots the moment a second caller or channel appears.

- must state what the entity offers, never how many places read it.
  - ❌ `/** The storage key — the single source of truth for every reader. */`
  - ✅ `/** The storage key for the draft code. */`
- must state what a value holds, never the channel carrying it or the scheme encoding it.
  - a second encoder or a copy-to-clipboard path makes the claim false.
  - ❌ `/** The phone number dialled on tap. */` → ✅ `/** The telephone number to dial. */`
- must keep a `conventions/` rule out of a use site ([documentation](documentation.md) § *Scope*).

```typescript
// ❌ carries a `conventions/` rule into the file — it reads the same on every such alias
/** A `ButtonProps` member this replaces. Written through `Pick` rather than a bare key union:
 *  `Omit` accepts a key the type does not have, `Pick` does not. */

// ✅ says what it is; the rule lives in its convention
/** @internal The `ButtonProps` handler this component replaces with its own emit. */
type ReplacedButtonProp = keyof Pick<ButtonProps, HandlerProp<typeof DomEvent.Error>>;
```

---

## Too much information *(Clean Code)*

Spec provenance, standards history, format archaeology — none of it reaches whoever calls the entity.

- must name a spec, never restate it — `Follows RFC 6068.` is the whole reference.
- must move provenance — *why the literals look this way* — to a `//` beside the literal, or drop it.
- conformance is a contract and ships; provenance is a maintainer fact and stays out of the doc.

---

## Over-specification

Documenting internals the contract does not guarantee — changing what the function wires breaks its doc.

- must state the guarantee, never the wiring.
  - ❌ `/** Manages the listings fetch — mounts the query, retries twice, writes the cache key. */`
  - ✅ `/** Manages the supply listings fetch lifecycle. */`
- must re-check a fact after moving it — one failing here usually fails in its new block too.

---

## Redundant comment *(Clean Code)*

Restates the name, so it costs a line and pays nothing.

- must say what the name cannot — the shape, the units, the range, what `null` means.
  - ❌ `/** The slug. */`
  - ✅ `/** The kebab-case slug, unique per workspace. */`
- must keep the starter verb — the defect is the empty predicate, never the opener
  ([documentation](documentation.md) § *Verb starters*).
- must not answer it by naming who writes the value, when, or how.

---

## Mandated comment *(Clean Code)*

A doc written because a rule demands one, carrying nothing the declaration lacks.

- must not write one where the declaration is the whole answer.
- a **pure-UI props member is exempt** — [documentation](documentation.md) § *Member docs* requires one per
  member, because a partial set reads as an omission.

---

## Inobvious connection *(Clean Code)*

A doc pointing at something the reader cannot locate — "the sentinel", "as described above", "the usual flow".

- must name the identifier with `{@link}`, or cut the sentence.
- must not lean on the link for correctness — nothing checks it ([falsifiability](falsifiability.md)).

---

## Circumstance as definition

A doc describing today's arrangement rather than what the entity is.

- must run [the falsifiability test](falsifiability.md), which names the six shapes this takes.

---

## Wrapped instead of cut

Hitting the one-line default and wrapping to fit, without re-checking what the extra lines carry.

- must treat a multi-line block as evidence the conditions were skipped, until each line is checked against
  the multi-line exception ([documentation](documentation.md) § *Format*).

---

## Neighbours

- [documentation](documentation.md) — the format, the verbs, and what a doc may claim
- [falsifiability](falsifiability.md) — the test that runs alongside this list
