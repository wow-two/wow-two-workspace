# Constructs

*Last updated: 2026-08-19*

> What each role a frontend declares **is** — the role, the suffix it takes, the shape of its contract.
> Purpose — the definition register; which one to reach for and with what values is
> [components](../components/components.md), and one component's own surface is its SDK `{Component}.spec.md`.
> Use case — writing a component file top to bottom, or coining a suffix no existing kind covers.

## The folder

| Folder | Covers | Lead |
|---|---|---|
| `visual/` | the 15 kinds that render, what each composes with, where it lives | [visual](visual/visual.md) |
| `behavior/` | the seams a component consumes, and the `use*` state it owns | [behavior](behavior/behavior.md) |
| `data/` | the model and carrier types a slice declares | [data](data/data.md) |

A doc saying which thing to reach for, or what value a parameter should carry, is a
[component](../components/components.md) instead.

The rest of this file is the authoring pass for one rendering kind.

**Flow:** `kind → name → folder → docs → props interface → styling → JSX → suffix gate`

---

## 1. Kind

- must classify by **what the component owns**, not by where it happens to render.
- must pick the kind from the [visual kinds](visual/visual.md) before naming anything else.
- must take the suffix that kind fixes (§ *Naming*).

---

## 2. Naming

The suffix is the kind written down — a reader who knows it knows the contract and the folder.

- must end every component name with the suffix its kind fixes; the kind's doc states which
  ([visual kinds](visual/visual.md) § *Suffix routing*).
- must read the suffix as the thing the component **is**, never as the thing it decorates — it trails, never leads.
- must suffix every component, however well known the bare word is — `Select` alone does not say whether it is
  a control, an overlay or a page, and the reader pays that ambiguity on every file they open.
- an enum needs no kind suffix; its own name carries the role (`*Type` · `*Status` · `*Level`)
  ([enums](../../lla/components/enums.md)).
- must not reach for a synonym of a listed suffix — a `*Container`, a `*Dialog`, a `*Selector` names nothing new.
- must name a seam from the [headless suffixes](behavior/headless-suffixes.md) instead; no component suffix fits one.
- must coin a suffix only through the gate below (§ *Adding a new suffix*).

```txt
✅ CodesListPage · AppShell · MonthView · TabsPanel · BottomSheet · JsonEditor · MeterBar
✅ SelectInput · StackLayout · FabButton     (a known word still takes its kind)
✅ BadgeOverlay · LoadingOverlay        (the component IS an overlay, so Overlay trails)
❌ CodesListContainer · DeleteDialog · ColorSelector · StatusIcon · EmptyPlaceholder
❌ Select · Stack · Fab                      (bare — the kind is unreadable)
❌ OverlayConfirmDelete                 (Overlay never leads — that reads as an instruction, not a thing)
```

### Modifiers

- must suffix `*Compact` for a condensed variant of a component that already exists.
- must suffix `*Simple` for the free-children counterpart of a slotted root — `AlertSimple` · `ToastSimple`.
- must prefix `App*` for app-frame singletons only
  ([naming](../../lla/notation/naming/naming.md) § *App-shell baselines*).
- compound subpart naming and export → [compound](compound.md).

```txt
✅ AlertSimple · BannerSimple · AccordionItem · MenuItem · AppShell · AppErrorBoundary
❌ SimpleAlert · CompactNavItem · ItemMenu     (a modifier trails; the role word ends the name)
```

---

## 3. Folder

Whether a component takes a folder of its own is the deliverable's answer: a package gives every component one
([library](../../../shapes/library/library.md) § *Layout*), a product may keep flat files grouped by concern
([architecture](../../../shapes/app/architecture/architecture.md) § *Component files*).

- must keep sub-components internal either way — a non-exported sibling or a nested fn; only the barrel's
  re-exports are public.
- applies to every rendering kind, not to hooks or lib files.
- must order the component file: imports → types → constants → pure helpers → component fn → sub-components
  (only when small and tightly coupled). Import order: [style](../../lla/notation/style/style.md).

---

## 4. Docs

The verb table and the multi-line exception live one layer down
([documentation](../../lla/notation/documentation/documentation.md)); a component adds only these.

- must open the component's one-line JSDoc with `Renders …`, and the props interface's with `Defines props for …`.
- must leave one blank line between documented members; a props interface is a model ([models](data/models.md)).

---

## 5. Props interface

- must name the props `interface` `{Component}Props`, one per file
  ([typescript](../../lla/constructs/typescript/typescript.md)).
- must mark every member `readonly`, and type an array prop `ReadonlyArray<T>` to block `.push()`.
- must read a prop through whichever access its framework fixes — [vue](../frameworks/vue/macros.md) bans
  destructure and takes defaults through `withDefaults`; [react](../frameworks/react/react.md) destructures in
  the parameter. The `interface` above is the shared surface either way.

```tsx
/** Defines props for the fill controls. */
interface FillControlsProps {
  /** The current foreground gradient, or null for a solid fill. */
  readonly gradient: Gradient | null;

  /** Emits the next gradient, or null to fall back to the solid fill. */
  readonly onGradientChange: (gradient: Gradient | null) => void;
}
```

---

## 6. Styling

- must use Tailwind utilities only, conditional classes through `cn()`
  ([styling](../../../shapes/app/platform/styling.md)).
- must put a multi-variant class map in a co-located `*.variants.ts` / `*Styles.ts` built with
  `tailwind-variants` — never inline a large conditional class string.
- should reach for a `@wow-two-beta/ui` component before hand-rolling; a missing one is built locally, then
  extracted once generic ([boundaries](../../../shapes/app/architecture/boundaries.md)).
- must duplicate a pure DRY or layout wrapper inline; an atom carrying logic is never product-local.

---

## 7. JSX attributes

- must put one attribute per line once an element has 3+ attributes **and** the line passes 120 characters.
- must give peer siblings one shape — never mix inline and wrapped.
- must set Prettier `printWidth: 120` — the width trigger is then automatic, the 3-attribute floor a review gate.

---

## 8. Adding a new suffix — the gate [REQUIRED]

Answer in order; the first **yes** picks the suffix, and coining requires four `no`s.

1. does it render? → the suffix its kind fixes ([visual kinds](visual/visual.md) § *Suffix routing*).
2. does it own reactive state for a subtree? → `use*` ([hooks](behavior/hooks.md)).
3. does it cross the wire or a layer seam? → `*Dto` · `*ApiRequest` · `*Content` ([models](data/models.md)).
4. does it implement a contract behind a seam? → the domain's provider vocabulary ([domains](../domains/domains.md)).

- must coin only for a role no existing suffix covers — a distinct verb, never a synonym.
- must not coin inline; a name that misses is copied forward by every later scaffold.
- must state the role's verb in one line — no verb to state means it is not a new role.
- must name the nearest two suffixes and why each fails; failing against none means it folds.
- must bring both to the developer and wait — only a confirmed suffix is implemented.
- must add the confirmed suffix to its kind's doc — or give a whole new kind its own doc — in the same pass.
- must raise this bar under rapid scaffolding, never lower it — it replicates a bad name fastest.

---

## Neighbours

- [visual](visual/visual.md) — the 15 kinds that render, and what each composes with
- [vue SFC](../frameworks/vue/vue-sfc.md) — the Vue counterpart: blocks, macro order, emit and slot verbs
- [props](../../lla/notation/naming/props.md) — the prop-name vocabulary these shapes are spelled in
- [enums](../../lla/components/enums.md) — modelling a value as an enum member rather than parallel `is*` booleans
- [architecture](../../../shapes/app/architecture/architecture.md) — the `presentation/` layer a component lives in
