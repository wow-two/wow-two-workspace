# PasswordInput

*Last updated: 2026-08-19*

> A masked secret with a reveal toggle — the only control that hides what it holds.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `PasswordInput.spec.md`.

## Reach for it when

- must collect a secret the reader types — a password, a token, an API key
- must let the reader reveal it; the toggle ships on and mistyping is the failure mode
- should pair it with [PasswordStrength](passwordStrength.md) on a create or reset flow

---

## Instead of

| Reach for | When |
|---|---|
| [TextInput](textInput.md) | the value is not secret and needs no masking |
| [PinInput](pinInput.md) | the secret is a short code entered one character per box |
| `Snippet` | the secret is shown to be copied, not typed |

---

## Values

- must set `autocomplete` per flow — `current-password` to sign in, `new-password` to create
- must not leave `autocomplete` unset; nothing is inferred and the manager guesses wrong
- should leave `hasToggle` on — hide it only where shoulder-surfing is the stated threat
- should leave `size` at `md`, `state` unset — the field's invalid flag drives it
