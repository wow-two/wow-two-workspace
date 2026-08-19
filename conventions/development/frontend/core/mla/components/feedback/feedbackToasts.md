# FeedbackToasts

*Last updated: 2026-08-19*

> The bus-to-viewport adapter — mounts the toast viewport and subscribes it to `notify()`.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).
> Its full surface → `FeedbackToasts.vue`.

## Reach for it when

- must render notices published through `notify()` or an explicit `FeedbackBus`
- must be mounted once at the app root, in place of a bare [Toaster](toaster.md)
- should reach for it whenever a non-view layer raises notices — a query hook

---

## Instead of

| Reach for | When |
|---|---|
| [Toaster](toaster.md) | every toast is fired imperatively from view code |
| [UndoBar](undoBar.md) | the notice is a single reversible act, not a queue |

---

## Values

- must not mount it beside a [Toaster](toaster.md) — every toast would render twice
- must mount it above anything that publishes; notices raised before mount are dropped
- should leave `bus` unset — it binds the `feedbackBus` that `notify()` publishes on
- should pass any [Toaster](toaster.md) value straight through — they all forward
