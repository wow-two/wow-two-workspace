# Documentation

*Last updated: 2026-07-06*

JSDoc on every public export. Mirrors the backend XML-doc starter table ([documentation](../../backend/dotnet/lla/notation/documentation/documentation.md)) so a type reads the same in C# and TS.

## Format

- must write a doc as a **one-liner** — `/** ... */` on a single line.
- may exceed one line **only** when every condition below holds; failing any one, collapse it.

### The multi-line exception

1. the entity is **exported** — an `@internal` never earns more than one line.
2. every extra line states a fact the **caller must act on**: a precondition, a failure mode, an ordering constraint, a disposal duty.
3. that fact is not derivable from the signature.
4. no line compares to another implementation, justifies the pattern, or explains *why this shape*.
5. **≤5 lines**; past that it is a doc page, not a comment.
6. no usage example — a snippet in a doc restates the obvious and goes stale with nothing to catch it. Put it in a test or a story, which the build runs.

**The test:** strike every line whose removal costs the caller nothing. One line surviving earns the block; none surviving collapses it.

Length is not the test. A 200-character comment restating what the code does fails on condition 2 while looking substantial.

```typescript
// ❌ long, and every line is what the code already says or how it used to be
/* Chained after the consumer's own click (attribute fallthrough puts theirs first) and skipped
   when they called `preventDefault()` — the original's `onClick?.(e); if (e.defaultPrevented) return`. */

// ✅ one line, the role
/* Runs after the consumer's handler; a prevented default skips it. */

// ✅ earns three lines — each is a caller obligation absent from the signature
/**
 * Opens the channel and returns it. Call `close()` before the page unloads.
 * Throws `DOMException` when the origin is cross-site.
 * Messages sent before `ready` resolves are dropped, not queued.
 */
```

```typescript
// ✅ Correct — compact one-liner
/** Defines the editable fields for the listing edit form. */
export interface EditableFields { }

// ✅ OK — multi-line for genuinely complex docs
/**
 * Maps a raw ListingDto from the API to a domain Listing.
 * Resolves enum string fields to TS enum values; returns `{ listing, error }` —
 * on failure, listing is null.
 */
export function mapListingDto(dto: ListingDto): MapListingResult { }

// ❌ Wrong — multi-line for a simple doc
/**
 * Defines the editable fields for the listing edit form.
 */
export interface EditableFields { }
```

## Verb starters (the table)

| Target | Verb | Example |
|---|---|---|
| Enum | `Defines` | `/** Defines the QR data-module body shape. */` |
| Enum member | `Refers to` | `/** Refers to a plain square module. */` — a member is a label, not its referent; `Represents` claims the entity *carries* what it names |
| Displays Record (`{Enum}Displays`) | `Maps` | `/** Maps each barcode format to its display. */` |
| Interface — shape/contract | `Defines` | `/** Defines the editable fields for the listing edit form. */` |
| Interface — data holder | `Represents` | `/** Represents a domain listing with resolved enum values. */` |
| Props interface | `Defines` | `/** Defines props for the author contact strip. */` |
| Prop member — value / input | `The …` | `/** The current foreground gradient, or null for a solid fill. */` |
| Prop member — callback / event | `Emits …` | `/** Emits the next gradient. */` (pure event → `Fires when …`) |
| Component fn | `Renders` | `/** Renders the author contact strip. */` |
| Utility fn | 3rd-person verb | `/** Resolves a raw API string to a TS enum value. */` |
| Hook | `Manages` | `/** Manages the supply listings fetch lifecycle. */` — leads with the state / behavior it owns |
| Context-accessor hook | `Provides access to` | `/** Provides access to auth state from AuthContext. */` |
| Extension object | `Extends` | `/** Extends `Person` for display formatting. */` — it bolts methods onto a type it does not own, so `Provides` overstates |
| Extension method | 3rd-person verb | `/** Extracts up to 2 uppercase initials. */` |
| Internal constant | `@internal {desc}` | `/** @internal Whitespace splitter. */` |

> **"Provides"** is reserved for implementation objects that supply behaviour of their own (services). An extension object supplies none — it bolts methods onto a type it does not own — so it takes **`Extends`**, matching the backend. Interfaces use **"Defines"** (shape) or **"Represents"** (data). A hook leads with **`Manages …`** — the state / behavior it owns — alongside the other keywords (`Renders` · `Emits` · `Defines` · `Maps` · `Defines props for`); `Manages` ≈ 90% of hooks, with `Provides access to` only for thin context unwrappers.
>
> **Prop members carry a direction-appropriate verb, not `Gets or sets`** — a React prop is unidirectional, and the get/set pair is split across a `value` prop and its `onChange` callback. Doc the inbound `value` as a noun phrase led by `The …`; doc the outbound callback with `Emits …` (or `Fires when …` for a pure event). Not `Gets or sets` (C#-property framing — a prop is neither), `Holds`/`Provides` (implies mutable storage the component doesn't own). The keyword scheme lives in [components](../presentation/components.md) § Members.

## Member-level docs

- **Props interfaces (backend-mirrored):** type-level JSDoc required; **member-level omitted** — the backend declares field semantics, so the FE doesn't restate them.
- **Props interfaces (pure UI — no backend counterpart):** member-level JSDoc **encouraged** — a one-liner per prop; there's no backend contract to lean on. (`Renders` on the component, `Defines props for …` on the interface.)
- **Domain interfaces / DTOs:** member docs optional; add `// ── Section ──` field groups instead (see [code-organization.md](code-organization.md)).

## Scope — what a doc is allowed to be about

A doc says **what the entity is**, and — when the name doesn't carry it — **what it is for**. Nothing else.

- must not say **why this shape rather than another** — pattern choice is a convention's job, not an entity's.
- **The test:** would this line read identically on every entity that follows the same rule? Then it belongs in the rule, not here.
- must not restate a rule from `conventions/` at a use site — a convention justified per use site puts the rulebook in every file, and the two drift the moment the rule changes.
- must not point at the convention either (`// see vue-sfc.md § …`) — a reader who needs it looks it up once; a pointer per site is the same noise, shorter.
- may keep a **one-clause** because when it changes what the reader does at that spot (`// second pass — the first leaves the ref unset`).

```typescript
// ❌ restates a convention (Pick-over-Omit is a rule; it reads the same on every such alias)
/** A `ButtonProps` member this replaces. Written through `Pick` rather than a bare key union:
 *  `Omit` accepts a key the type does not have, `Pick` does not. */
type ReplacedButtonProp = keyof Pick<ButtonProps, 'onError'>;

// ✅ says what it is; the rule lives in vue-sfc.md § Magic strings
/** @internal The `ButtonProps` handler this component replaces with its own emit. */
type ReplacedButtonProp = keyof Pick<ButtonProps, HandlerProp<typeof DomEvent.Error>>;
```

Why this gap stayed open: the rule below forbids *rationale*, and its examples are all **history** (migration notes, version drift). Explaining a convention-mandated pattern doesn't feel like history while writing it — it feels like helping a reader with a non-obvious API. The test above is what separates the two.

---

## Comments (non-JSDoc)

A `//` block / inline comment states a **role** in one line — never the rationale, history, or a design essay.

- must keep a file-top / block comment to **one line** naming what the code is or does — not why it came to be
- must not narrate migrations, drift-risks, version notes, or trade-offs in source (`// v0.7 — … the drift risk this rewire removes`) — that goes in the commit / PR / a doc
- must keep an inline / JSX comment a **short role label** (`{/* type picker */}`), not a sentence explaining the binding
- rationale / history / "why" → commit message or a doc, never the code file

## See also

- [documentation](../../backend/dotnet/lla/notation/documentation/documentation.md) — the C# starter table this mirrors
- [components](../presentation/components.md) · [enums](enums.md) · [extensions](extensions.md)
