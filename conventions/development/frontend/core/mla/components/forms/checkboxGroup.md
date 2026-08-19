# CheckboxGroup

*Last updated: 2026-08-19*

> Zero-to-many from a short fixed set, every option visible at once under one legend.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `CheckboxGroup.spec.md`.

## Reach for it when

- must collect several values from a set short enough to show whole
- must give every item a `value` — the group keys selection by it
- should carry `legend`; it is the group's label and its `fieldset` needs one

---

## Instead of

| Reach for | When |
|---|---|
| [MultiSelect](multiSelect.md) | the set is long enough to need a dropdown |
| [Listbox](listbox.md) | the options scroll in place with arrow-key movement |
| [Checkbox](checkbox.md) | the box is one independent boolean |
| `ToggleButtonGroup` | the choices set a mode rather than a submitted value |

---

## Values

- should leave `orientation` at `vertical` — the readable default for labels
- must set `horizontal` only for two or three short options
- must cascade `isDisabled` from the group, never repeat it per item
- must not wrap an item in its own field — the group hands each a fresh context
