# Heading

*Last updated: 2026-08-19*

> The outline entry — its semantic level and its visual size are chosen separately.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Heading.spec.md`.

## Reach for it when

- must title a page, a section, a card, or a panel body
- must take the outline level from the document tree, never from the wanted size
- should carry a [Text](text.md) description line under it when one is needed

---

## Instead of

| Reach for | When |
|---|---|
| [SectionHeader](sectionHeader.md) | the title arrives with a description and an actions row |
| [Eyebrow](eyebrow.md) | the label is a tiny uppercase kicker above a block |
| [Text](text.md) | the line is body copy and holds no outline position |
| [GradientText](gradientText.md) | the words are a decorative display line, not an outline entry |

---

## Values

- must set `level` from the outline — `2` is the default, a page's own title is `1`
- must fix a wrong visual scale through `size`, never by moving `level`
- should leave `size` at `lg` and `weight` at `semibold`
