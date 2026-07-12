# Naming

*Last updated: 2026-07-08*

## Files — PascalCase (one rule, one exception)

**All `.ts` and `.tsx` files use PascalCase.** The file name matches the primary export.

**Exception:** `index.ts` barrel files are always **lowercase** — Node/TS module resolution depends on it (`import from "../foo"` → `foo/index.ts`). PascalCase `Index.ts` breaks on case-insensitive filesystems (macOS, Windows).

```
// ✅ Correct
ListingCard.tsx            ← component exports ListingCard
UseSupplyListings.ts       ← hook exports useSupplyListings
Constants.ts               ← exports constants
Filters.ts                 ← exports filter types
ListingDto.ts              ← exports ListingDto interface
ContactType.ts             ← exports ContactType enum
index.ts                   ← barrel export (always lowercase)

// ❌ Wrong
listingCard.tsx             ← camelCase file
use-supply-listings.ts      ← kebab-case file
contact-type.ts             ← kebab-case file
```

**Hooks file vs export mismatch is accepted:** the export `useSupplyListings` is camelCase (React convention), but the file is `UseSupplyListings.ts` (PascalCase). One universal file rule beats a per-kind carve-out.

## Folders — camelCase

```
// ✅ Correct
src/supply/components/
src/common/hooks/
packages/domain/src/listings/core/enums/
src/supply/propertyInfo/

// ❌ Wrong
src/Supply/Components/       ← PascalCase folders
src/property-info/           ← kebab-case folders
```

## Helper-file suffixes

Non-component utility files co-located in a folder use **descriptive PascalCase + role suffix**:

| Suffix | Use | Examples |
|---|---|---|
| `*Extensions.ts` | Helpers that extend a built-in/external type (see [extensions.md](extensions.md)) | `DateExtensions.ts`, `StringExtensions.ts` |
| `*Styles.ts` | Shared `tailwind-variants` configs (see [styling.md](../presentation/styling.md)) | `ButtonStyles.ts`, `InputStyles.ts` |
| `*Helpers.ts` | Domain-specific fns that don't fit `Extensions` | `FormHelpers.ts` |

The `*Extensions` suffix is borrowed from .NET extension methods — a deliberate divergence from JS's camelCase-utilities norm, for consistency with the .NET-heavy wow-two ecosystem. **Internal** = absent from `index.ts`, not a naming signal.

## Resource-access abstractions — `*Broker`

A swappable app-side seam over a **client-side resource** — `localStorage`, `sessionStorage`, a Redux store, an in-memory map — is a **`*Broker`**: the contract `StorageBroker`, its instances `localStorageBroker` / `memoryBroker`, and the injected dependency a `broker` param / option. It borrows the backend **`Broker`** term ([component-names.md](../../backend/foundation/component-names.md) — "app-side seam over an external dependency"), so the same word names the same idea on both sides of the stack. Reach for it only for a resource seam; a plain helper stays `*Helpers` / `*Extensions`.

## App-shell baseline components — `App*`

The framework singletons every app has exactly one of — the router root, the shell, the root error boundary — take an **`App*`** prefix so they group together and read as the app's *frame*, not feature UI. They live in `bootstrap/` and are the seam that extracts to `@wow-two-beta/app` — the names are the stable contract.

| Component | Role | Home |
|---|---|---|
| `AppRoot` | router root element — `<ScrollRestoration>` + title sync + `<Outlet>` | `bootstrap/router/` |
| `AppLayout` | the visible shell — SDK `AppShell` + sidebar/header + `<Outlet>` | `bootstrap/` |
| `AppErrorBoundary` | root route `errorElement` | `bootstrap/router/` |

**Bare (not `App*`):** a **page** the router renders keeps a plain page name — `NotFound` (the `*` catch-all), the `*Page` places — and a **utility** stays descriptive — `DocumentTitle`, `createAppRouter`. `App*` marks the singleton *frame* pieces, not every routing file. See [routing.md](../architecture/routing.md).

## Exports

- **Named exports preferred** — avoid `export default` except for React page/view components used with lazy loading.
- **Barrel `index.ts`** in each folder that has a public API; it controls what is public.

## Component props

Prop **names** follow a fixed vocabulary so any component reads the same way. (Prop **shape** rules — `readonly`, no-destructure, `interface` — live in [components.md](../presentation/components.md).)

| Kind | Prefix / shape | Examples |
|---|---|---|
| Standalone boolean | `is*` / `has*` / `can*` / `show*` | `isDisabled`, `isInvalid`, `isLoading`, `hasError`, `canResize`, `showLabel` |
| Event handler | `on*` | `onClick`, `onSelect`, `onValueChange` |
| Render-prop | `render*` | `renderItem`, `renderEmpty`, `renderTrigger` |

`show*` names a boolean for **visibility / display intent** (`showLabel`, `showFooter`) — it joins `is*` / `has*` / `can*` as a standalone-boolean prefix.

**`on*` is inbound-only — a method the consumer calls is an imperative verb.** `on*` names an **inbound event-handler prop** — a callback *passed into* a component. A hook / view-model **method the consumer calls** is an imperative verb (`setSearchKeyword`, `selectEmoji`, `clearSelection`) — never `on*`-prefixed. `onClearSelection` for something you call reads as a prop you'd wire up; `clearSelection` reads as the action it is.

Within a single-purpose inner component an unambiguous abstract method name (`clear`, `select`) is fine; disambiguate (`clearSelection`, `selectEmoji`) only when the surrounding scope makes the bare verb ambiguous.

| Do | Avoid |
|---|---|
| `onSelect` (prop) · `selectEmoji` (method you call) | `onSelectEmoji` for a method the consumer calls |
| `clearSelection`, `setSearchKeyword` | `onClearSelection`, `onSetSearchKeyword` (method dressed as a prop) |

**Controlled triad — the one exception to `is*`.** A value a parent may own ships as a fixed trio that reads as a unit. The controlled member keeps the **bare root** — it is *not* `is*`-prefixed — so the three names line up:

| Prop | Role |
|---|---|
| `x` (bare root) | **controlled** value — parent owns state |
| `defaultX` | **uncontrolled** seed — initial value, component owns state after |
| `onXChange` | change handler — fires with the next value |

Three canonical triads: `{ open, defaultOpen, onOpenChange }` · `{ value, defaultValue, onValueChange }` · `{ checked, defaultChecked, onCheckedChange }`. Use one of `x` / `defaultX` per usage; never both. The bare root is reserved for the triad — a *standalone* boolean with no `default*`/`on*Change` partners still takes `is*` (`isOpen` only if it's a one-off display flag, never half of a controlled pair).

**Native attributes pass through unrenamed.** A real DOM attribute (`type`, `disabled`, `name`, `id`, `role`) and every `aria-*` / `data-*` keep their exact HTML spelling — they hit the element verbatim, so renaming breaks the contract. Rename only the *public prop* a component introduces; never the ones it forwards.

**Single idiom carve-out — `asChild`.** The Radix-style `asChild` idiom (render into the consumer's child instead of the component's own element) keeps its name even though it isn't `is*`-prefixed. It's a recognized cross-library term; aliasing it to `isChild` would obscure intent.

| Do | Avoid |
|---|---|
| `isDisabled`, `isInvalid`, `hasIcon`, `canDismiss` | `disabledFlag`, `invalid`, `iconBool`, `dismissable` (no/ad-hoc prefix) |
| `onChange`, `onValueChange` | `handleChange`, `changeCallback`, `onChanged` |
| `renderItem` | `itemRenderer`, `itemTemplate` |
| `{ open, defaultOpen, onOpenChange }` (bare root) | `isOpen` + `defaultOpen` + `onOpenChange` (prefixing the controlled member) |
| `{ value, defaultValue, onValueChange }` | `value` + `initialValue` + `onUpdate` (mixed vocabulary) |
| `aria-label`, `data-state`, native `type` | `ariaLabel`, `dataState`, `buttonType` (renaming forwarded DOM props) |
| `asChild` (the one accepted idiom) | inventing new un-prefixed boolean idioms |

```typescript
/** Defines props for the dismissible info banner. */
interface InfoBannerProps {
  readonly open: boolean;              // controlled triad → bare root, NOT isOpen
  readonly defaultOpen?: boolean;      // uncontrolled seed (use root or default, not both)
  readonly onOpenChange: (open: boolean) => void;  // triad handler → on*Change
  readonly isDisabled: boolean;        // standalone boolean → is*
  readonly isInvalid?: boolean;        // standalone boolean → is*
  readonly hasIcon: boolean;           // standalone boolean → has*
  readonly renderAction?: () => ReactNode;         // render-prop → render*
  readonly "aria-label"?: string;      // native a11y attr — NOT renamed
  readonly asChild?: boolean;          // the single idiom carve-out
}
```

## Quick reference

| Kind | Casing | Example |
|---|---|---|
| Component file | PascalCase | `FilterBar.tsx` |
| Component export | PascalCase | `FilterBar` |
| Hook file | PascalCase | `UseTheme.ts` |
| Hook export | camelCase `use*` | `useTheme` |
| Util / extensions file | PascalCase | `Currency.ts`, `PersonExtensions.ts` |
| Type file | PascalCase | `Listing.ts` |
| Type export | PascalCase | `Listing` |
| Domain enum / label Record | PascalCase, singular, no `Enum` suffix | `ContactType`, `ContactTypeLabels` |
| UI value-set (const `as const`) | PascalCase, singular, no labels | `HtmlElement`, `ButtonType`, `Key` |
| Constant — scalar / data | PascalCase, `as const` for objects | `PresetIconSize`, `Angles`, `DefaultRadius` |
| Standalone boolean prop | `is*` / `has*` / `can*` / `show*` | `isDisabled`, `isInvalid`, `hasIcon`, `showLabel` |
| Handler prop (inbound) / render prop | `on*` / `render*` | `onValueChange`, `renderItem` |
| Hook / view-model method (consumer calls) | imperative verb, never `on*` | `selectEmoji`, `clearSelection`, `setSearchKeyword` |
| Controlled triad (bare root) | `x` / `defaultX` / `onXChange` | `open` / `defaultOpen` / `onOpenChange` |
| Prop idiom carve-out | as-is | `asChild` |
| Folder | camelCase | `propertyInfo/` |
| Barrel | lowercase | `index.ts` |

**Constants are PascalCase** — a scalar / data const is the same category as an enum / value-set, so it takes the same casing (`PresetIconSize`, `DefaultRadius`), not `UPPER_SNAKE`. Existing `UPPER_SNAKE` constants migrate gradually; new code is PascalCase.

## See also

- [enums.md](enums.md) — enums-as-`enum` + label Record; domain enum vs. UI value-set split
- [components.md](../presentation/components.md) — one-component-per-folder; prop **shape** rules (`readonly`, no-destructure) that pair with the prop **names** above
- [extensions.md](extensions.md) — `*Extensions` const objects
