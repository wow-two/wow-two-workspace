# ReactionPicker

*Last updated: 2026-08-19*

> The quick-reaction row — a handful of emoji reached in one click, with a `+` out to the full catalogue.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `ReactionPicker.vue`.

## Reach for it when

- must react to a message, a comment, or a post without opening anything
- must keep the common reactions one click away and the rest one click behind that
- should mount it inside a `Popover` on hover or long-press

---

## Instead of

| Reach for | When |
|---|---|
| [EmojiPicker](emojiPicker.md) | any emoji is fair game, and search matters |
| `ReactionBar` | the strip reports existing reactions and their counts |
| `ToggleButtonGroup` | the row owns one selection rather than many independent ones |

---

## Values

- must expect the seven house reactions when `emojis` is unset — `👍 ❤️ 😂 🎉 😮 😢 🚀`
- must pass `onMore` to render the `+` at all; without it the escape hatch is hidden
- should wire `onMore` to an [EmojiPicker](emojiPicker.md) — this row opens nothing itself
- should leave `size` at `md`; only `sm` and `md` have a drawn row
- must pass `selected` as the reactions already active, so they read as pressed
