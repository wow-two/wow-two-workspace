# Drawer

*Last updated: 2026-08-19*

> The edge-anchored panel — slides in from a viewport side while the page stays the subject.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).
> Its full surface → `Drawer.spec.md`.

## Reach for it when

- must hold a long or ancillary body — navigation, filters, a detail read
- should keep the page as the subject; the panel is the aside over it
- must anchor to an edge rather than the centre

---

## Instead of

| Reach for | When |
|---|---|
| [Modal](modal.md) | the flow owns the screen and a centred panel reads as the subject |
| [BottomSheet](bottomSheet.md) | the bottom edge needs a drag handle and snap heights |
| [ActionSheet](actionSheet.md) | the bottom edge holds a list of actions and a Cancel |
| [Popover](popover.md) | the body is small and anchored to its trigger, not to an edge |

---

## Values

- must not open a bare `side="bottom"` drawer — [BottomSheet](bottomSheet.md) owns that edge
- should leave `size` at `md` — `sm:max-w-md` on a left/right panel, `max-h-[60vh]` on a top/bottom one
