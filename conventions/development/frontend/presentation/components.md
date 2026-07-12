# Components

*Last updated: 2026-07-09*

> How to shape a component and its props — one component per folder, a `readonly` props `interface`, and the doc keywords that name each part. A prop is **not** a C# property, so it never reads `Gets or sets`.

**Flow:** `kind → folder → doc → props interface → prop members → styling → JSX → use`

---

## 1. Kind

The term fixes what the component owns and where it sits.

| Term | Owns | Example |
|---|---|---|
| **Page** | the whole viewport — outermost shell; decides sidebar / topbar / none | `SignInPage` · `MainLayout` |
| **View** | the content area inside a page — swaps on nav, layout persists | `InboxView` · `OutreachView` |
| **Modal** | an overlay above the current page+view — backdrop, floats | confirm dialog · detail preview |
| **Form** | a reusable input component — pluggable into any page / view / modal | `SignInForm` · `FilterForm` |

- must classify by **what it owns**, not by where it happens to render.

---

## 2. Folder

- **SDK library (`@wow-two-beta/ui`) — must** give every component its **own folder**: `camelCase` folder, `PascalCase` main file, an `index.ts` barrel, co-located `*.stories.tsx` (+ `*.variants.ts` when needed). Never flatten a `.tsx` next to sibling folders.
- **App (product frontend) — may** keep components as **flat files grouped by concern** (`core/design/FillControls.tsx` · `core/shape/ShapeControls.tsx`). No per-component folder or barrel; the **concern** folder's `index.ts` is the public API.
- must keep sub-components **internal** either way — a non-exported sibling (`GradientControls.tsx`) or a nested fn; only the barrel's re-exports are public.
- applies to **components only** — not views, pages, hooks, or lib files.

```
components/
  phoneChip/
    PhoneChip.tsx
    index.ts                 // export { PhoneChip } from "./PhoneChip.js"
  listingDetailModal/
    ListingDetailModal.tsx
    ListingDetailHeader.tsx  // internal sub-component
    index.ts                 // only exports ListingDetailModal
```

- must order the component file: imports → types / interfaces → constants → helpers (pure, no hooks) → component fn → sub-components (only if small + tightly coupled). Import order per [code-organization.md](../code-style/code-organization.md).

---

## 3. Doc

- must JSDoc the component with a **one-line** `/** … */` starting **`Renders …`** ([documentation.md](../code-style/documentation.md)) — never a multi-line block on a component.
- must JSDoc the props interface with a one-liner starting **`Defines props for …`**.

```tsx
/** Renders the author contact strip. */
export function AuthorContact(props: AuthorContactProps) { … }
```

---

## 4. Props interface

- must declare props as an **`interface`** (`type` only for a union), one file, named `{Component}Props`.
- must mark **every member `readonly`**; an array prop is **`ReadonlyArray<T>`** (blocks `.push()` / `.splice()`). `readonly` is the mutation guard — and it **flows through a destructured binding**, so it holds regardless of access style.
- must **destructure** in the parameter (`{ foreground, size = 16 }`) — inline defaults stay clean, `readonly` carries through, and a destructured `const` **keeps type-narrowing across closures** (a `props.x` member read re-widens inside a nested callback → forces `!` / captures).
  - *Evaluated & reverted (2026-07): no-`props`-destructure (`props.x` + `withDefaults` / `splitProps`) for discriminated-union narrowing + co-located defaults — the closure re-widening cost above outweighed the gain. Revisit if TS ships control-flow narrowing for immutable member access.*

```tsx
/** Defines props for the author contact strip. */
interface AuthorContactProps {
  readonly authorName: string;
  readonly phones: ReadonlyArray<string>;
}

export function AuthorContact({ authorName, phones }: AuthorContactProps) {
  phones[0];        // read + index
  phones.push("x"); // ❌ ReadonlyArray — readonly flows through the destructure
}
```

---

## 5. Prop members

Each member gets a one-line JSDoc whose verb matches the prop's **direction** — a prop is unidirectional, and the get/set is split across a `value` prop and its `onChange` callback, so one direction-appropriate verb per member is right ([documentation.md](../code-style/documentation.md) verb table).

- must doc a **value / input** prop as a noun phrase led by **`The …`**.
- must doc a **callback / event** prop with **`Emits …`** — the value it hands back; a *pure* event with no payload uses **`Fires when …`**.
- must **not** write `Gets or sets` (a prop is not a C# property), nor `Holds` / `Provides` (both imply mutable storage the component doesn't own).
- must leave **one blank line between members** — a props interface is a model, so its documented members are blank-line-separated per [models.md](../code-style/models.md); the docs read as separate units, not a wall.

| Prop shape | Keyword | Example |
|---|---|---|
| value / input | `The …` | `/** The current foreground gradient, or null for a solid fill. */` |
| callback (payload) | `Emits …` | `/** Emits the next gradient. */` |
| event (no payload) | `Fires when …` | `/** Fires when the user dismisses the sheet. */` |

**Required vs. optional per prop origin:**

- **pure-UI prop** (no backend counterpart) → member doc **required**; there's no backend contract to lean on.
- **backend-mirrored DTO prop** → member doc **omitted** — the backend declares the field semantics; the FE must not restate them ([documentation.md](../code-style/documentation.md) § Member-level docs).

```tsx
/** Defines props for the fill controls. */
interface FillControlsProps {
  /** The current foreground gradient, or null for a solid fill. */
  readonly gradient: Gradient | null;

  /** Emits the next gradient, or null to fall back to the solid fill. */
  readonly onGradientChange: (gradient: Gradient | null) => void;
}

/** Renders the foreground fill controls. */
export function FillControls(props: FillControlsProps) { … }
```

---

## 6. Styling

- must use Tailwind utilities only; conditional classes via `cn()` ([styling.md](styling.md)).
- must define a multi-variant component's class map with **`tailwind-variants`** in a co-located `*.variants.ts` / `*Styles.ts` — never inline a large conditional class string.
- should reach for a **`@wow-two-beta/ui`** component (`Button`, `Card`, `Badge`, `Heading`, `Text`, `Alert`, `Spinner`, `EmptyState`, `TextInput`, …) before hand-rolling; missing one → build locally, then migrate upstream **only if it clears the [SDK-extraction threshold](../../sdk-extraction.md)** (carries logic + ecosystem-worth). A pure DRY / layout wrapper stays inline (duplicate it); an **atom that carries logic is never product-local**.

---

## 7. JSX attributes

- must put **one attribute per line** once an element has **3+ attributes** *and* the single-line form passes the **120-char** wrap; else keep it inline. Peer siblings share one shape — don't mix inline + wrapped.
- set Prettier `printWidth: 120` so the width trigger is automatic; the "3+ attrs" floor is the review convention.

```tsx
<Spinner size="sm" />                                    // ≤2 attrs → inline
<ColorPicker
  triggerVariant="swatch"
  value={fromColor}
  onValueChange={(hex) => setStop(0, hex)}
  aria-label="Gradient start color"
/>                                                       // 3+ attrs & wide → one per line
```

---

## 8. Use

- a value that is one of an enum's members is modeled as the **enum**, compared `x === Enum.Member` — never fanned into `isSolid` / `isGradient` booleans ([enums.md](../code-style/enums.md) § No parallel `isMember` flags).
- where a component lives (the `presentation/` layer) → [architecture.md](../architecture/architecture.md); forms + hooks → [forms.md](forms.md) · [hooks.md](hooks.md).
