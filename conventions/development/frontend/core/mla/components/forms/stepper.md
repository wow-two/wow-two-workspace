# Stepper

*Last updated: 2026-08-19*

> A flow walked stage by stage — the step strip and the panel it swaps are one component.
> What a control is → [control](../../constructs/visual/control.md): it owns the active step.
> Its full surface → `Stepper.spec.md`.

## Reach for it when

- must move a reader through stages that are done in order
- must compose the parts — `StepperList`, `StepperStep`, `StepperPanel`
- should reach for it when each stage collects input, not only when it reports progress

---

## Instead of

| Reach for | When |
|---|---|
| `ProgressSteps` | the stages are only marked and nothing is switched |
| `Tabs` | the panels are alternative views, reachable in any order |
| `Accordion` | the sections stack and more than one may be open |

---

## Values

- must set `defaultValue` to the first step's `value` — an unset step renders no panel
- should leave `orientation` at `horizontal`; `vertical` once the labels stop fitting a row
- must give every `StepperStep` and `StepperPanel` the same `value` — it is the pairing key
- must set `isDisabled` on a step the reader may not skip to; nothing is gated by default
