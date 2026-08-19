# IconPicker

*Last updated: 2026-08-19*

> The searchable icon grid — it commits a key the product stores, never the component behind it.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `IconPicker.spec.md`.

## Reach for it when

- must let a reader mark something with a UI icon — a project, a category, a shortcut
- must store a stable key that survives an icon set being swapped underneath it
- should reach for it where the set is small enough to scan and search covers the rest

---

## Instead of

| Reach for | When |
|---|---|
| [EmojiPicker](emojiPicker.md) | the glyphs are emoji, and the catalogue is the whole point |
| [ColorSwatchPicker](colorSwatchPicker.md) | the grid holds colours rather than glyphs |
| [FontPicker](fontPicker.md) | the choice is a typeface |
| [Select](select.md) | the options read better as labels than as a grid |

---

## Values

- must speak the icon key, never the icon component — `bell`, `chevron-down`, `cart`
- should leave `icons` at the built-in lucide subset; pass a set to widen or narrow it
- should leave `columns` at `8`, `size` at `20` px, `iconButtonSize` at `36` px
- should leave `placeholder` at `Search icons…`
- must set `name` for a plain form post; the hidden input carries the key
