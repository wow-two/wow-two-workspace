# RadioGroup

*Last updated: 2026-08-19*

> Exactly one from a short fixed set, every option visible at once under one legend.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `RadioGroup.spec.md`.

## Reach for it when

- must pick one value from a set short enough to show whole
- must own the items' `name` and selection — the children read it by injection
- should carry `legend`; it is the group's label and its `fieldset` needs one

---

## Instead of

| Reach for | When |
|---|---|
| [CheckboxGroup](checkboxGroup.md) | more than one option may hold at a time |
| [Select](select.md) | the set is long enough that showing it whole costs the screen |
| `SegmentedControl` | the choices are short and read better as one strip |
| [Listbox](listbox.md) | the options scroll in place with arrow-key movement |

---

## Values

- should leave `orientation` at `vertical` — the readable default for labels
- must set `horizontal` only for two or three short options
- must accept `null` as the empty selection; the group starts unselected
- must cascade `isDisabled` from the group, never repeat it per item
- should hold [ChoiceCard](choiceCard.md) items when each option needs explaining
