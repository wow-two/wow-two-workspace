# ControlGroup

*Last updated: 2026-08-19*

> The labelled control row — a muted label bound to the control beside or above it.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its surface → `ControlGroup.vue`; no spec ships.

## Reach for it when

- must bind a muted label to a control in a settings or preferences list
- must stack such rows and have the hairlines fall between them
- should reach for it outside a form — a validated input is a form field

---

## Instead of

| Reach for | When |
|---|---|
| `Field` | the control is a form input with help and error text |
| [Stack](stack.md) | the label is not part of the arrangement |
| `ButtonGroup` | the row is commands, not a labelled control |

---

## Values

- must leave `orientation` at `horizontal`; `vertical` only for a wide control
- must leave `divided` on for a stacked list — the rule already skips the last row
- should pass `labelWidth` to align labels down a stack — a CSS length, `"6rem"`
- should reach for the `label` slot for richer content; it overrides the prop's text
