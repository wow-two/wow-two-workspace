# ColorArea

*Last updated: 2026-08-19*

> The saturation / value square — two axes at once, tinted by a hue it is given rather than one it owns.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `ColorArea.spec.md`.

## Reach for it when

- must edit saturation and brightness together, in one pointer drag
- must expect the hue to arrive from a sibling — the square never picks one
- should reach for it only inside a hand-built panel; [ColorPicker](colorPicker.md) already holds one

---

## Instead of

| Reach for | When |
|---|---|
| [ColorPicker](colorPicker.md) | the whole colour is being picked, panel and trigger included |
| [ColorWheel](colorWheel.md) | the axis being edited is hue, on a ring |
| [ColorSlider](colorSlider.md) | one channel is edited on a strip, hue included |
| [ColorSwatchPicker](colorSwatchPicker.md) | the palette is fixed and the axes never move |

---

## Values

- must drive `hue` from a sibling — it defaults to `0`, so the square opens red
- must bind both halves, `v-model:saturation` and `v-model:value`; each is `0`–`1`
- should read `@value-change` instead when both axes are stored together
- should leave `step` at `0.01`; `PageUp` / `PageDown` already move ten of them
- must expect `1` for both axes when uncontrolled — the square opens at full colour
- should let a wrapping field name it; an explicit `aria-label` wins over that
