# Sparkline

*Last updated: 2026-08-19*

> The inline trend — a shape with no axes, no scales and no legend.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Sparkline.spec.md`.

## Reach for it when

- must show a direction beside a figure — in a table cell, a card, a [Stat](stat.md)
- must expect no axes; a reader who needs values needs a real chart
- should colour it by inheritance where it sits inside already-toned copy

---

## Instead of

| Reach for | When |
|---|---|
| [Stat](stat.md) | the endpoint is the story and the shape is not |
| [HeatmapCalendar](heatmapCalendar.md) | the series is per-day over a year |
| [Gantt](gantt.md) | the marks are spans on a schedule |
| [AudioWaveform](audioWaveform.md) | the bars are audio peaks the reader seeks through |

---

## Values

- should leave `variant` at `line`, `width` at `120`, `height` at `32`, `tone` at `brand`
- must set `min` and `max` to compare two sparklines; each scales to itself
- must replace `ariaLabel`; the default reads `Trend` and says nothing
