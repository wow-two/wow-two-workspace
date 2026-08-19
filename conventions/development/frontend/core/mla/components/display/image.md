# Image

*Last updated: 2026-08-19*

> A picture with a fallback for when it fails to load.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Image.spec.md`.

## Reach for it when

- must render content the reader looks at — a photo, a screenshot, a cover
- must fill the fallback slot; without one a broken source leaves a broken image
- should wrap it in `AspectRatio` when the box must not resize as the file loads

---

## Instead of

| Reach for | When |
|---|---|
| [Avatar](avatar.md) | the picture stands for a person or an account |
| `Icon` | the mark is a glyph rather than a file |
| [PdfViewer](pdfViewer.md) | the file is a document with pages |

---

## Values

- must set `alt`; an omitted one is coerced to empty, claiming decoration
- must let the component own `onError`; a caller's handler is chained, never replaced
