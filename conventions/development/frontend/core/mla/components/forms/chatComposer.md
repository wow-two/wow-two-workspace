# ChatComposer

*Last updated: 2026-08-19*

> The message box for a thread — an autogrowing textarea, a toolbar, and a send button.
> A [control](../../constructs/visual/control.md): it owns the draft text and composes the send as an
> [action](../../constructs/visual/action.md), so the `submit` emit is not a form's.
> Its full surface → `ChatComposer.spec.md`.

## Reach for it when

- must compose a message into a running thread, not a document
- must handle a keystroke send and a newline in the same box
- should hang attach or model pickers off `leading` and `trailing`

---

## Instead of

| Reach for | When |
|---|---|
| [TextAreaInput](textAreaInput.md) | the page owns the send and the box only collects text |
| [MarkdownEditor](markdownEditor.md) | the author writes a document and wants a preview |
| `MessageList` | the surface renders the thread rather than composing into it |

---

## Values

- should leave `submitOn` at `enter` — the chat default readers expect
- must set `submitOn` to `mod-enter` only where multi-line drafts are the norm
- should leave `maxHeight` at `200` px; past it the textarea scrolls
- must set `isSendButtonHidden` only when the page renders its own send
