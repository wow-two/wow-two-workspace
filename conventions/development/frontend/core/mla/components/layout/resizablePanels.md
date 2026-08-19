# ResizablePanels

*Last updated: 2026-08-19*

> The draggable split — two or more panes the reader resizes by dragging between them.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `ResizablePanels.spec.md`.

## Reach for it when

- must let the reader set the split, rather than the layout fixing it
- must compose panels and separators as children, alternating
- should reach for it for an editor beside its preview, or a tree beside a document

---

## Instead of

| Reach for | When |
|---|---|
| [TwoColumn](twoColumn.md) | the aside width is fixed and the reader never moves it |
| [Grid](grid.md) | the tracks are equal and the layout owns them |
| `Drawer` | the second pane opens and closes over the first |
| [ScrollArea](scrollArea.md) | the panes never resize and only one of them scrolls |

---

## Values

- must seed unequal panes with `defaultSizes` on the group — percentages, one per panel
- must not seed with a panel's `defaultSize` — it only drives the double-click reset
- must set `minSize` on each panel — it defaults to `0`, so a pane can vanish
- must place `n - 1` separators between `n` panels, in child order
- must not name them `ResizablePanels.Panel` — the spec is React-era; they ship flat
