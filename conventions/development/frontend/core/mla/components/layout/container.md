# Container

*Last updated: 2026-08-19*

> The centred column — a max width and a horizontal padding around page content.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Container.spec.md`.

## Reach for it when

- must cap a page's reading width and centre what is left
- must sit near the page root, above the content that fills it
- must not nest one in a [Section](section.md) or [Navbar](navbar.md) — each mounts its own

---

## Instead of

| Reach for | When |
|---|---|
| [Section](section.md) | the band behind the column is tinted or padded too |
| [Navbar](navbar.md) | the centred row is a header bar |
| [Box](box.md) | the width comes from a class rather than a preset |

---

## Values

- must leave `size` at `lg` unless the content genuinely reads wider
- should reach for `size="full"` when the cap goes but the padding stays
