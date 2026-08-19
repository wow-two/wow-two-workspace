# AlertModal

*Last updated: 2026-08-19*

> The confirm — a modal locked to `alertdialog` that a stray click outside cannot dismiss.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).
> Its full surface → `AlertModal.spec.md`.

## Reach for it when

- must gate a destructive or irreversible act — delete, revoke, discard
- must force an explicit choice; there is no corner close affordance
- should name the consequence in the description, not only in the title

---

## Instead of

| Reach for | When |
|---|---|
| [Modal](modal.md) | the flow is not a confirm and dismissing it costs nothing |
| `UndoBar` | the act is reversible — undo after it beats a confirm before it |
| [ActionSheet](actionSheet.md) | a phone picks between several actions, one of them destructive |

---

## Values

- must not pass `dismissOnOutsideClick` — the type omits it and the scrim is inert
- should land initial focus on the safe option, `Cancel`
- should keep `dismissOnEscape` on, clearing it only when a stray Escape loses work
