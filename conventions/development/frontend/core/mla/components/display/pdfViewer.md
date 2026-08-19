# PdfViewer

*Last updated: 2026-08-19*

> A PDF read in place — the browser's own viewer, framed with page and zoom controls.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `PdfViewer.spec.md`.

## Reach for it when

- must let a reader read a document without leaving the page
- must expect first-generation scope — no per-page render, no thumbnails, no search
- should pass `pageCount` when it is known; it enables `n / total` and clamps paging

---

## Instead of

| Reach for | When |
|---|---|
| [Image](image.md) | the file is a picture rather than a paged document |
| [DiffViewer](diffViewer.md) | two texts are compared rather than one read |
| `Link` | the document should open in its own tab |

---

## Values

- should leave `defaultPage` at `1`, `defaultZoom` at `100`, `height` at `70vh`
- must replace `title` — the default reads `PDF document` and names nothing
- should leave `canDownload` on unless the document must not leave the page
