# Table

*Last updated: 2026-08-19*

> The table primitives — the caller writes the rows and cells by hand.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Table.spec.md`.

## Reach for it when

- must lay out a table whose cells no column descriptor can express
- must own the markup — the parts ship as siblings, `TableHead` through `TableCaption`
- should let the root carry density and striping; the sections read them by injection

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the rows come from data and a `columns` descriptor covers them |
| [DataGrid](dataGrid.md) | the reader edits cells in place |
| [DescriptionList](descriptionList.md) | the table is one record's properties, not many records |
| [List](list.md) | each row has a single field |

---

## Values

- should leave `density` at `cozy` and `radius` at `md`
- should leave `isStriped` and `isHoverable` off unless the rows are hard to track
- must set `isBare` only when an outer surface already owns the scroll wrapper
- must class the wrapper via `containerClassName`; `class` lands on the `<table>`
