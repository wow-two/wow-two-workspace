# CodeEditor

*Last updated: 2026-08-19*

> Source entry with a line-number gutter and Tab handling — plain by design, no highlighting.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `CodeEditor.spec.md`.

## Reach for it when

- must collect source the reader edits — a snippet, a config, a template
- must accept it is first-generation: a styled textarea, no highlighting or completion
- should pass `language` as the declared format; nothing renders from it yet

---

## Instead of

| Reach for | When |
|---|---|
| [JsonEditor](jsonEditor.md) | the value is JSON and must parse before it commits |
| [MarkdownEditor](markdownEditor.md) | the value is prose and the author wants a preview |
| [TextAreaInput](textAreaInput.md) | the text needs no gutter and no Tab handling |
| `Code` | the source is read and never edited |

---

## Values

- should leave `tabSize` at `2` — the house indent for every language shipped
- must set `isTabIndented` only where Tab must indent; it costs the keyboard exit
- should raise `minHeight` past `12rem` only for a whole file, not a snippet
