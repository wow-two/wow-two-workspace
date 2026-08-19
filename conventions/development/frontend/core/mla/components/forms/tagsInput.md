# TagsInput

*Last updated: 2026-08-19*

> Free-form labels typed in — each commit turns into a removable chip inside the box.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `TagsInput.spec.md`.

## Reach for it when

- must collect values the reader invents — labels, keywords, recipients
- must accept the value is a string array, in entry order
- should reach for it when no option list could be complete in advance

---

## Instead of

| Reach for | When |
|---|---|
| [MultiSelect](multiSelect.md) | the values come from a known set the reader picks from |
| [Combobox](combobox.md) | the reader types to narrow a list and picks exactly one |
| [CheckboxGroup](checkboxGroup.md) | the set is short, fixed, and better shown unfolded |
| `Tag` | the chips are rendered read-only |

---

## Values

- should leave `delimiters` at `[',']` — Enter and Tab already commit alongside it
- must pass `validate` for anything beyond non-empty; the default only trims
- must set `max` where the list has a cap; nothing is bounded by default
- should leave `allowsDuplicates` off — a repeated tag is almost always a mistype
- should leave `tagVariant` at `neutral`; a tone here competes with the field's own state
