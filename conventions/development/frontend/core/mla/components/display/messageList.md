# MessageList

*Last updated: 2026-08-19*

> The scrolling conversation viewport — sticky to the bottom, with a jump-to-latest.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `MessageList.vue`.

## Reach for it when

- must hold a live conversation that grows at the bottom
- must keep the messages in the default slot — the list owns the viewport, not the rows
- should compose `DaySeparator` between days rather than styling a divider by hand

---

## Instead of

| Reach for | When |
|---|---|
| [ThreadView](threadView.md) | the panel is one thread with a parent and a composer |
| [CommentThread](commentThread.md) | the messages nest as replies |
| [ActivityFeed](activityFeed.md) | the rows are system activity rather than messages |
| [List](list.md) | the rows do not grow and never need to stick |

---

## Values

- should leave `isSticky` on and `bottomThreshold` at `32` px
- should leave `hasJumpToBottom` on; a reader scrolled up must be able to return
- must leave `isReversed` off — the natural top-to-bottom order is what ships
