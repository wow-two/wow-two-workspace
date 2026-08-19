# Backdrop

*Last updated: 2026-08-19*

> The bare scrim — for a custom surface that has no overlay of its own.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).
> Its full surface → `Backdrop.spec.md`.

## Reach for it when

- must dim and block the page behind a surface the SDK does not already ship
- must not add one to a [Modal](modal.md), [Drawer](drawer.md) or [BottomSheet](bottomSheet.md) — each mounts its own
- should carry its own dismissal wiring; the scrim only reports the click

---

## Instead of

| Reach for | When |
|---|---|
| [Modal](modal.md) | the surface above the scrim is a dialog already in the group |
| `LoadingOverlay` | the scrim marks a busy region rather than an open surface |

---

## Values

- should leave `pointerEvents` at `auto`; `none` only for a dim that stays decorative
- must set `isInline` only when the scrim stays inside its stacking context — it portals to the body otherwise
