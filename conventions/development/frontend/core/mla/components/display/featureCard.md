# FeatureCard

*Last updated: 2026-08-19*

> The marketing feature tile — tinted icon badge, title, one supporting line.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `FeatureCard.vue`.

## Reach for it when

- must fill a landing page's feature grid, one capability per tile
- must stay content-only; the tile bakes in no routing and no call to action
- should carry the icon in its slot and leave the title a scalar prop

---

## Instead of

| Reach for | When |
|---|---|
| [StepCard](stepCard.md) | the tiles are an ordered sequence with visible numbers |
| [PricingCard](pricingCard.md) | the tile sells a plan and ends in a call to action |
| [Card](card.md) | the box is app content rather than a marketing tile |

---

## Values

- must pass `description` or fill the default slot; the body needs one
- must keep the copy to a line or two; the tile is a grid member, not a page
