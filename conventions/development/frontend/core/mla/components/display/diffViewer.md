# DiffViewer

*Last updated: 2026-08-19*

> Two versions of a text, lined up — split or unified.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `DiffViewer.spec.md`.

## Reach for it when

- must show what changed between two revisions — a config, a document, a record
- must expect line-level granularity; no intra-line word highlighting ships
- should switch to `unified` where the column is too narrow for two panes

---

## Instead of

| Reach for | When |
|---|---|
| [Code](code.md) | one version is shown and nothing is compared |
| [Table](table.md) | the changes are rows of fields rather than lines of text |
| [Timeline](timeline.md) | the story is the sequence of revisions, not one comparison |

---

## Values

- should leave `view` at `split`, `hasStats` on
- must replace `leftLabel` and `rightLabel`; the defaults read `Before` and `After`
- must pass both sides as strings — an absent side falls back to empty, not to unchanged
