# CharacterCount

*Last updated: 2026-08-19*

> The live `current / max` readout under a capped text control — it owns no value and edits nothing.
> A [feedback](../../constructs/visual/feedback.md) component, not a control, though the SDK ships it in `forms/`.
> Its full surface → `CharacterCount.spec.md`.

## Reach for it when

- must show how much of a hard cap a text control has spent
- must pass `value` as the current length, never the string itself
- should sit in the field's helper row, beside the error, not inside the control

---

## Instead of

| Reach for | When |
|---|---|
| [PasswordStrength](passwordStrength.md) | the measure is strength rather than length |
| `MeterBar` | the ratio reads better than the two numbers |
| [FormHelperText](formHelperText.md) | the copy is a hint and no cap is enforced |

---

## Values

- should leave `isMaxShown` on — `120 / 280` orients better than a bare count
- must pass the same `max` the control enforces; it only colours the text
- must not mount it where no cap exists — a count with no ceiling is noise
