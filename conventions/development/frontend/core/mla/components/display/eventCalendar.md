# EventCalendar

*Last updated: 2026-08-19*

> The calendar the reader browses — month, week, day, or agenda.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `EventCalendar.spec.md`.

## Reach for it when

- must let the reader move through dates and read what is on them
- must expect first-generation scope — no drag-edit, no recurrence
- should bind `v-model:view` and `v-model:date` when an outer control drives the range

---

## Instead of

| Reach for | When |
|---|---|
| [ScheduleView](scheduleView.md) | one day is shown across several resources |
| [HeatmapCalendar](heatmapCalendar.md) | the year is read as density, with no events to open |
| [Gantt](gantt.md) | the spans are plan tasks with dependencies |

---

## Values

- should leave `defaultView` at `month` and `weekStart` at `0`
- should narrow `hourRange` from the full `[0, 24]` to the working window
- must anchor `date` as a zoned instant — its zone decides which day a moment falls on
