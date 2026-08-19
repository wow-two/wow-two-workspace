# HeatmapCalendar

*Last updated: 2026-08-19*

> The year grid — 53 weeks by 7 days, each cell shaded by its count.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `HeatmapCalendar.spec.md`.

## Reach for it when

- must show a whole year's activity at once — commits, streaks, sessions, logins
- must key the values by calendar date; a `Map` of dates to counts is the input
- should bind `onCellClick` as a prop; its presence makes a cell a button

---

## Instead of

| Reach for | When |
|---|---|
| [EventCalendar](eventCalendar.md) | the days hold events the reader reads and opens |
| [Sparkline](sparkline.md) | the series is a line rather than a per-day grid |
| [Gantt](gantt.md) | the marks span ranges rather than land on single days |

---

## Values

- should leave `cellSize` at `12` px, `gap` at `2` px, `levels` at `5`, `tone` at `brand`
- should leave `weekStart` at `0`, and set `1` only where the locale starts on Monday
- must leave `year` unset for the current year — it is resolved lazily on purpose
- should leave `hasLegend` on; the shading means nothing without its scale
