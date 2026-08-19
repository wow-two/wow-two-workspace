# NavItem

*Last updated: 2026-08-19*

> The standing row in a sidebar or nav rail.
> What a nav component is → [nav](../../constructs/visual/nav.md).
> Its full surface → `NavItem.spec.md`.

## Reach for it when

- must offer a destination the reader returns to across routes
- must pair a leading icon with a label, and a trailing count or status dot
- should render one row per destination, in a list the caller owns

---

## Instead of

| Reach for | When |
|---|---|
| `NavigationMenuLink` | the destination sits in a horizontal top strip |
| `MenuItem` | the row lives inside a floating menu, not a standing list |
| [Breadcrumb](breadcrumb.md) | the row would report position rather than offer a destination |

---

## Values

- must pass `as-child` when the destination routes — the bare element is an `<a>`
- must keep the label short under `as-child`; that path drops the truncating label span
- must set `is-active` on exactly one row per route match
