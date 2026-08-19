# Link

*Last updated: 2026-08-19*

> Inline text that goes somewhere — the one member of this folder that moves rather than runs.
> What an action is → [action](../../constructs/visual/action.md).
> Its full surface → `Link.spec.md`.

## Reach for it when

- must reach for it for a destination inside prose, a caption, or a footer
- must wrap a router link with `asChild` — middle-click and prefetch survive
- should reach for it when the destination reads as text, not as a control

---

## Instead of

| Reach for | When |
|---|---|
| [Button](button.md) | the trigger runs a command → [action](../../constructs/visual/action.md) |
| `Button asChild` | the destination has to carry a button's weight — a CTA |
| `ToolbarLink` | the destination sits inside a [Toolbar](toolbar.md)'s roving strip |
| `NavItem` | the destination is a row in a sidebar or nav structure → [nav](../../constructs/visual/nav.md) |

---

## Values

- must set `variant="inherit"` where the link takes the surrounding text colour
- must reach for `asChild` for a routing library's own link — no `as` prop ships
