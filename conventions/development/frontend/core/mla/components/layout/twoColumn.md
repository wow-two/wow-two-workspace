# TwoColumn

*Last updated: 2026-08-19*

> The aside-and-main pair — a fixed-width rail beside a column that takes the rest.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `TwoColumn.spec.md`.

## Reach for it when

- must fix one column's width and let the other take what is left
- must fill the `aside` slot — it is required, and the default slot is the main column
- should reach for it for filters beside results, or an outline beside an article

---

## Instead of

| Reach for | When |
|---|---|
| [AppShell](appShell.md) | the frame also owns a header, a footer and a collapse |
| [Grid](grid.md) | both columns are tracks of one equal set |
| [ResizablePanels](resizablePanels.md) | the reader drags the split between the two |
| [Stack](stack.md) | the two columns stack instead of sitting side by side |

---

## Values

- must pass `asideWidth` as a Tailwind width class — `w-72`, never a raw length
- must leave `asideWidth` at `w-64`, `asideSide` at `left`, `gap` at `6`
- must pick `gap` from `0`, `4`, `6`, `8`, `10` — the scale here is its own
- must not mount it in [AppShell](appShell.md)'s main region — it renders its own `main`
