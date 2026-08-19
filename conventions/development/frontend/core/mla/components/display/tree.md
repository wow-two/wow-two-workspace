# Tree

*Last updated: 2026-08-19*

> The nested tree — one selected leaf, many expanded branches.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Tree.spec.md`.

## Reach for it when

- must show a hierarchy the reader opens and closes — files, categories, an org
- must compose `TreeGroup` for a branch and `TreeItem` for a node
- should let the root own selection and expansion; the parts read them by injection

---

## Instead of

| Reach for | When |
|---|---|
| [Accordion](accordion.md) | the sections are flat and only one opens at a time |
| [List](list.md) | the entries do not nest |
| `TableOfContents` | the tree is a document outline that tracks the scroll |
| `NavItem` | the nodes are app destinations rather than data |

---

## Values

- must control `selectedValue` and `expanded` together, or leave both uncontrolled
- must seed a deep tree through `defaultExpanded`, landing on the right branch
