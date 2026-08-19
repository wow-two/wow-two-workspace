# Marquee

*Last updated: 2026-08-19*

> A strip that scrolls itself, forever — logos, ticker text, a wall of proof.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Marquee.spec.md`.

## Reach for it when

- must run a decorative band the reader never operates
- must expect the content duplicated once — the loop is a `-50%` translation
- should carry nothing the reader has to read exactly; it never stops on its own

---

## Instead of

| Reach for | When |
|---|---|
| [Carousel](carousel.md) | the reader steps through the items |
| [AvatarGroup](avatarGroup.md) | the strip is people and should end in a `+N` |
| [Typewriter](typewriter.md) | the motion is in the copy rather than the track |

---

## Values

- should leave `speed` at `30` s per traversal and `gap` at `48` px
- should leave `canPauseOnHover` on, so a reader can stop the band to read it
- should leave `direction` at `left`
