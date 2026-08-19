# GradientPicker

*Last updated: 2026-08-19*

> The gradient editor — geometry, angle, and a stop list the reader adds to and removes from.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `GradientPicker.spec.md`.

## Reach for it when

- must edit a fill made of several colours rather than one
- must keep the geometry editable — linear, radial, conic — not just the stops
- should reach for it for a theme background, a hero fill, a chart ramp

---

## Instead of

| Reach for | When |
|---|---|
| [ColorPicker](colorPicker.md) | the fill is one flat colour |
| [ColorSwatchPicker](colorSwatchPicker.md) | the fill comes off a fixed palette |
| [ColorSlider](colorSlider.md) | one channel of one colour is being edited |

---

## Values

- must speak a `Gradient` object — `kind`, `angle`, and a `stops` array
- must give each stop a `color` and a `position` in percent, `0`–`100`
- must expect a 90° linear ramp when uncontrolled — `#3b82f6` to `#a855f7`
- must expect `angle` to be ignored on a radial gradient; linear and conic honour it
- must set `name` for a plain form post — the hidden input carries the CSS string
