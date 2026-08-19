# LLA — one symbol

*Last updated: 2026-08-19*

> Every rule whose reach is **one symbol** — the form it is declared in, that form carried end to end, and how
> it is written down.
> Purpose — settle spelling once, so no component doc re-argues a `const` object or a `<button>`.
> Use case — a rule that holds whatever kind the symbol belongs to, and needs no app around it to mean anything.

## The three buckets

| Bucket | Answers | Lead |
|---|---|---|
| [constructs](constructs/constructs.md) | which platform form may I write | one folder per platform, each with a ban |
| [components](components/components.md) | how do I use one form completely | a language form, end to end |
| [notation](notation/notation.md) | how is it written down | naming, documentation, style, imports |

---

## The boundary

The test is whether TypeScript, a framework or the browser supplies the term; `Dto`, `Entity` and `Page` are
ours, so they sit in [mla](../mla/mla.md) however familiar they read.

- must hold for **any** symbol — a rule naming a kind we coined is [mla](../mla/mla.md).
- must sink a rule here from `mla/` once it survives with no app, domain or collaborator present.
- must keep only `constructs/` platform-bound — a form used end to end and its notation are platform-neutral, so
  nothing else nests under a platform folder.
- must let a higher layer override a rule here, stated in that layer's own file, never by editing this one.

---

## The split inside

- `constructs/` states the form and the verdict on writing it; `components/` carries that same form through
  declaring, keeping, wiring and reading it.
- what a framework *offers* is a construct (`defineProps`, `useState`); how we *build a component* with it is
  [mla](../mla/mla.md). Each cites the other rather than restating it.
- a role **we** coined is never `lla/` — `Page`, `Overlay`, `Model` and `Result` are ours, so they sit in
  [`mla/constructs/`](../mla/constructs/constructs.md), and the register over them in
  [`mla/components/`](../mla/components/components.md).
- notation is a **default set** — a component may override a rule in its own file, and one that does not
  override cites [notation](notation/notation.md) rather than restating it.

---

## Neighbours

- [core](../core.md) — the scope cut this bucket sits in
- [mla](../mla/mla.md) — the scope above, where a kind we coined lands
- [shapes](../../shapes/shapes.md) — where a form is placed in a tree, which is never a `lla/` question
