# Grid

*Last updated: 2026-08-19*

> The two-axis container — equal tracks and one gap, optionally per breakpoint.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Grid.spec.md`.

## Reach for it when

- must align items across rows as well as down columns
- must change the track count at a breakpoint, through the responsive map
- should keep the tracks equal — an uneven split is an explicit `gridTemplateColumns`

---

## Instead of

| Reach for | When |
|---|---|
| [Stack](stack.md) | the children run down one axis only |
| [TwoColumn](twoColumn.md) | one column is a fixed-width aside and the other flexes |
| [Inline](inline.md) | the items wrap freely and need no column alignment |
| [ResizablePanels](resizablePanels.md) | the reader drags the split between the tracks |

---

## Values

- must leave `columns` at `2` and `gap` at `4` for the ordinary case
- must pick `columns` from `1`–`6`, `8`, `12` — no other track count ships
- must pass a `{ base, sm, md, lg, xl }` map for a per-breakpoint value
- should set an explicit `gridTemplateColumns` style for non-uniform tracks
