# NodeEditor

*Last updated: 2026-08-19*

> The node graph — boxes on a pannable canvas, joined by edges.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `NodeEditor.spec.md`.

## Reach for it when

- must show a graph the reader arranges — a pipeline, a flow, a dependency map
- must expect first-generation scope — no drag-to-connect, no minimap, no auto-layout
- should own the node positions in the caller; the editor reports a move

---

## Instead of

| Reach for | When |
|---|---|
| [Tree](tree.md) | the graph is a hierarchy with one parent per node |
| [Gantt](gantt.md) | the nodes are dated tasks and the edges are dependencies |
| [Timeline](timeline.md) | the nodes sit in one order on one rail |

---

## Values

- should leave `nodeWidth` at `160` px and `nodeHeight` at `60` px
- should leave `minZoom` at `0.25` and `maxZoom` at `2`
- must pass `edges` explicitly; an unset graph renders nodes with nothing between them
