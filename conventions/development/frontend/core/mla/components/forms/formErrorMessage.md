# FormErrorMessage

*Last updated: 2026-08-19*

> The error line under a control — the node the control's `aria-describedby` points at.
> What feedback is → [feedback](../../constructs/visual/feedback.md).
> Its full surface → `FormErrorMessage.spec.md`.

## Reach for it when

- must reach for it only outside a [Field](field.md) — the wrapper mounts its own
- must let it read the context's `errors`; it renders every client and server message
- must not hand-roll an error paragraph — only this node registers as the described-by target
- should pass `message` only as a single hand-written override

---

## Instead of

| Reach for | When |
|---|---|
| [Field](field.md) | the control already has a wrapper that renders the error |
| [FormHelperText](formHelperText.md) | the copy is a hint, and yields while an error shows |
| `Alert` | the failure belongs to the whole form, not one control |

---

## Values

- must not set `id` unless detaching it — the control then stops describing itself by it
- must expect nothing to render while the context is valid; an error needs `isInvalid`
- must keep the message in the schema, never at the call site ([form](../../domains/forms/forms.md))
