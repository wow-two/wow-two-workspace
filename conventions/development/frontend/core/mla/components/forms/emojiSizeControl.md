# EmojiSizeControl

*Last updated: 2026-08-19*

> The three size presets for a chosen emoji, each tile previewing the real glyph rather than naming a number.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `EmojiSizeControl.spec.md`.

## Reach for it when

- must scale a glyph the reader already picked — [EmojiPicker](emojiPicker.md) chose it, this sizes it
- must show the choice as the glyph itself, since a ratio means nothing on its own
- should reach for it wherever an emoji is placed on a surface at a chosen scale

---

## Instead of

| Reach for | When |
|---|---|
| [EmojiPicker](emojiPicker.md) | the choice is which emoji, not how big |
| [Slider](slider.md) | the scale is continuous rather than three presets |
| `OptionTileGroup` | the options need a title and a description each |
| `SegmentedControl` | the options are words with nothing to preview |

---

## Values

- must supply `glyph` — the tiles preview it, so an empty one previews nothing
- must speak a ratio of the host's width — `0.18`, `0.25`, `0.32`, small through large
- must expect `0.25` to apply when no ratio is set
- must drive it controlled — it keeps no state of its own
- should leave `maxPreviewGlyph` at `24` px, the cap that stops a glyph clipping its tile
- must leave `size` unset for the tile default — the spec claims `sm`, the code sets none
