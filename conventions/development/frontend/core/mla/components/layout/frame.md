# Frame

*Last updated: 2026-08-19*

> The bordered padded shell — a card's look without a card's slots.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Frame.spec.md`.

## Reach for it when

- must contain free-form content in a bordered, padded, rounded box
- must reach for the `muted` surface for a recessed well inside a page
- should reach for it when the shell's look is fixed at the call site

---

## Instead of

| Reach for | When |
|---|---|
| `Card` | the content splits into header, body and footer |
| [Surface](surface.md) | the fill, border and shadow recipe varies at the call site |
| [Box](box.md) | the shell carries no border, padding or radius |
| [Section](section.md) | the shell is a full-bleed band, not a contained box |

---

## Values

- must leave `padding` at `4`, `radius` at `md`, `surface` at `card`
- must pass `padding="0"` rather than a `p-0` class — that step emits no class at all
- must not take `radius` from the spec — the code adds `xl`, `2xl` and `full` too
