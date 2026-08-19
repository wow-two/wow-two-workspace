# OptionTile

*Last updated: 2026-08-19*

> An icon-only square tile for a preset grid — fill types, module shapes, gradient presets.
> What an action is → [action](../../constructs/visual/action.md).
> Its full surface → `OptionTile.vue`.

## Reach for it when

- must reach for it when the option reads as a glyph or swatch, not a word
- must mount it inside an [OptionTileGroup](optionTileGroup.md) — it carries name and disabled state
- should keep the active value on the parent; the tile takes `selected`

---

## Instead of

| Reach for | When |
|---|---|
| [ToggleButton](toggleButton.md) | the option carries a visible word label |
| [ToggleButtonGroup](toggleButtonGroup.md) | the strip itself should own the selected value |
| [Button](button.md) | picking the option runs a command instead of leaving a selection |

---

## Values

- must set `label` — the icon-only tile has no other accessible name
- should keep `size="sm"` and `tone="primary"`, the shipped defaults
