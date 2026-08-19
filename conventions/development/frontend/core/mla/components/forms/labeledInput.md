# LabeledInput

*Last updated: 2026-08-19*

> The pre-[Field](field.md) wrapper — deprecated, and kept for one release only.
> What a field is → [field](../../constructs/visual/field.md).
> Its full surface → `LabeledInput.vue`.

## Reach for it when

- must not reach for it in new code — [Field](field.md) replaced it
- should keep it only at a call site already binding its scoped `id`

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) | always — label, helper, error and the control context in one |
| [Label](label.md) + a control | the row wants a name only, and no wrapper at all |

---

## Values

- must bind the default slot's scoped `id` onto the control — nothing else wires it
- must not expect a helper, an error, or the form-control context; it provides none
- should carry the inline-end note in `trailing` — an `Optional` marker, a count
