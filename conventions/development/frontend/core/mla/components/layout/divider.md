# Divider

*Last updated: 2026-08-19*

> The rule between two runs of content — plain, or carrying a centred label.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `Divider.vue`; no spec ships.

## Reach for it when

- must separate two runs of content with a visible line
- must reach for the labelled form for the classic "or" between two paths
- should reach for it inside a menu, a list or a form, between groups

---

## Instead of

| Reach for | When |
|---|---|
| `Separator` | the hairline is decorative and carries no separator role |
| [ControlGroup](controlGroup.md) | the settings rows already divide themselves |
| [Spacer](spacer.md) | the separation is space, with no line |

---

## Values

- must state `orientation` on a plain rule — the prop is required, never defaulted
- must read `orientation` as the line's own axis — `vertical` parts side-by-side content
- must not pass `orientation` beside a `label` — a labelled rule is always horizontal
- should reach for the `label` slot for richer content; it overrides the prop's text
