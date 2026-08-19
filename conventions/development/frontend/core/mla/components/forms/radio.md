# Radio

*Last updated: 2026-08-19*

> One dot of a mutually exclusive set — it means nothing outside the group that names it.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `Radio.spec.md`.

## Reach for it when

- must offer one option of a set where exactly one may hold
- must sit inside a [RadioGroup](radioGroup.md) — the group owns `name` and the selection
- should reach for [RadioField](radioField.md) when the dot needs a label beside it

---

## Instead of

| Reach for | When |
|---|---|
| [Checkbox](checkbox.md) | each option is independent and several may hold |
| [ChoiceCard](choiceCard.md) | the option needs a description or an icon to be picked |
| `SegmentedControl` | the options are short and belong in one strip |
| [Select](select.md) | the set is long enough that laying it out costs the screen |

---

## Values

- should leave `size` at `md`; `lg` for a standalone dot with a thumb target
- must bind `checked` or `modelValue`, never both — `checked` wins on collision
- must leave `disabled` and `required` unset to inherit the group's context
- must not mount a lone radio — one dot the reader cannot unset is a trap
