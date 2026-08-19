# ScrollReveal

*Last updated: 2026-08-19*

> Content that fades or slides in as it enters the viewport.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `ScrollReveal.spec.md`.

## Reach for it when

- must stage a long marketing page section by section
- must stay decorative — reduced motion shows the content from the start
- should wrap a whole block, not each line; per-line reveals read as a stutter

---

## Instead of

| Reach for | When |
|---|---|
| [Tilt](tilt.md) | the motion belongs to hover rather than entry |
| [CountUp](countUp.md) | the thing revealed is a number that should also count |
| `ScrollSpy` | only the section in view is needed, with nothing animated |

---

## Values

- should leave `effect` at `fade`, `duration` at `600` ms, `delay` at `0`
- should leave `threshold` at `0.1` — a taller block would otherwise never trip it
- should leave `isOnce` on; re-hiding on scroll-back makes a page feel unstable
