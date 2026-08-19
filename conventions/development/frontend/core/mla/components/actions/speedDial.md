# SpeedDial

*Last updated: 2026-08-19*

> A Fab that fans out into a small stack of secondary commands.
> What an action is → [action](../../constructs/visual/action.md).
> Its full surface → `SpeedDial.spec.md`.

## Reach for it when

- must reach for it when one floating anchor has to offer several commands
- must reach for it only with two or more actions — a single one is a [Fab](fab.md)
- should let it replace the screen's [Fab](fab.md) rather than sit beside one

---

## Instead of

| Reach for | When |
|---|---|
| [Fab](fab.md) | the anchor runs exactly one command |
| [Toolbar](toolbar.md) | the commands belong in the content flow, as a strip |
| `ActionSheet` | the choices take the full width of a mobile sheet → [overlay](../../constructs/visual/overlay.md) |

---

## Values

- must give every action an `aria-label` — each one is icon-only
- must name the trigger where the default `Toggle actions` is wrong for the locale
- should keep `gap` at `12` px, and let `direction` derive from `position`
