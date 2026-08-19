# ColorSlider

*Last updated: 2026-08-19*

> The single-channel track — hue, saturation, value or alpha, drawn as its own gradient.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `ColorSlider.spec.md`.

## Reach for it when

- must edit exactly one channel, with the gradient showing what the channel does
- must stack several tracks to build a panel by hand — one per channel
- should reach for it for alpha; nothing else in the folder edits opacity alone

---

## Instead of

| Reach for | When |
|---|---|
| [ColorPicker](colorPicker.md) | the whole colour is being picked and the panel is not bespoke |
| [ColorWheel](colorWheel.md) | hue reads better as a ring than a strip |
| [ColorArea](colorArea.md) | saturation and value move together |
| [Slider](slider.md) | the number is not a colour channel and needs no gradient |

---

## Values

- must set `channel` — it defaults to `hue`, which is rarely the one meant
- must pass `color` for the saturation, value and alpha tracks; hue ignores it
- must read the range off the channel — hue `0`–`360`, every other one `0`–`1`
- should leave `step` unset — it resolves to `1` for hue and `0.01` elsewhere
- must expect `0` when uncontrolled — a bare alpha track opens fully transparent
