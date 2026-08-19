# DataGrid

*Last updated: 2026-08-19*

> The editable grid — cell-by-cell keyboard navigation and in-place edit.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `DataGrid.spec.md`.

## Reach for it when

- must let the reader change cell values without leaving the table
- must expect first-generation scope — range select, fill and TSV paste are not built
- should keep the row array on the caller; the grid reports an edit, it never mutates

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the rows are read and sorted, never edited |
| [Table](table.md) | the cells are irregular and nothing is edited |
| `Form` | the record is edited as fields rather than as a grid |

---

## Values

- must set `rowKey` to a stable id — it is required and drives every cell address
- should leave `isDense` unset; set it only where the grid is the whole screen
- must declare each column's cell type — the editor casts the typed string back by it
