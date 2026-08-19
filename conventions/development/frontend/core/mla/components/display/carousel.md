# Carousel

*Last updated: 2026-08-19*

> A slide track the reader steps through — the root owns the index.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Carousel.spec.md`.

## Reach for it when

- must step through peers in order — screenshots, testimonials, onboarding cards
- must compose the sibling parts — `CarouselViewport` through `CarouselDot`
- should keep every slide worth reaching; a slide behind an arrow is rarely seen

---

## Instead of

| Reach for | When |
|---|---|
| [Tabs](tabs.md) | the panels are named alternatives rather than an ordered run |
| [Marquee](marquee.md) | the strip scrolls itself and is never stepped |
| [List](list.md) | every item should be visible at once |

---

## Values

- should leave `defaultIndex` at `0` and `canLoop` off
- must set `autoPlay` in ms only for decorative strips — it is off by default
- must set `slidesCount` when the slides are virtualised; the count cannot be derived
