# Breadcrumb

*Last updated: 2026-08-19*

> The trail of ancestors above the page the reader is on.
> What a nav component is → [nav](../../constructs/visual/nav.md).
> Its full surface → `Breadcrumb.spec.md`.

## Reach for it when

- must place the current page inside a hierarchy the reader can climb
- must name every ancestor between the root and the page as its own entry
- should carry a trail short enough to sit on one line

---

## Instead of

| Reach for | When |
|---|---|
| [TableOfContents](tableOfContents.md) | the position is a section inside one page, not a page in a tree |
| [Pagination](pagination.md) | the neighbours are an ordered sequence, not ancestors |
| [NavItem](navItem.md) | the destination stands in a sidebar instead of tracking the page |

---

## Values

- must order `items` root first and the current page last
- must not rely on the last entry's `href` — it renders as text, never a link
- should keep the default chevron separator — an override applies to every gap
