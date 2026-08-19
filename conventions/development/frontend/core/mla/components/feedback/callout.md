# Callout

*Last updated: 2026-08-19*

> The quiet aside — a coloured left rule and no fill, for a note that lives inside prose.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).
> Its full surface → `Callout.spec.md`.

## Reach for it when

- must sit inline in documentation or long-form content, MDX-style
- must stay quieter than an alert — the rule carries the severity, not a fill
- should hold supplementary detail the reader may skip without losing the thread

---

## Instead of

| Reach for | When |
|---|---|
| [Alert](alert.md) | the note reports system state and may carry actions |
| [AlertSimple](alertSimple.md) | the note earns a filled surface at its severity |
| `InfoRow` | the content is a labelled datum rather than a note |

---

## Values

- must carry the body in the default slot — only `icon` and `title` take props
- should leave `severity` at its `info` default; `neutral` renders a plain border rule
- must not bind a close handler — the callout ships none and stays with the content
