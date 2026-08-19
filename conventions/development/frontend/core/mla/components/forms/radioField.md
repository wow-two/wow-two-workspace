# RadioField

*Last updated: 2026-08-19*

> A radio and its label in one clickable `<label>` — one option of a mutex set.
> What a field is → [field](../../constructs/visual/field.md).
> Its full surface → `RadioField.vue`.

## Reach for it when

- must reach for it whenever a bare [Radio](radio.md) needs a visible label
- must mount it inside a [RadioGroup](radioGroup.md) for a mutex set — the group supplies `name`
- must give every item a `value` inside a group; the group tracks selection by it
- should reach for a standalone one only where a `name` is set by hand

---

## Instead of

| Reach for | When |
|---|---|
| [Radio](radio.md) | a surrounding [Field](field.md) supplies the label |
| [RadioGroup](radioGroup.md) | the group itself should own the selected value |
| [ChoiceCard](choiceCard.md) | the option reads as a card with a title and a description |
| [CheckboxField](checkboxField.md) | the options are not mutually exclusive |
| `ToggleButtonGroup` | the choice switches a mode instead of posting a value |

---

## Values

- must style the wrapper through `wrapperClassName` — a plain `class` lands on the radio
- must not set `name` inside a group — the group's shared name drives arrow-key roving
- should carry the secondary line in `description`, never in a sibling paragraph
