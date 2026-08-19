# Modal

*Last updated: 2026-08-19*

> The centred blocking dialog — the default surface when a flow must own the screen until it resolves.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).
> Its full surface → `Modal.spec.md`.

## Reach for it when

- must hold a flow that owns the screen — a form, an edit, a picker
- must block the page; nothing behind the scrim is reachable until it closes
- should carry a title, a body, and a footer of actions

---

## Instead of

| Reach for | When |
|---|---|
| [AlertModal](alertModal.md) | the flow confirms a destructive act and must not dismiss by accident |
| [Drawer](drawer.md) | the body is long or ancillary and the page stays the subject |
| [BottomSheet](bottomSheet.md) | the same place on a phone — thumb-reachable and draggable |
| [Popover](popover.md) | the content belongs to one trigger and the page need not dim |

---

## Values

- must not set `role` — it is internal, and [AlertModal](alertModal.md) is the `alertdialog` path
- should leave `dismissOnOutsideClick` on; a flow that cannot afford it is an alert modal
- should set `hideBackdrop` only when an outer surface already dims the page
