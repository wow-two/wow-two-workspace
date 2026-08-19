# RangeCalendar

*Last updated: 2026-08-19*

> The inline month grid that picks two ends, previewing the span under the pointer between them.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `RangeCalendar.spec.md`.

## Reach for it when

- must select a span — a stay, a reporting window, a leave request
- must keep the grid open so the span stays visible while it is built
- should reach for it as [DateRangePicker](dateRangePicker.md)'s panel, which mounts this one

---

## Instead of

| Reach for | When |
|---|---|
| [Calendar](calendar.md) | one day is picked, not a span |
| [DateRangePicker](dateRangePicker.md) | the grid belongs behind a trigger |
| `EventCalendar` | the spans are read rather than picked |
| `Gantt` | the spans are plan tasks with dependencies |

---

## Values

- must speak `DateRange` — `{ start, end }`, both `Temporal.PlainDate`
- must expect `null` until both ends land; the half-built range stays internal
- should bound the grid with `min` and `max` before reaching for a predicate
- must keep `isDisabled` a per-day predicate returning a boolean, never a flag
- must take the ends as Temporal — the spec still types them as `Date`
