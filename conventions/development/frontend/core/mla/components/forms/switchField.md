# SwitchField

*Last updated: 2026-08-19*

> A switch and its label in one clickable `<label>` — the settings row that takes effect on the flip.
> What a field is → [field](../../constructs/visual/field.md).
> Its full surface → `SwitchField.vue`.

## Reach for it when

- must reach for it when the toggle applies at once, with no submit behind it
- must reach for it whenever a bare [Switch](switch.md) needs a visible label
- should set `side="right"` for a settings row — label leading, switch trailing

---

## Instead of

| Reach for | When |
|---|---|
| [Switch](switch.md) | a surrounding [Field](field.md) supplies the label |
| [CheckboxField](checkboxField.md) | the value is posted with a form rather than applied at once |
| `ToggleButton` | the press is a toolbar mode, not a stored setting |

---

## Values

- must set `side` to `left` or `right` — the type takes all four, `top` and `bottom` render as `left`
- must style the wrapper through `wrapperClassName` — a plain `class` lands on the switch
- should carry the secondary line in `description`, never in a sibling paragraph
