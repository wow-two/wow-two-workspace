# CheckboxField

*Last updated: 2026-08-19*

> A checkbox and its label in one clickable `<label>` — the default for any labelled box.
> What a field is → [field](../../constructs/visual/field.md).
> Its full surface → `CheckboxField.vue`.

## Reach for it when

- must reach for it whenever a bare [Checkbox](checkbox.md) needs a visible label
- must not hand-roll the `<label>` around a checkbox — this one owns the association
- must give every item a `value` inside a [CheckboxGroup](checkboxGroup.md)
- should nest it in a [Field](field.md) only for the error and helper — the two labels would double

---

## Instead of

| Reach for | When |
|---|---|
| [Checkbox](checkbox.md) | a surrounding [Field](field.md) supplies the label |
| [CheckboxGroup](checkboxGroup.md) | several boxes share one name and one selection |
| [SwitchField](switchField.md) | the toggle applies at once instead of on submit |
| [ChoiceCard](choiceCard.md) | the option reads as a card with a title and a description |
| [Field](field.md) | the control is anything but a checkbox |

---

## Values

- must style the wrapper through `wrapperClassName` — a plain `class` lands on the box
- must set `value` inside a group and leave it unset outside, where it is ignored
- should carry the secondary line in `description`, never in a sibling paragraph
