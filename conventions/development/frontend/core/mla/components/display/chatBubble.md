# ChatBubble

*Last updated: 2026-08-19*

> One message in a conversation — a side, a tone, and a delivery state.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `ChatBubble.vue`.

## Reach for it when

- must render a single message inside a [MessageList](messageList.md)
- must set `tone="system"` for a join, leave, or metadata row; it centres itself
- should pair the footer slot with a [ReactionBar](reactionBar.md)

---

## Instead of

| Reach for | When |
|---|---|
| [CommentThread](commentThread.md) | the message is a comment carrying nested replies |
| [ActivityFeed](activityFeed.md) | the row is an actor-verb-target sentence, not a message |
| [Card](card.md) | the message is a record rather than a turn in a conversation |

---

## Values

- must set `side="end"` for the reader's own messages; `start` is the default
- must set `isTailless` on every message but the last of a stacked run
- must set `canShowStatusOnStart` for inbound delivery; it is hidden there
