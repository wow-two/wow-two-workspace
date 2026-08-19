# FrameGlyph

*Last updated: 2026-08-19*

> The viewfinder mark — an outer frame with an inner pupil, or the pupil alone.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `FrameGlyph.vue`.

## Reach for it when

- must preview a QR eye, a scanner corner, or a viewfinder in a preset picker
- must drive it from the numbers the real render uses, never set by eye
- should mount it inside an `OptionTile` when it labels a choice

---

## Instead of

| Reach for | When |
|---|---|
| [RadiusGlyph](radiusGlyph.md) | the mark shows one extent as a filled disc |
| [ModuleGlyphs](moduleGlyphs.md) | the mark previews a module shape rather than an eye |
| `Icon` | the mark is a named icon rather than a parameter preview |

---

## Values

- should leave `size` at `20` px, the preset-grid step
- must set `frameRx` and `pupilRoundness` from the values being previewed, not by eye
- must set `isDot` to render the enlarged pupil alone, without its frame
