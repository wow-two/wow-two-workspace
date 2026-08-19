# CopyButton

*Last updated: 2026-08-19*

> A one-click clipboard write that swaps to a copied state on its own.
> What an action is → [action](../../constructs/visual/action.md).
> Its full surface → `CopyButton.spec.md`.

## Reach for it when

- must reach for it beside a code block, ID, token, or share URL
- must reach for it rather than wiring `navigator.clipboard` behind a [Button](button.md)
- should read the slot's `{ copied, error }` when the label swaps, not only the icon

---

## Instead of

| Reach for | When |
|---|---|
| [Button](button.md) | the command is anything other than a clipboard write |
| [Button](button.md) | the payload is rich or multi-part — the copied text is a plain string |

---

## Values

- must keep `resetAfter` at `2000` ms; `0` holds the copied state until unmount
- must keep the default `ghost` variant beside content — a secondary affordance
- must supply `aria-label`; add `copiedAriaLabel` only if the name must change
- should surface a failed copy through the `error` emit — no toast ships
