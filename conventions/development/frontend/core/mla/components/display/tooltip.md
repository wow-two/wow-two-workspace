# Tooltip

*Last updated: 2026-08-19*

> One short label on hover or focus — the smallest thing that floats.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Tooltip.spec.md`.

## Reach for it when

- must name an icon-only control, or expand a truncated label
- must carry text only; it takes no focus and holds nothing operable
- should stay optional — the app must work for a reader who never hovers

---

## Instead of

| Reach for | When |
|---|---|
| `HoverCard` | the hover previews a card of content rather than a label |
| `Popover` | the panel holds a control the reader must reach |
| [KeyboardShortcut](keyboardShortcut.md) | the label is only the accelerator for a command |

---

## Values

- should leave `openDelay` at `700` ms and `closeDelay` at `0` — the OS pattern
- should leave `placement` at `top`
- must set `isDisabled` on empty content rather than passing an empty string
- must bind either `open` or `isOpen`, never both — `open` wins when they collide
