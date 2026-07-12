# Documentation

*Last updated: 2026-07-06*

JSDoc on every public export. Mirrors the backend XML-doc starter table ([../backend/documentation.md](../../backend/code-style/documentation.md)) so a type reads the same in C# and TS.

## Format

- **One-liner by default** — `/** ... */` on a single line.
- **Multi-line only** when documenting parameters or complex behavior (3+ lines of substance).

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
| Enum member | `Refers to` | `/** Refers to a plain square module. */` |
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
| Extension object | `Provides` | `/** Provides extensions for person formatting. */` |
| Extension method | 3rd-person verb | `/** Extracts up to 2 uppercase initials. */` |
| Internal constant | `@internal {desc}` | `/** @internal Whitespace splitter. */` |

> **"Provides"** is reserved for implementation objects (extensions, services). Interfaces use **"Defines"** (shape) or **"Represents"** (data). A hook leads with **`Manages …`** — the state / behavior it owns — alongside the other keywords (`Renders` · `Emits` · `Defines` · `Maps` · `Defines props for`); `Manages` ≈ 90% of hooks, with `Provides access to` only for thin context unwrappers.
>
> **Prop members carry a direction-appropriate verb, not `Gets or sets`** — a React prop is unidirectional, and the get/set pair is split across a `value` prop and its `onChange` callback. Doc the inbound `value` as a noun phrase led by `The …`; doc the outbound callback with `Emits …` (or `Fires when …` for a pure event). Not `Gets or sets` (C#-property framing — a prop is neither), `Holds`/`Provides` (implies mutable storage the component doesn't own). The keyword scheme lives in [components.md](../presentation/components.md) § Members.

## Member-level docs

- **Props interfaces (backend-mirrored):** type-level JSDoc required; **member-level omitted** — the backend declares field semantics, so the FE doesn't restate them.
- **Props interfaces (pure UI — no backend counterpart):** member-level JSDoc **encouraged** — a one-liner per prop; there's no backend contract to lean on. (`Renders` on the component, `Defines props for …` on the interface.)
- **Domain interfaces / DTOs:** member docs optional; add `// ── Section ──` field groups instead (see [code-organization.md](code-organization.md)).

## Comments (non-JSDoc)

A `//` block / inline comment states a **role** in one line — never the rationale, history, or a design essay.

- must keep a file-top / block comment to **one line** naming what the code is or does — not why it came to be
- must not narrate migrations, drift-risks, version notes, or trade-offs in source (`// v0.7 — … the drift risk this rewire removes`) — that goes in the commit / PR / a doc
- must keep an inline / JSX comment a **short role label** (`{/* type picker */}`), not a sentence explaining the binding
- rationale / history / "why" → commit message or a doc, never the code file

## See also

- [../backend/documentation.md](../../backend/code-style/documentation.md) — the C# starter table this mirrors
- [components.md](../presentation/components.md) · [enums.md](enums.md) · [extensions.md](extensions.md)
