# PhoneInput

*Last updated: 2026-08-19*

> A phone number with its country — a dial-code select beside the national number, emitting E.164.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `PhoneInput.spec.md`.

## Reach for it when

- must collect a number that will be dialled or texted, not merely stored
- must accept the value is E.164-shaped — `+<country><number>`, one string
- must accept it is first-generation: a hand-curated country list, no full parsing

---

## Instead of

| Reach for | When |
|---|---|
| [TelInput](telInput.md) | the number is local and no country code is needed |
| [MaskedInput](maskedInput.md) | the format is fixed to one country and never varies |
| [TextInput](textInput.md) | the field is an extension or a short internal code |

---

## Values

- must set `defaultCountry` from the reader's locale — it ships `US`, and is never derived
- must rewrite the `(555) 555-5555` placeholder when `defaultCountry` is not `US`
- must validate on the server; the country list formats but does not check the number
