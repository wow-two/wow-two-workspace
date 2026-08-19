# FontPicker

*Last updated: 2026-08-19*

> The font-family choice, where every row is drawn in the face it offers.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `FontPicker.spec.md`.

## Reach for it when

- must choose a typeface, where seeing the face is the whole decision
- must store a CSS family stack the surface can apply directly
- should reach for it in an editor, a theme panel, or a document's style controls

---

## Instead of

| Reach for | When |
|---|---|
| [Select](select.md) | the options are words and the preview buys nothing |
| [Combobox](combobox.md) | the list is long enough to need typeahead filtering |
| [IconPicker](iconPicker.md) | the choice is a glyph rather than a face |
| [GradientPicker](gradientPicker.md) | the choice is a fill rather than a typeface |

---

## Values

- must speak the CSS family stack, not the display name — `Helvetica, Arial, sans-serif`
- should leave `fonts` at the built-in thirteen; pass a set only for a real brand list
- must expect the first entry's family when uncontrolled
- should leave `previewText` at `The quick brown fox` and `placeholder` at `Select font…`
- must set `name` for a plain form post; the hidden input carries the family
