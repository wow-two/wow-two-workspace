# Slider

*Last updated: 2026-08-19*

> A value swept along a track — the native range input, where the position carries the meaning.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `Slider.spec.md`.

## Reach for it when

- must set an approximate value where the range matters more than the digits
- must accept it is single-thumb; a two-ended range is not this control
- should reach for it where the reader adjusts and watches the effect live

---

## Instead of

| Reach for | When |
|---|---|
| [NumberInput](numberInput.md) | the reader needs to type an exact value |
| [Knob](knob.md) | the parameter sits in a dense panel and rotation reads as the gesture |
| [PercentInput](percentInput.md) | the rate is typed and the track would add nothing |
| `ProgressBar` | the bar reports work rather than takes a value |

---

## Values

- should leave `min` `0` and `max` `100` — the percentage range the default assumes
- must pass `step` as a native attribute; it falls through to the range input
- should leave `size` at `md`; the sizes only set the track's thickness
- must show the value beside it — the track alone gives the reader no number
