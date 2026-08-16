# Vue SFC

*Last updated: 2026-08-15*

> Block layout, in-file order, shared DOM vocabulary, and JSDoc verbs for a Vue Single-File Component.
> Purpose — the React rules in [components.md](components.md) have no counterpart for `<script setup>`, macros, `useAttrs`, or emits.
> Use case — writing or reviewing any `.vue` file, above all in `@wow-two-beta/ui-vue`.

## Blocks

- must put exported types and module-scope constants in a plain `<script lang="ts">` — `<script setup>` cannot hold an `export`.
- must put instance logic in `<script setup lang="ts">`.
- must order blocks `<script>` → `<script setup>` → `<template>` → `<style>`.
- must not repeat an import across the two blocks — Vue merges them into one module scope.
- must not add a plain `<script>` block that exports nothing.

---

## Order inside `<script setup>`

- must order **macros → constants → composables → reactive state → computed → watchers → functions**.
- must keep `defineOptions` · `defineProps` · `defineEmits` · `defineSlots` together at the top.
- must not declare a constant, state, or a `computed` between two functions.
- must declare a `computed` before any `watch` that reads it.

---

## Imports

- must import across `src/` with **relative** paths — an alias survives into the emitted `.d.ts`, where a consumer cannot resolve it.
- must use the `@src/*` alias in `tests/` only.
- must ignore the IDE's "import can be shortened" hint inside a library's `src/`.
- group order and intra-group sort → [../code-style/imports.md](../code-style/imports.md).

---

## Docs

- must anchor the component doc as `/** Renders … */` immediately above `defineOptions`.
- must give the props interface `/** Defines props for … */`, and every member a one-liner.
- must doc each emit with `Fires when …`, each slot with `The …`.
- must doc a `computed` as the value it yields (`The …`), never `Computes …`.
- must doc a `watch` by the effect it causes (`Emits …` · `Syncs …` · `Resets …`), never `Watches …`.
- must doc a function with a third-person verb — `Copies …` · `Resolves …`.
- must mark a non-exported type, constant, or helper `@internal`.
- must keep a doc a **one-liner**; the six-condition exception is in [../code-style/documentation.md](../code-style/documentation.md) § The multi-line exception.
- must keep a non-JSDoc `/* */` comment to **one line** stating a role — no exception at all.
- must not restate a rule from this file at a use site → [../code-style/documentation.md](../code-style/documentation.md) § Scope.
- verb table for everything else → [../code-style/documentation.md](../code-style/documentation.md).

---

## Width

- must wrap every line at **120 columns**, comments included.
- Prettier owns code width (`printWidth: 120`); ESLint `max-len` owns comments, which Prettier never reflows.
- must run `pnpm format` before `pnpm lint`.

---

## Shared vocabulary

One home per DOM literal, in `foundation/utils`. Take from it; never re-declare per component.

| Need | Take | Example |
|---|---|---|
| ARIA / DOM attribute name | `AriaAttribute` | `AriaAttribute.Label` |
| Boolean attribute value | `AttributeValue` | `AttributeValue.True` |
| Event name | `DomEvent` | `emit(DomEvent.Error, cause)` |
| The `onX` prop for an event | `HandlerProp<E>` | `HandlerProp<typeof DomEvent.Error>` |
| Element tag | `ElementTag` | `ElementTag.Div` |

- must add a missing literal to the shared module rather than declaring it locally — a shared const object costs one object for the whole package, a per-component tuple multiplies by component count.
- must name a **constant** PascalCase, never `SCREAMING_SNAKE` → [../code-style/constants.md](../code-style/constants.md).
- must not extract a DOM attribute **name** used once in a template — markup is not code.

---

## Types over literals

- must name another type's key through `keyof Pick<T, 'k'>`, never a bare `'k'` union — `Omit` accepts a key `T` lacks, `Pick` does not.
- must declare a literal used in **both** a type and at runtime once, as an `as const` tuple, and derive the type from it.
- must not hoist a key already inside a `keyof Pick<…>` into a runtime tuple — the alias is the extraction.

```ts
const OwnedAttributes = [AriaAttribute.Label] as const;
type OwnedAttribute = (typeof OwnedAttributes)[number];
type ReplacedButtonProp = keyof Pick<ButtonProps, HandlerProp<typeof DomEvent.Error>>;
```

---

## Attributes

- must read an attribute Vue would camelize off `useAttrs()`, not `props` — a declared `'aria-label'` arrives as `props.ariaLabel`.
- must set `inheritAttrs: false` when the component re-renders an attribute under its own value.
- must filter the owned keys out of the forwarded set before `v-bind`.
- must mark a types-only heritage `/* @vue-ignore */`.
- must extend **one** named type, never a comma-separated heritage list — Prettier lifts `/* @vue-ignore */ ` above a multi-entry `extends`, where the SFC compiler stops seeing it.
- must re-declare a heritage prop in the body when it needs a `withDefaults` default.
- must reach for `dataAttr()` for a boolean `data-*`; a component whose standard pins a literal value keeps it, from `AttributeValue`.

---

## Gates

Four, and each catches something the others miss. Run all four; `check:sfc` is the one with no substitute.

| Gate | Catches |
|---|---|
| `pnpm format` | code width, quote style, trailing commas |
| `pnpm lint` | comment width, boundaries, unused code |
| `pnpm typecheck` | types **and** `check:sfc` — a heritage the SFC compiler cannot resolve |
| `pnpm test` | behaviour, SSR safety, mount smoke |

**What no gate catches: what a comment says.** `max-len` measures a comment's width and nothing else, so a doc
that restates a convention, argues a trade-off, or narrates history passes all four. Tooling cannot close this —
a rule-restating doc is well-formed prose of legal length. It is caught in review, or not at all, which is why
[../code-style/documentation.md](../code-style/documentation.md) § Scope carries a test a reviewer can apply in one pass.

---

## Reference

[`CopyButton.vue`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/actions/copyButton/CopyButton.vue)
is the worked example — every rule above holds in it, at zero warnings across all four gates.
