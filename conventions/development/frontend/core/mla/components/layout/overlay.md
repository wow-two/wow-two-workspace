# Overlay

*Last updated: 2026-08-19*

> The in-box pin — a child anchored to a corner or an edge of the box it already sits in.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Overlay.spec.md`.

## Reach for it when

- must pin a control to a corner of an image, a card or a media box
- must keep the pin inside its ancestor's box — it never portals out
- should reach for it for corner badges, close buttons, hover-revealed actions

---

## Instead of

| Reach for | When |
|---|---|
| `Popover` | the surface floats free and belongs to one trigger |
| `HoverCard` | the hover opens a read-only preview surface |
| `Backdrop` | the page behind has to dim |
| [Box](box.md) | the child sits in the flow and needs no anchor |

---

## Values

- must give the nearest ancestor `relative` — the pin resolves against it
- must add `class="group"` to that ancestor for `hover` or `focus-within`
- must leave `position` at `top-right`, `inset` at `0.5rem`, `zIndex` at `10`
- must not set `role` or `aria-*` on it — the child carries its own semantics
- should leave `transition` unset — it resolves to `fade` under gating, `none` otherwise
- should keep `asChild` on, its default; off adds a wrapping `div`
