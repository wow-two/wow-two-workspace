# Cluster

*Last updated: 2026-08-19*

> The centred wrapping row — hero CTAs, auth-page actions, footer link groups.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Cluster.spec.md`.

## Reach for it when

- must centre a row that wraps onto more lines as it fills
- should reach for it under a heading or a hero, where a row reads as centred

---

## Instead of

| Reach for | When |
|---|---|
| [Inline](inline.md) | the row starts at the leading edge instead of the centre |
| [Stack](stack.md) | the row stays on one line and the axis may change |
| `ButtonGroup` | the buttons read as one connected control |
| `Toolbar` | the commands share one tab stop |

---

## Values

- must leave `gap` at `4` and `justify` at `center` — the centring is the reason for it
- must pick `gap` from `2`, `3`, `4`, `6`, `8` — the scale here is shorter than [Stack](stack.md)'s
- should reach for [Inline](inline.md) rather than `justify="start"`
