# Editable

*Last updated: 2026-08-19*

> Edit in place — a preview that swaps to an input on click and commits without a form around it.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `Editable.spec.md`.

## Reach for it when

- must rename a thing where it sits — a title, a board column, a table cell
- must compose the parts — `EditablePreview`, `EditableInput`, and the submit and cancel
- should reach for it where a whole form for one string would be too much

---

## Instead of

| Reach for | When |
|---|---|
| [TextInput](textInput.md) | the box is always in edit mode inside a form |
| [Field](field.md) | the value needs a label, a helper, and an error |
| `Modal` | the edit touches more than one value |

---

## Values

- should leave `canSubmitOnBlur`, `canSubmitOnEnter` and `canCancelOnEscape` on
- must keep all three on together — they are the in-place contract readers expect
- must bind `isEditing` or `editing`, never both — `isEditing` wins on collision
- must replace the `Click to edit` placeholder with the value's own noun
