# Components

*Last updated: 2026-08-19*

> A language form used end to end — declaring it, keeping it, wiring it, reading it.
> Purpose — one owner for a form's whole span, so no doc re-argues a `const` object at each use site.
> Use case — writing a constants holder, a value set, or a `*Extensions` object over a type.

## The gate [REQUIRED]

- must place a doc here only when it governs a **language form used end to end** — declaration through use.
- must place it in [`lla/constructs/`](../constructs/constructs.md) when it says only what the form is and
  whether we write it.
- must place it in [`mla/components/`](../../mla/components/components.md) when the thing is one **we** coined —
  `Page`, `Overlay`, `Model`, `Result` are ours, not the language's.
- must not read self-sufficiency as the test — every form has a caller, and a constant has a reader.
- must keep the whole span in the one file — a rule about writing the form and a rule about reading it stay together.

| Doc | The form, end to end |
|---|---|
| [constants](constants.md) | the `const` binding — casing, `as const`, co-location, the doc line |
| [enums](enums.md) | the `const` object value set — derived type, label Record, wire casing, use sites |
| [extensions](extensions.md) | the `const` object of statics over one type — naming, shape, JSDoc, location |

---

## Neighbours

- [constructs](../constructs/constructs.md) — the forms themselves, and the verdict on writing each
- [notation](../notation/notation.md) — the naming and doc defaults a doc here overrides in its own file
- [mla components](../../mla/components/components.md) — the roles we coined, and the shape a components doc takes
