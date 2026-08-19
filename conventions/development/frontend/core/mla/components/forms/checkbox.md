# Checkbox

*Last updated: 2026-08-19*

> One independent boolean the form submits — the default box for opt-ins, flags, and row selection.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `Checkbox.spec.md`.

## Reach for it when

- must carry a boolean that takes effect on submit, not on click
- must set `isIndeterminate` on a parent whose children are partly checked
- should reach for [CheckboxField](checkboxField.md) when the box needs a label

---

## Instead of

| Reach for | When |
|---|---|
| [Switch](switch.md) | the toggle applies at once and nothing is submitted |
| [CheckboxGroup](checkboxGroup.md) | several boxes share one value array under a legend |
| [Radio](radio.md) | exactly one of a set may be chosen |
| `ToggleButton` | the state is a toolbar mode, not a form value |

---

## Values

- should leave `size` at `md`, `variant` at `solid`, `tone` at `primary`
- must size `lg` or larger standalone — `md` is 20 px, under the 24 px target
- must bind `checked` or `modelValue`, never both — `checked` wins on collision
- must not pass `defaultChecked` beside a bound value; it is the uncontrolled seed
- must leave `disabled` and `required` unset to inherit the field's context
