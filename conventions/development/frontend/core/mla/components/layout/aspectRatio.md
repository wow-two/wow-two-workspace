# AspectRatio

*Last updated: 2026-08-19*

> The shape lock — a box that holds its ratio before its content has loaded.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `AspectRatio.spec.md`.

## Reach for it when

- must derive a media box's height from its width, ahead of the load
- must hold one child — an image, a video, an embed
- should reach for it wherever a late-loading media box would shift the page

---

## Instead of

| Reach for | When |
|---|---|
| [Frame](frame.md) | the box needs a border and padding, not a fixed shape |
| [Box](box.md) | the height is set outright rather than derived |
| [Center](center.md) | the child is positioned, and the box's shape is free |

---

## Values

- must leave `ratio` at `1` for a square, and pass the fraction otherwise — `16 / 9`
- must give the child `absolute inset-0 h-full w-full` — the box only sets the ratio
