# Sortable

*Last updated: 2026-08-19*

> Drag-to-reorder — headless, handle-initiated, and it never owns the array.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Sortable.vue`.

## Reach for it when

- must let the reader set an order by hand — a playlist, a checklist, a column set
- must compose `SortableItem` per row and `SortableHandle` inside it
- should apply the move in the caller; `@reorder` reports raw `from` and `to` indices

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the order comes from sorting a column, not from the reader |
| [List](list.md) | the order is fixed |
| [SwipeActions](swipeActions.md) | the drag reveals actions rather than moving the row |

---

## Values

- must render a `SortableHandle` in every row — a row without one never drags
- must clamp the emitted indices before splicing; they arrive raw
