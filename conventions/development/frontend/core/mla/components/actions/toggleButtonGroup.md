# ToggleButtonGroup

*Last updated: 2026-08-19*

> The strip that owns one selection across its [ToggleButton](toggleButton.md) children.
> What an action is → [action](../../constructs/visual/action.md).
> Its full surface → `ToggleButtonGroup.spec.md`.

## Reach for it when

- must reach for it when the row's value matters, not the individual presses
- must reach for it with `type="multi"` when any number of items may stay on at once
- should reach for `variant="segmented"` for a short exclusive picker — day / week
- should reach for `variant="pill"` when the items read as detached chips

---

## Instead of

| Reach for | When |
|---|---|
| [ButtonGroup](buttonGroup.md) | the row is commands, with nothing selected |
| [SegmentedControl](segmentedControl.md) | never — a deprecated alias for `variant="segmented"` |
| `RadioGroup` | the selection is a form field, submitted with the form |
| `Tabs` | the strip switches content panels rather than setting a value |
| [OptionTileGroup](optionTileGroup.md) | the options are icon-only preset tiles |

---

## Values

- must give each child [ToggleButton](toggleButton.md) a `value` matching the group's
- must set `itemRole="tab"` only when the strip drives real tab panels
- should keep `type` at `single`; re-pressing the active item clears it
- should leave attachment alone — `segmented` forces it on, `pill` never attaches
- should set `equalWidth` when every cell shares the row width — an icon strip
