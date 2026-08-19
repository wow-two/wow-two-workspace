# CronInput

*Last updated: 2026-08-19*

> The cron expression, typed, with a plain-English readout under it that says what was actually written.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `CronInput.spec.md`.

## Reach for it when

- must store a schedule in the form a job runner already reads
- must serve a reader who writes cron directly — an operator, not an end user
- should reach for it where the schedule is infrastructure rather than a person's calendar

---

## Instead of

| Reach for | When |
|---|---|
| [RecurrenceEditor](recurrenceEditor.md) | the reader is an end user, and the rule is calendar-shaped |
| [TimePicker](timePicker.md) | the value is one clock time, not a repetition |
| [TextInput](textInput.md) | the string is not a schedule and needs no readout |

---

## Values

- must speak a five-field cron string — minute, hour, day, month, weekday
- must expect `*/5 * * * *` when uncontrolled — every five minutes
- should leave `placeholder` at `* * * * *` and `hasPreview` on
- must expect step support to be first-generation — `*/N` only, never `from-to/N`
- must set `name` for a plain form post; the hidden input carries the expression
- must call the readout flag `hasPreview` — the spec still names it `showPreview`
