# Component Catalog

*Last updated: 2026-08-19*

> The index of the component **kinds** our SDK ships — what each kind is, what it composes with, what it is for.
> Purpose — pick the kind before the name; the kind fixes the suffix, the group folder, and the contract shape.
> Use case — starting a component, or placing one that already exists.

## Reading it [REQUIRED]

- must pick the kind first — it fixes the suffix (§ *Suffix routing*) and the group folder.
- must read a component's co-located `{Component}.spec.md` for its props, slots, emits, and states.
- must not look for a component's own entry here — this file indexes kinds, the spec specifies the component.
- must add a kind only through the coining gate ([constructs](constructs.md) § *Adding a new suffix*).

```markdown
<!-- ✅ the kind is looked up here, the component in its spec -->
overlay → overlays/ → `*Modal` · `*Drawer` · `*Sheet`  →  Modal.spec.md
<!-- ❌ a component's props do not live in a convention -->
| Modal | `open` · `dismissable` · `size` |
```

---

## Kinds

| Kind | Is | Used with | Used for | Lives in |
|---|---|---|---|---|
| [page](page.md) | a routed viewport owner | layout · view · overlay | one URL's whole surface | app `pages/` |
| [view](view.md) | a swappable content body | page · panel | one display mode | `display/` |
| [panel](panel.md) | a bounded region of a parent | view · layout | one pane of a whole | `display/` · `layout/` |
| [layout](layout.md) | an arrangement owning no content | every visual kind | placing children | `layout/` |
| [overlay](overlay.md) | a surface floating above the page | action · field | a task without leaving | `overlays/` |
| [nav](nav.md) | a move between places | layout · overlay | wayfinding | `nav/` |
| [action](action.md) | an intent trigger, no value | overlay · form | running a command | `actions/` |
| [control](control.md) | a widget owning one value | field · form | reading input | `forms/` |
| [field](field.md) | a labeled control plus its help | control · form | one form value | `forms/` |
| [display](display.md) | a render of content it does not own | layout · view | showing data | `display/` |
| [feedback](feedback.md) | a report of system state | layout · provider | saying what happened | `feedback/` |
| [indicator](indicator.md) | a passive mark of live state | display · nav | status at a glance | `feedback/` |
| [state](state.md) | a stand-in for no content | view · panel | empty · loading · failed | `display/` · `router/` |
| [provider](provider.md) | a context supplier, slot only | any subtree | sharing one capability | `auth/` · `query/` |
| [primitive](primitive.md) | headless behavior, no styling | every visual kind | reusing behavior | `primitives/` |

---

## Suffix routing

One kind per suffix. The kind's doc is the **authority** — it states the suffix, the bare names that take none,
and the shape words that stand in for it; this table only routes.

| Suffix | Kind, and the doc that states it |
|---|---|
| `*Page` | [page](page.md) |
| `*View` | [view](view.md) |
| `{Root}Panel` · `*Tab` · `*Section` | [panel](panel.md) |
| `*Layout` · `*Shell` | [layout](layout.md) |
| `*Modal` · `*Drawer` · `*Sheet` · `*Popover` · `*Tooltip` · `*HoverCard` · `*Overlay` | [overlay](overlay.md) |
| `*Menu` · `*Item` | [nav](nav.md) |
| `*Button` · `*Group` | [action](action.md) |
| `*Input` · `*Picker` · `*Editor` · `*Controls` · `{Control}Group` | [control](control.md) |
| `*Field` · `*Form` | [field](field.md) |
| `*Table` · `*Grid` · `*Row` · `*Cell` · `*Card` · `*Badge` · `*Tag` · `*Status` | [display](display.md) |
| `*Preview` · `*Carousel` · `*Gallery` · `*Viewer` · `*Player` · `*Renderer` · `*Glyph` | [display](display.md) |
| `*Callout` · `*Toast` · `*Alert` · `*Banner` | [feedback](feedback.md) |
| `*Indicator` · `*Bar` | [indicator](indicator.md) |
| `*State` · `*Gate` · `*Boundary` | [state](state.md) |
| `*Provider` · `*Context` | [provider](provider.md) |
| none — the behaviour's own word | [primitive](primitive.md) |

- must read the modifiers (`*Compact` · `*Simple` · `App*`) at [constructs](constructs.md) § *Naming*, and
  the coining gate at that doc's § *Adding a new suffix*.

---

## Composition order

The ladder a surface is built down — each rung composes the rungs below it, never a rung above.

- `page` → `layout` → `view` → `panel` → `display` · `control` · `action` → `indicator` · `state`
- `overlay` hangs off any rung — it is opened by an `action` and portals out of the tree.
- `provider` wraps a rung without rendering one — it supplies, it does not compose.
- `primitive` sits under every rung — behavior and a11y with no visual of its own.

- must not compose upward — a `display` never mounts a `view`, a `control` never mounts a `panel`.
- must lift a component whose children climb the ladder, rather than widening its props.

```txt
✅ CodesListPage → AppShell → CodesView → TabsPanel → DataTable → StatusIndicator
❌ DataTable → CodesView          (a display mounting a view — composes upward)
```

---

## Placement

- must read every kind's group folder (`presentation/actions/` · `presentation/forms/`) as **SDK layout** — the
  package groups by kind because it ships no domains.
- must place the same kind by **domain** in a product, in the layer's slice or its `common/`
  ([architecture](../architecture/architecture.md) § *Domains*).
- must not carry the SDK's group folders into a product tree; the kind fixes the suffix and the contract, not
  the folder a product puts it in.
- must place a **capability module** — `auth/` · `query/` · `flags/` · `router/` · `foundation/` — at the SDK
  root, beside `presentation/`, never inside it. A capability ships seams and providers, not visual kinds.
- must keep a `foundation/` primitive importing nothing from `presentation/` or a capability module; the
  boundary is linted, and it runs one way.

---

## Headless kinds

Not components — the seams a component consumes. Their vocabulary is the [headless suffixes](headless-suffixes.md).

- must name a headless role from that keep-list — `*Client` · `*Bus` · `*Registry` · `*Strategy` · `*Policy`.
- must not read `*Provider` as one kind — the `.vue` file is a [provider](provider.md), the `.ts` interface is a seam.

```ts
// ✅ two roles, one word — the seam and the component that installs it
export interface AnalyticsProvider { track?(e: AnalyticsEvent): void }   // src/analytics/ — a seam
// AuthProvider.vue — a provider component; its template is `<slot />`
// ❌ a seam declared in presentation/
// src/presentation/display/AnalyticsProvider.ts
```

---

## Neighbours

- [constructs](constructs.md) — how any component is shaped, named, and the gate for coining a new suffix
- [headless suffixes](headless-suffixes.md) — the second keep-list, for seams a component consumes
- [architecture](../architecture/architecture.md) — the layer and domain a kind's folder sits in
- [hooks](hooks.md) — the `use*` counterpart, for state a component owns rather than renders
