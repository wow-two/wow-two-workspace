# Popover

*Last updated: 2026-08-19*

> The click-anchored panel — positioned on its trigger, focus-trapped, and it never dims the page.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).
> Its full surface → `Popover.spec.md`.

## Reach for it when

- must hold content belonging to one trigger — a picker, a share menu, a mini form
- should sit beside the page rather than blocking it
- must be operable by keyboard; focus enters the panel and returns to the trigger

---

## Instead of

| Reach for | When |
|---|---|
| [HoverCard](hoverCard.md) | the panel is a hover preview with nothing to operate |
| [Modal](modal.md) | the flow must block the page until it resolves |
| `Tooltip` | the content is one short label rather than a panel |
| `DropdownMenu` | the panel is a list of commands with roving focus |

---

## Values

- should leave `placement` at `bottom` and `offset` at `8` — the house anchor pair
- must not add a scrim — a popover that dims the page is a [Modal](modal.md)
