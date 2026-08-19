# ScheduleView

*Last updated: 2026-08-19*

> One day across many resources — rooms, staff, or machines against the hours.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `ScheduleView.spec.md`.

## Reach for it when

- must answer who or what is free, at which hour, on one day
- must bind `onSlotClick` as a prop; its presence renders the slot overlay

---

## Instead of

| Reach for | When |
|---|---|
| [EventCalendar](eventCalendar.md) | the reader browses dates rather than resources |
| [Gantt](gantt.md) | the axis spans days and the bars carry dependencies |
| [Table](table.md) | the bookings are read as rows rather than placed on an axis |

---

## Values

- should leave `hourRange` at `[8, 20]` and widen it only where the day really runs longer
- should leave `slotMinutes` at `30`; a finer grid costs width per resource
- must anchor `date` as a zoned instant — its zone decides which day is rendered
