# FileUpload

*Last updated: 2026-08-19*

> The dropzone — a whole surface that takes a drag, falls back to a click, and flags what it rejects.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `FileUpload.spec.md`.

## Reach for it when

- must accept a drag onto a region the reader can see and aim at
- must reject by type, size, or count and report which rule failed
- should reach for it when files are the screen's subject, not one row of it

---

## Instead of

| Reach for | When |
|---|---|
| [FilePicker](filePicker.md) | a button is all there is room for and nothing is rejected |
| `ProgressBar` | the transfer has started and only its progress is left to show |

---

## Values

- must set `maxSize` in bytes — nothing is capped by default
- must set `accept` as a MIME or extension list; an open zone takes anything
- must set `maxFiles` whenever `multiple` is on, or the count rule never fires
- must render the picked-file list yourself — this one emits `File[]` and shows none
- should rewrite the `Drop files here, or click to browse` label to name the file kind
