# AvatarGroup

*Last updated: 2026-08-19*

> Stacked avatars with a `+N more` tail.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `AvatarGroup.spec.md`.

## Reach for it when

- must show who is on a thread, a document, or a team in one strip
- must let the group set the size — it clones each child with the group's `size`
- should cap the strip with `max` so the row cannot grow without bound

---

## Instead of

| Reach for | When |
|---|---|
| [Avatar](avatar.md) | one identity is shown |
| [ReactionBar](reactionBar.md) | the strip counts reactions rather than people |
| [DescriptionList](descriptionList.md) | the people are listed with roles, not stacked |

---

## Values

- should leave `size` at `md` and `overlap` at `-ml-2`
- must set `max` when the set is unbounded; without it every child renders
- must not set a child's own `size` — the group overwrites it on clone
