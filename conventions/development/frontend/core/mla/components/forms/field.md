# Field

*Last updated: 2026-08-19*

> The generic wrapper — a label, a helper and an error around any one control, and the id that ties them together.
> What a field is → [field](../../constructs/visual/field.md).
> Its full surface → `Field.spec.md`.

## Reach for it when

- must wrap any control that needs a visible label, a hint, or an error
- must reach for it inside a `form.Field` — it adopts the engine's context, never shadows it
- must not hand-wire `for`, `aria-describedby` or `aria-invalid` — the wrapper mints the id
- should leave `error` unset under the forms engine — every client and server message renders itself
- should pass `label`, `helper` and `error` as props; the same-named slots are for rich copy only

---

## Instead of

| Reach for | When |
|---|---|
| [CheckboxField](checkboxField.md) | the control is a checkbox and the label sits beside the box |
| [RadioField](radioField.md) | the control is a radio inside a [RadioGroup](radioGroup.md) |
| [SwitchField](switchField.md) | the toggle applies at once instead of on submit |
| [Fieldset](fieldset.md) + [Legend](legend.md) | several fields answer to one name |
| [Label](label.md) alone | a compact row wants the name and no helper or error slot |
| [LabeledInput](labeledInput.md) | never — it is the deprecated ancestor of this one |

---

## Values

- must not expect to set the id — `Field` takes no `id`; the provider mints or adopts one
- must leave `isRequired`, `isDisabled` and `isReadOnly` unset to inherit the context
- must read an explicit `false` on any of the three as a shadow over the parent's value
- must wrap exactly one control — a second control under one label is a [Fieldset](fieldset.md)
- must keep validation copy in the schema, never in `error` ([form](../../domains/forms/forms.md))
- must read `Field.spec.md` as stale — it is titled `FormField` and defaults the three flags to `false`
