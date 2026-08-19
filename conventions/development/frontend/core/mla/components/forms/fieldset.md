# Fieldset

*Last updated: 2026-08-19*

> The native `<fieldset>` — several fields grouped under one [Legend](legend.md).
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Fieldset.spec.md`.

## Reach for it when

- must reach for it when two or more fields answer to one name — an address, a date range
- must pair it with a [Legend](legend.md); an unnamed group is a `Box`
- must reach for it to disable a whole group at once — native `disabled` cascades
- should not wrap a single field; one [Field](field.md) already names its control

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) | one control takes the name, the helper and the error |
| [RadioGroup](radioGroup.md) | the group is a mutex set and owns the selected value |
| [CheckboxGroup](checkboxGroup.md) | the group owns a set of selected keys |
| `Stack` | the grouping is spacing only and names nothing |

---

## Values

- must set `disabled`, `name` and `form` as native attributes — every one falls through
- must not expect a border or padding; the SDK strips both to zero
