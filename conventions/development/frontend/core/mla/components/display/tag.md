# Tag

*Last updated: 2026-08-19*

> The removable pill — a badge the reader can take off.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Tag.spec.md`.

## Reach for it when

- must show a chosen filter, label, or recipient the reader can drop
- must bind `@close` — the close button renders only when a listener exists
- should leave the array to the caller; removal is reported, never applied

---

## Instead of

| Reach for | When |
|---|---|
| [Badge](badge.md) | the pill is inert and nothing removes it |
| `Chip` | the pill toggles a selection instead of being removed |
| [ReactionBar](reactionBar.md) | the pills are emoji reactions with counts |

---

## Values

- should leave `variant` at `neutral` and pick a tone only when it means something
- should leave `closeLabel` at `Remove`; change it when the verb is not removal
- must omit `@close` for a pill that cannot be dropped — the button disappears with it
