# NotificationDot

*Last updated: 2026-08-19*

> The bare dot — something is new, and the count does not matter.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `NotificationDot.spec.md`.

## Reach for it when

- must mark an unread nav item, tab, or avatar with no number to show
- must set `position` to pin it to a parent corner, or wrap it in an overlay

---

## Instead of

| Reach for | When |
|---|---|
| [CountBadge](countBadge.md) | the number of waiting items is worth showing |
| [Status](status.md) | the dot names a state and carries its label beside it |
| [BadgeOverlay](badgeOverlay.md) | the pinned thing is a badge rather than a bare dot |

---

## Values

- should leave `tone` at `destructive` and `size` at `sm`
- must set `position` only when the parent is a positioning context
- should set `hasPulse` for live arrivals only; a standing pulse reads as broken
