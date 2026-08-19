# PercentInput

*Last updated: 2026-08-19*

> A rate — a [NumberInput](numberInput.md) with a trailing `%` pinned inside the box.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `PercentInput.spec.md`.

## Reach for it when

- must collect a rate the reader thinks of in percent — a discount, a tax, a share
- must accept the bound value is the bare number, read as `0`–`100`
- should reach for every [NumberInput](numberInput.md) prop — this one adds none of its own

---

## Instead of

| Reach for | When |
|---|---|
| [NumberInput](numberInput.md) | the number is a count and the suffix would mislead |
| [CurrencyInput](currencyInput.md) | the value is an amount rather than a rate |
| [Slider](slider.md) | the reader sweeps the rate instead of typing it |
| [Knob](knob.md) | the rate is a live parameter in a control panel |

---

## Values

- must divide by `100` before storing a fraction — nothing converts the value here
- must set `min` `0` and `max` `100` where the rate cannot exceed the whole
- should set `step` to `0.1` or finer where whole points are too coarse
