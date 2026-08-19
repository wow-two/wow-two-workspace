# CurrencyInput

*Last updated: 2026-08-19*

> An amount of money — a [NumberInput](numberInput.md) with a leading symbol pinned inside the box.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `CurrencyInput.spec.md`.

## Reach for it when

- must collect a price, a balance, a limit — anything denominated
- must keep the bound value a bare number; the symbol is decoration only
- should reach for every [NumberInput](numberInput.md) prop — they pass straight through

---

## Instead of

| Reach for | When |
|---|---|
| [NumberInput](numberInput.md) | the number is a quantity rather than money |
| [PercentInput](percentInput.md) | the number is a rate and the suffix is `%` |
| [MaskedInput](maskedInput.md) | the format is rigid and the value is a string |

---

## Values

- must set `symbol` per currency — it defaults to `$` and is never derived
- should set `step` to the minor unit, `0.01`, over the inherited `1`
- must set `min` to `0` where a negative amount is meaningless
