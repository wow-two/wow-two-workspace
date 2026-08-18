# Notation

*Last updated: 2026-08-17*

> How a settled concept gets written down — its name, its documentation, its layout, its imports.
> Purpose — sit between the abstraction and the first keystroke, so no component doc re-argues spelling.
> Use case — reach here while turning a decided component into source.

## The four

| Bucket | Notates |
|---|---|
| [naming/](naming/naming.md) | identity — which characters stand for this thing |
| [documentation/](documentation/documentation.md) | intent — what the reader is told about it |
| [style/](style/style.md) | structure — how the text is arranged |
| [style/imports](style/imports.md) | reach — which names a file pulls in, and in what order |

---

## Defaults

- must apply to **every** symbol, whatever it is — a rule that needs a role is not notation.
- may be **overridden by a component**, which states the override in its own file.
- must not be restated by a component that does not override it — cite this folder instead.
- must hold for both frameworks — a rule true only of an SFC or only of JSX belongs with that framework.

---

## Neighbours

- [constructs](../constructs/constructs.md) — the constructs being notated
- [components](../components/components.md) — the roles that override
- [Vue SFC](../../mla/components/vue/vue-sfc.md) — the framework delta, which overrides rather than restates
