# Section

*Last updated: 2026-08-19*

> The full-bleed band — a tinted or padded strip with a centred column inside it.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Section.spec.md`.

## Reach for it when

- must break a page into bands, each with its own vertical rhythm
- must tint the band behind a centred column
- should reach for it where a [Container](container.md) alone leaves the band bare

---

## Instead of

| Reach for | When |
|---|---|
| [Container](container.md) | only the width cap is wanted, with no band behind it |
| [Navbar](navbar.md) | the band is a header bar with a start, centre and end |
| [Frame](frame.md) | the box is contained rather than edge to edge |
| [Surface](surface.md) | the recipe wraps content that is not a page band |

---

## Values

- must leave `py` at `md` and `containerSize` at `lg`
- must not nest a [Container](container.md) inside it — it mounts one already
- must pass `bleed` for edge-to-edge content; the inner container drops then
- should leave `tone` unset for a transparent band — a tone applies the `subtle` fill
