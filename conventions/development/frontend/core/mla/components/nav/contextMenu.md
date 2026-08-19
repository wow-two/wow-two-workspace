# ContextMenu

*Last updated: 2026-08-19*

> The right-click menu over a region, opened where the pointer is.
> What a nav component is → [nav](../../constructs/visual/nav.md).
> Its full surface → `ContextMenu.spec.md`.

## Reach for it when

- must offer commands for the object under the pointer, with no visible trigger
- must cover a region rather than a single control
- must not make it the only path to a command — the trigger region is not focusable

---

## Instead of

| Reach for | When |
|---|---|
| [DropdownMenu](dropdownMenu.md) | a visible button should open the same list |
| [Menu](menu.md) | the anchor is an element, not the point the gesture happened at |

---

## Values

- should keep the default `2` px offset — it hangs off a point, not a control
- must not tune the touch long-press — the `600` ms delay is fixed
- must not expect focus back on the trigger — it returns to the pre-gesture element
