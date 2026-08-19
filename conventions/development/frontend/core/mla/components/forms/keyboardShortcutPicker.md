# KeyboardShortcutPicker

*Last updated: 2026-08-19*

> Record a chord — the reader presses the combination and the control captures it as normalized keys.
> What a control is → [control](../../constructs/visual/control.md).
> Its full surface → `KeyboardShortcutPicker.spec.md`.

## Reach for it when

- must let a reader rebind a command in settings
- must accept the value is a key-name array — `['Meta', 'K']`, never a display string
- should reach for it over typing the chord; a typed shortcut is unverifiable

---

## Instead of

| Reach for | When |
|---|---|
| `KeyboardShortcut` | the chord is shown beside a command, not set |
| `Kbd` | one key is rendered inline in prose |
| [TextInput](textInput.md) | the value is a command name rather than a chord |

---

## Values

- must render the chord back with `Kbd`; the picker only shows it while set
- must reject a chord that collides with a browser or OS binding — nothing is checked here
- should keep `Click to record` and `Press keys…`; they name the two states plainly
