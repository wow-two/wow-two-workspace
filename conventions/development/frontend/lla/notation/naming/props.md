# Props

*Last updated: 2026-08-19*

> The prop-name vocabulary every component reads by — boolean prefixes, handlers, render props, the controlled
> triad, and the two carve-outs. Prop **shape** (`readonly`, `interface`, and which access each framework
> fixes) is a [construct](../../../mla/constructs/constructs.md) rule; this doc names them.

## Vocabulary [REQUIRED]

| Kind | Prefix / shape | Examples |
|---|---|---|
| standalone boolean | `is*` · `has*` · `can*` · `show*` | `isDisabled` · `hasError` · `canResize` · `showLabel` |
| event handler | `on*` | `onClick` · `onSelect` · `onValueChange` |
| render-prop | `render*` | `renderItem` · `renderEmpty` · `renderTrigger` |

- must prefix a boolean naming visibility or display intent `show*` — it joins `is*` / `has*` / `can*`.
- must not invent a new un-prefixed boolean idiom.

---

## Inbound versus imperative

- must use `on*` for an **inbound** handler prop only — a callback passed *into* a component.
- must name a hook or view-model method the consumer **calls** with an imperative verb — `selectEmoji`,
  `clearSelection`, `setSearchKeyword` — never `on*`.
- may keep a bare verb (`clear`, `select`) inside a single-purpose component, and must disambiguate only when
  the surrounding scope makes it ambiguous.

| Do | Avoid |
|---|---|
| `onSelect` (prop) · `selectEmoji` (method you call) | `onSelectEmoji` for a method the consumer calls |
| `clearSelection` · `setSearchKeyword` | `onClearSelection` — a method dressed as a prop |

---

## The controlled triad

A value a parent may own ships as a fixed trio that reads as a unit, and the controlled member keeps the **bare
root** so the three names line up.

| Prop | Role |
|---|---|
| `x` (bare root) | **controlled** value — the parent owns state |
| `defaultX` | **uncontrolled** seed — initial value, the component owns state after |
| `onXChange` | change handler — fires with the next value |

- must reach for one of the three canonical triads — `{ open, defaultOpen, onOpenChange }` ·
  `{ value, defaultValue, onValueChange }` · `{ checked, defaultChecked, onCheckedChange }`.
- must use one of `x` / `defaultX` per usage, never both.
- must reserve the bare root for the triad — a standalone boolean with no `default*` / `on*Change` partner
  still takes `is*`.

---

## Carve-outs

- must pass a native attribute through unrenamed — a real DOM attribute (`type`, `disabled`, `name`, `id`,
  `role`) and every `aria-*` / `data-*` keep their exact HTML spelling, because they hit the element verbatim.
- must rename only a prop the component itself introduces, never one it forwards.
- must keep `asChild` as spelled — the Radix-style idiom is a recognized cross-library term, and `isChild`
  would obscure it. It is the single un-prefixed boolean carve-out.

| Do | Avoid |
|---|---|
| `isDisabled` · `isInvalid` · `hasIcon` | `disabledFlag` · `invalid` · `iconBool` |
| `onChange` · `onValueChange` | `handleChange` · `changeCallback` · `onChanged` |
| `renderItem` | `itemRenderer` · `itemTemplate` |
| `{ open, defaultOpen, onOpenChange }` | `isOpen` + `defaultOpen` + `onOpenChange` |
| `aria-label` · `data-state` · native `type` | `ariaLabel` · `dataState` · `buttonType` |

```typescript
/** Defines props for the dismissible info banner. */
interface InfoBannerProps {
  readonly open: boolean;                            // controlled triad → bare root, NOT isOpen
  readonly defaultOpen?: boolean;                    // uncontrolled seed (root or default, never both)
  readonly onOpenChange: (open: boolean) => void;    // triad handler → on*Change
  readonly isDisabled: boolean;                      // standalone boolean → is*
  readonly hasIcon: boolean;                         // standalone boolean → has*
  readonly renderAction?: () => ReactNode;           // render-prop → render*
  readonly "aria-label"?: string;                    // native a11y attr — NOT renamed
  readonly asChild?: boolean;                        // the single idiom carve-out
}
```

---

## Neighbours

- [naming](naming.md) — the file, folder and constant casing these props sit inside
- [constructs](../../../mla/constructs/constructs.md) — the prop **shape** rules: `readonly`, `interface`
