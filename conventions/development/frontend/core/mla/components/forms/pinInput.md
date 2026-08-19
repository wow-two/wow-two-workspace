# PinInput

*Last updated: 2026-08-19*

> A short code, one character per box — paste-aware, and it fires once the last cell fills.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `PinInput.spec.md`.

## Reach for it when

- must collect a one-time code, a verification code, or a short PIN
- must act on `complete` rather than watching the value fill up
- should reach for it only for codes; a longer secret belongs in one box

---

## Instead of

| Reach for | When |
|---|---|
| [PasswordInput](passwordInput.md) | the secret is long and the reader may want to reveal it |
| [MaskedInput](maskedInput.md) | the value carries literals and varies in length |
| [NumberInput](numberInput.md) | the digits are a quantity, not a code |

---

## Values

- must set `length` to the code the sender issues — it defaults to `6`
- should leave `type` at `numeric` so mobile opens the digit keypad
- must set `type` to `alphanumeric` only when the issuer mixes letters in
- should leave `size` at `md`; `lg` where the boxes must be thumb-sized
- must set `isMasked` for a secret; the cells show their characters by default
