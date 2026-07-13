# Forms

*Last updated: 2026-07-13*

> Form state, validation, server-error wiring, and the control catalog — every form runs on the `@wow-two-beta/ui` `/forms-engine` facade (`useAppForm`) composed
> with the presentation `Field` chrome; supersedes hand-rolled `useState`-per-field forms. The engine architecture behind the facade
> (contract · adapters · conformance): [../../swappable-modules.md](../../swappable-modules.md).

## Entities

The surface a form touches — all from `@wow-two-beta/ui/forms-engine` (engine-free) unless noted.

| Entity | Kind | Role |
|---|---|---|
| `useAppForm` | hook | creates the form (`{ defaultValues, schema, onSubmit }`); imported from the app's pinned `@/form` |
| `AppForm` · `AppFieldApi` · `AppFormState` | types | the form / field / state contract types |
| `form.Field` | render-prop | binds one field; composes the presentation `Field` chrome |
| `form.Subscribe` · `form.useFormState` | selector | slice-subscribe (`isSubmitting`, `submitError`, `isDirty`, …) |
| `useFieldArray<TItem>` | hook | typed row collections (`rows`, `key`, `push`/`remove`/`move`) |
| `StandardSchemaV1` | type | the validation seam (zod 4 default; valibot per-form swap) |
| `{Model}Schema` · `empty{Model}` | app | the whole-form schema + init-values const, in `application/{domain}/` |
| `*ApiRequest` / `*Dto` | app | the shape the form **produces** — bind `defaultValues` to it |
| `ApiError` | type | thrown from `onSubmit`; drives auto field-error mapping (`foundation/http`) |

## Engine pin

- must pin the engine once per app — `src/form.ts` re-exports exactly one adapter subpath; screens import `useAppForm` from `@/form`
- must import contract types (`AppForm`, `AppFieldApi`, `AppFormState`, `StandardSchemaV1`) from `@wow-two-beta/ui/forms-engine` — the engine-free
  entry
- must not import `@tanstack/react-form` (or any engine package) in app code — native access goes through the pinned adapter's typed `form.engine`
- default pin `/forms-engine/tanstack` (optional peer `@tanstack/react-form`); `/forms-engine/house` — the zero-dependency micro-engine for the
  smallest apps; swapping engines = editing the pin line

```typescript
// src/form.ts — the only vendor-touching line in the app
export { useAppForm } from '@wow-two-beta/ui/forms-engine/tanstack';
```

---

## Values and schema

- must bind the form to the shape it **produces** — a **`*ApiRequest`** (form submits to the backend) or a **`*Dto`** (form updates a frontend model instance). There is no third case, so **no bespoke `*Values` / `*Draft` type**. Fields stay forgiving while editing (`""` for a required string, enums as `string`), validated at submit; a UI-only row key comes from `useFieldArray`'s `row.key`, never a modeled `id`
- must validate with one whole-form schema — `zod` 4 default; the seam is `StandardSchemaV1` (so `valibot` is a per-form size-first swap). A **partial** schema (only the fields the form owns) is fine — the backend is the source of truth
- must name the schema `{Model}Schema` and co-locate it with the mappers, form-adjacent in `application/{domain}/`; an `empty{Model}` **init-values const** (the `defaultValues`) is fine — "values" names the initial-state constant, not a type
- must keep validation messages in the schema (`z.string().min(3, '…')`), never in the component

---

## Creation

- must create the form with `useAppForm({ defaultValues, schema, onSubmit })` — `defaultValues` carries the complete `*Values` shape
- must keep async edit-prefill on `/query` — render the form once data is loaded, or `reset(data)`; must not fan prefill into per-field
  setter effects
- `reset()` returns to `defaultValues`; `reset(next)` re-seeds the values **and** the dirty baseline

```typescript
const save = useAppMutation({ mutationFn: registerProduct, invalidates: () => [productKeys.list] });

const form = useAppForm({
  defaultValues: { slug: '', name: '', repo: '' },
  schema: ProductSchema,
  onSubmit: (values) => save.mutateAsync(values),
});
```

---

## Field wiring

- must render every field through `form.Field`, composing the presentation `Field` chrome (label / helper / error) in the render prop
- free via `FormControlContext`: control `id` / `aria-describedby` / `aria-invalid` / `disabled` / `required` / `readOnly` on every SDK control that
  reads `useFormControl` (`TextInput`, `Select`, `DatePicker`, …), `Label` targeting, `FormErrorMessage` `role="alert"` — must not hand-wire ids
  or aria
- the app adds only: `label`, the `value` / `setValue` binding, and `onBlur={f.onBlur}` (touched tracking) — errors render automatically; the `error`
  prop is a single-message override, not the default
- must put per-mode flags on the chrome (`<Field isDisabled>` for an edit-locked field); a bare control without chrome gets the same wiring from
  `form.Field`'s own `isDisabled` / `isRequired` / `isReadOnly` props; `Field` inside `form.Field` adopts the glue's provider (flags may live on
  either) and `aria-describedby` / `aria-labelledby` reference only rendered chrome
- `f.errors` is client + server messages merged, client first — `Field` / `FormErrorMessage` render them all; first-error-only display is opt-in via
  the `error` override
- may disable the whole form — `useAppForm({ …, isDisabled })` ORs into every `form.Field`'s control-disabled flag (on top of any per-field
  `<Field isDisabled>`) and makes `handleSubmit` / auto-submit inert; for read-only / role-locked screens or a while-related-data-loads freeze — must not
  hand-disable each control

```tsx
<form.Field name="slug">
  {(f) => (
    <Field label="Slug" isDisabled={isEdit}>
      <TextInput value={f.value} onChange={(e) => f.setValue(e.target.value)} onBlur={f.onBlur} />
    </Field>
  )}
</form.Field>
```

---

## Controls

All `presentation/forms` controls read `FormControlContext`, so inside `form.Field` they inherit id / aria / disabled / required wiring for free (§Field wiring). Import from `@wow-two-beta/ui/presentation/forms`; per-control detail lives in the SDK component catalog (`engineering/architecture/component-catalog.md` §presentation/forms). **74 controls**, by family:

| Family | Controls |
|---|---|
| Field chrome | `Field` · `Fieldset` · `Legend` · `Label` · `LabeledInput` · `FormErrorMessage` · `FormHelperText` · `CharacterCount` · `PasswordStrength` · `InputGroup` · `InputAddon` |
| Text | `TextInput` · `TextAreaInput` · `PasswordInput` · `EmailInput` · `UrlInput` · `TelInput` · `PhoneInput` · `SearchInput` · `MaskedInput` · `PinInput` · `Editable` |
| Numeric | `NumberInput` · `CurrencyInput` · `PercentInput` · `Stepper` · `Knob` · `Slider` |
| Selection | `Select` · `MultiSelect` · `Combobox` · `Listbox` · `ChoiceCard` |
| Boolean & choice groups | `Checkbox` · `CheckboxField` · `CheckboxGroup` · `Radio` · `RadioField` · `RadioGroup` · `Switch` · `SwitchField` |
| Date & time | `Calendar` · `RangeCalendar` · `DateField` · `DatePicker` · `DateRangePicker` · `DateTimeField` · `TimeField` · `TimePicker` · `RecurrenceEditor` · `CronInput` |
| Color | `ColorArea` · `ColorField` · `ColorPicker` · `ColorSlider` · `ColorSwatch` · `ColorSwatchPicker` · `ColorWheel` · `GradientPicker` |
| File | `FileUpload` · `FilePicker` |
| Code & rich text | `CodeEditor` · `JSONEditor` · `MarkdownEditor` |
| Specialized pickers | `EmojiPicker` · `EmojiSizeControl` · `IconPicker` · `FontPicker` · `KeyboardShortcutPicker` · `ReactionPicker` · `TagsInput` |
| Composite / flow | `AddressForm` · `Wizard` · `ChatComposer` |

- the `*Field` variants (`CheckboxField` · `RadioField` · `ColorField` · `SwitchField` · `DateField` · `TimeField`) pair a control with the `Field` chrome for the common labelled-single-control case; drop to the bare control inside `<Field>` when you need custom chrome
- date & time controls speak `Temporal.PlainDate` / `PlainTime` (§Values and schema), never a native `Date`
- `Wizard` drives multi-step forms — gate each step with `form.validate()` (§Validation timing), one form spanning the steps, not per-step mini-forms

---

## Submit and server errors

- must let `onSubmit` be the only failure path — `onSubmit: (values) => mutation.mutateAsync(values)` when the app uses `/query`, else a direct
  `onSubmit: (values) => client.post(...)`; must not `try/catch` in the screen — the pipeline owns failures either way
- must throw the SDK `ApiError` (`foundation/http`) from the submit call — the default `mapSubmitError` is `instanceof`-gated, so an app on a hand-rolled
  client must re-export/throw the SDK `ApiError` or field mapping silently no-ops
- ProblemDetails field errors land on fields automatically — the default `mapSubmitError` is `fieldErrors` (both .NET shapes: the ModelState dict
  and the wow-two `[{ property, message }]` array), paths rewritten by `defaultMapFieldPath` (`Rules[0].Destination` → `rules[0].destination`)
- must render the unmapped remainder — `submitError: ApiError | null` — as the form-level `Alert` via `form.Subscribe`
- must read progress from `isSubmitting` (`form.Subscribe` / `form.useFormState`) — no hand-rolled `saving` flag
- must re-trim in `onSubmit` when a schema `.trim()`/transform shapes the DTO — the engine validates only, `onSubmit` receives the raw values
- may branch on the submit verdict — `const ok = await form.handleSubmit()` (`Promise<boolean>`) or the `isSubmitSuccessful` slice — for wizard-step
  gates / post-submit navigation; must not track a hand-rolled `passed` ref
- may clear a dismissible submit banner with `form.clearSubmitError()`
- may apply out-of-pipeline server results with `setFieldErrors(errors)` — replaces the current server-error overlay
- may auto-submit — `submitOn: 'change' | 'blur' | 'manual'` (default `'manual'`) routes through the SAME submit path as `handleSubmit` (validation,
  `submitInvalid`, server-error mapping, verdict, concurrent guard all apply); pair `'change'` with `submitDebounceMs` (trailing, coalesces a burst)
  for settings / live-save, `'blur'` for save-on-blur. `reset()` / `reset(data)` / prefill never auto-submit — only user-origin writes do
- may submit past client errors — `submitInvalid: true` (default `false`, on the validation-config surface) always validates (errors still render,
  advisory) but runs `onSubmit` regardless — the **backend is the source of truth**; the verdict then reflects `onSubmit`, not the bypassed client gate
- the submit path is single-flight — a re-entrant trigger (double-click / Enter-spam / a `submitOn: 'change'` burst) coalesces onto the in-flight run,
  never a double-`onSubmit`; must not hand-roll an `isSubmitting` re-entry guard

```tsx
<form onSubmit={form.handleSubmit}>
  {/* fields */}
  <form.Subscribe selector={(s) => s.isSubmitting}>{(busy) => <Button type="submit" isLoading={busy}>Save</Button>}</form.Subscribe>
  <form.Subscribe selector={(s) => s.submitError}>{(e) => e && <Alert severity="danger" description={e.message} />}</form.Subscribe>
</form>
```

---

## Validation timing

- must keep the default `validateOn: 'submit'` — the first attempt validates everything; after it, touched fields re-validate on change
- may override per form: `'change'` when the field is the product (live parse / preview off keystrokes); `'blur'` when errors must surface earlier
- touched = blur or submit attempt — errors surface then, never on the first keystroke; server messages clear on the next change to their field
- must gate unsaved-changes guards on `isDirty` (baseline-compared) — pair with the router's `useNavigationBlocker`
- must derive live UI (previews, counts) through a selector — `form.Subscribe` / `form.useFormState(selector)` re-render only on the selected slice,
  never the whole form; pass `isEqual` to a selector returning a fresh object (`{a,b}`) or it re-renders every change
- must write derived / cross-field values with `form.setValue(path, value)` (e.g. name → slug) — not the `.engine` escape hatch
- may validate without submitting — `const ok = await form.validate()` (`Promise<boolean>`) runs the schema, populates + displays errors (marks fields
  touched), and returns client validity WITHOUT calling `onSubmit`; the clean single-form multi-step / wizard-step gate (RHF `trigger` / TanStack
  `validateAllFields` equivalent) — must not lean on `handleSubmit`-as-gate or per-step mini-forms when one form spans the steps
- may seed initial validity — `validateOnMount: true` (default `false`) runs one validation on mount for edit-screen validity indicators / wizard
  step-entry gating; fields stay untouched (`isTouched` false) so the pass shows validity without asserting the user interacted
- unsaved-changes edit screens: bare `reset()` returns to the ORIGINAL `defaultValues`, not the loaded entity — Discard must call `reset(loadedEntity)`

---

## Arrays

- must drive row collections with `useFieldArray<TItem>(form, path)` (from `@wow-two-beta/ui/forms-engine`, engine-free) — the typed row helper:
  reactive `rows` + stable `key`s, element-typed ops (`push` / `insert` / `remove` / `swap` / `move`, delegating to `form.array`), and a **cast-free**
  row field
- must render a row cell through `<array.Field index={row.index} name="…">` — `f.value` / `f.setValue` are typed as `TItem['…']` (one level deep);
  must not cast `f.value` on array rows (`f.value as string`), the tax `useFieldArray` exists to remove — the raw deep path `rules[0].destination`
  is `unknown` on `AppFieldValue` by design (no recursive path types)
- must key rows by `row.key`, never the array index — the helper's keys follow their row through insert/remove/swap/move, so focus + local state
  stay with the logical row on reorder; row-scoped errors and touched state reindex with every op
- `form.array(path)` is the lower-level primitive `useFieldArray` composes on — reach for it directly only for ops without rendered rows

```tsx
const rules = useFieldArray<RuleValues>(form, 'rules');   // rules.push(emptyRule()) · rules.remove(i) · rules.move(from, to)

{rules.rows.map((row) => (
  <div key={row.key}>
    <rules.Field index={row.index} name="destination">
      {(f) => (
        <Field label={`Destination ${row.index + 1}`}>
          <TextInput value={f.value} onChange={(e) => f.setValue(e.target.value)} onBlur={f.onBlur} />
        </Field>
      )}
    </rules.Field>
  </div>
))}
```

---

## Escape hatch

- `form.engine` is the native engine instance, typed by the adapter import — for the 10% past the contract (typed deep paths, per-field async
  validators, listeners)
- may couple one form to the pinned adapter through it — per-form and visible at the import site; must not pass `engine` into shared components
  or hooks
- must promote the pattern into the facade once 2+ forms reach for the same native feature — the contract-promotion rule in
  [../../swappable-modules.md](../../swappable-modules.md), never copy-paste
- the house engine has a hard ceiling (no typed deep paths / per-field async validators / listener graphs) — a form outgrowing it flips the app's
  pin to `/forms-engine/tanstack`

---

## Testing

- must exercise forms in interaction `play()` stories driven through the house engine — `/forms-engine/house` is zero-dependency, so the Storybook
  surface never needs the `@tanstack/react-form` peer
- engine parity is the SDK's job — `describeFormEngineConformance` pins identical semantics per adapter; apps must not re-test forms per engine
- must assert through the rendered chrome (`FormErrorMessage` text, disabled / loading submit) — never engine internals
