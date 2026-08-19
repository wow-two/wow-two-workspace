# FilePicker

*Last updated: 2026-08-19*

> A button that opens the OS file dialog — the small file control, with no drop target.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `FilePicker.spec.md`.

## Reach for it when

- must take a file from a button press in a dense row or toolbar
- must fit where a dropzone would not — a settings row, an inline avatar swap
- should fill `preview` with the chosen file's name or thumbnail; nothing renders by default

---

## Instead of

| Reach for | When |
|---|---|
| [FileUpload](fileUpload.md) | the whole surface takes a drop and rejects by type, size, or count |
| `Button` | the press runs a command and reads no file back |

---

## Values

- must pass `accept` and `multiple` as native attributes — they fall through to the input
- must rename `label` from `Choose file` to the file's own noun — `Upload logo`
- should leave `size` at `md`; it matches the input row it sits in
- must validate size and type yourself — this one rejects nothing
