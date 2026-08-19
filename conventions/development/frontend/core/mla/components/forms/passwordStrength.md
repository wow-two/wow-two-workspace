# PasswordStrength

*Last updated: 2026-08-19*

> The strength meter under a new-password box — it reads the value and sets nothing.
> A [feedback](../../constructs/visual/feedback.md) component, not a control, though the SDK ships it in `forms/`.
> Its full surface → `PasswordStrength.spec.md`.

## Reach for it when

- must show how strong a secret is while it is being created or reset
- must sit under a [PasswordInput](passwordInput.md), never replace it
- should reach for it only where the reader can act on the reading

---

## Instead of

| Reach for | When |
|---|---|
| [CharacterCount](characterCount.md) | the constraint is a length cap rather than strength |
| `MeterBar` | the ratio is generic and carries no password rules |
| [FormErrorMessage](formErrorMessage.md) | the password failed a rule and must be rewritten |

---

## Values

- must pass `score` when the app scores the password itself — the built-in heuristic is a fallback
- must keep `score` inside `0`–`4`; nothing outside that range renders
- should leave `isLabelHidden` off — the band name carries the meaning, not the colour
- must not mount it on a sign-in field; strength only matters where a secret is chosen
