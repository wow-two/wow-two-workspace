# Eyebrow

*Last updated: 2026-08-19*

> The tiny uppercase kicker over a block — the lightest label in the group.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Eyebrow.vue`.

## Reach for it when

- must label a block inside a drawer or card — `FULL TEXT`, `SEGMENTS`
- must stay lighter than a titled header; it carries a word, not a sentence
- should keep the uppercase and tracking treatment the component already applies

---

## Instead of

| Reach for | When |
|---|---|
| [SectionHeader](sectionHeader.md) | the block wants a title, a description and actions |
| [Heading](heading.md) | the label is the section's real outline entry |
| [Badge](badge.md) | the word classifies a thing rather than labelling a region |

---

## Values

- should leave `level` at `3` — it is an outline level, not a size step
- should leave `tone` at `muted`; the kicker never competes with the block
