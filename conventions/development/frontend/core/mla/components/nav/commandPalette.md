# CommandPalette

*Last updated: 2026-08-19*

> The ⌘K palette — actions found by typing rather than by looking.
> What a nav component is → [nav](../../constructs/visual/nav.md).
> Its full surface → `CommandPalette.spec.md`.

## Reach for it when

- must expose more actions than a menu can list without scrolling
- must reach an action by name from anywhere in the app
- should bind the global chord, so the palette needs no visible trigger

---

## Instead of

| Reach for | When |
|---|---|
| [DropdownMenu](dropdownMenu.md) | the list is short and fixed enough to read at a glance |
| [Menubar](menubar.md) | the commands belong to named groups the reader browses |
| `Combobox` (forms) | the reader picks a value to keep, not an action to run |

---

## Values

- must set `search-text` when the label differs from `value`; the filter reads `value`
- must pass `trigger-key` to bind the global chord; omitting it binds none
- should keep `close-on-select` on, so the palette closes on the action it ran
