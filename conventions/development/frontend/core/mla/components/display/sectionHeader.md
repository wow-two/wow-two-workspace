# SectionHeader

*Last updated: 2026-08-19*

> The section's whole header — title, description, and an actions row in one.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `SectionHeader.spec.md`.

## Reach for it when

- must open a section or a page with a title plus supporting copy
- must sit a control beside the title — a filter, a create button, a view switch
- should let it own the rule under the header rather than adding a separator

---

## Instead of

| Reach for | When |
|---|---|
| [Heading](heading.md) | the title stands alone, with no description and no actions |
| [Eyebrow](eyebrow.md) | the label is a tiny uppercase kicker rather than a header |
| [MetaInline](metaInline.md) | the row carries meta chips, not a title |
| [Card](card.md) | the header belongs to a bordered box and its own body |

---

## Values

- should leave `level` at `2` and `size` at `lg` for a section inside a page
- must lower `level` for a nested section — the size stays independent
- should leave `isBordered` on; drop it only when a surface already draws the rule
