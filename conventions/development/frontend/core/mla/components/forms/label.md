# Label

*Last updated: 2026-08-19*

> The `<label>` element — one control's accessible name, for a control placed without a [Field](field.md).
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Label.spec.md`.

## Reach for it when

- must reach for it when a control stands without a [Field](field.md) around it
- must not add one inside a [Field](field.md) — the wrapper renders its own from `label`
- must not hand-roll a `<label>` element; only this one registers with the control context
- should let a surrounding context fill `for` and `id` — both auto-wire

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) | the control also needs a helper, an error, or the invalid state |
| [Legend](legend.md) | the copy names a whole [Fieldset](fieldset.md), not one control |
| [FormHelperText](formHelperText.md) | the copy describes the input rather than naming it |
| `SectionHeader` | the copy titles a region, and no control answers to it |

---

## Values

- must set `htmlFor` when no form-control context surrounds it — nothing else fills it
- must set one of `for` or `htmlFor`, never both — `for` wins when they disagree
- must not set `id` unless detaching the label; it then stops naming the control
- should leave `isRequired` unset — it falls back to the context's own flag
- should leave `size` at `md` — only `xs` renders differently, `sm` matches it, `lg` and `xl` fall back
- must read `Label.spec.md` as stale — the Vue prop is `isRequired`, not `required`
