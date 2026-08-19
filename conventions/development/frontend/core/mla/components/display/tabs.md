# Tabs

*Last updated: 2026-08-19*

> One strip, one visible panel — sibling views of the same subject.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `Tabs.spec.md`.

## Reach for it when

- must show alternative views of one subject, exactly one at a time
- must compose the parts as siblings — `TabsList`, `TabsTab`, `TabsPanel`
- should keep the tab set small and stable; a growing set belongs in a nav

---

## Instead of

| Reach for | When |
|---|---|
| [Accordion](accordion.md) | the sections stack and more than one may be open |
| `SegmentedControl` | the strip sets a value rather than swapping a panel |
| `NavigationMenu` | the entries are routes rather than panels |
| [Carousel](carousel.md) | the panels are stepped through in order |

---

## Values

- must set `defaultValue` — an unset active value renders no panel
- should leave `activationMode` at `automatic`; `manual` when a panel costs a fetch
- should leave `orientation` at `horizontal`
