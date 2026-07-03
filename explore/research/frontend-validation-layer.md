# Frontend Validation Layer — Functionality Analysis

*Last updated: 2026-06-27*

> Scope: design a validation layer for the frontend SDK (`@wow-two-beta/ui`). Used for **forms first**, but the core must be reusable for **anything** (API payloads, config, business rules, runtime guards).
> This doc = exhaustive functionality catalog grouped by layer. Each bullet is one atomic capability to review (keep / cut / refine). Decisions deferred to the review pass.

## Design tenet

- **Split: framework-agnostic core (the "anything") + React forms binding + SDK UI integration** — three layers, one direction of dependency (UI → binding → core).
- Core never imports React; binding never imports Tailwind/components; UI integration is the only DOM/a11y layer.
- Prefer **adopt + extend** over build-from-scratch where a mature lib fits; own only the SDK-native glue.

## Existing assets to build on

- `primitives/formControlContext/FormControlContext.tsx` — provides `isInvalid`/`isRequired`/IDs + a11y wiring; controls already consume it.
- `forms/formField/FormField.tsx` — L4 wrapper: label + control + `FormErrorMessage`/`FormHelperText`; takes an `error` prop today.
- `hooks/useControlled.ts` — managed/unmanaged dual-prop pattern (SDK controls are **controlled**, not uncontrolled).
- `forms/wizard/Wizard.tsx` — only existing validation: per-step `registerValidator(): boolean | Promise<boolean>`.
- 79 form controls already wired to `FormControlContext` (TextInput, Select, DatePicker, etc.) — bind to these, don't rebuild.

---

## A. Core engine (framework-agnostic)

### A1. Schema / rule definition

- Primitive validators — `string`, `number`, `boolean`, `date`, `bigint`, `enum`.
- Composite validators — `object`, `array`, `tuple`, `record`, `union`, `intersection`.
- Discriminated unions — branch on a tag field.
- Modifiers — `optional`, `nullable`, `nullish`, `default(value)`.
- Literals & constants — exact-value match.
- Coercion — opt-in `string→number`, `string→Date`, etc.
- Transforms — `trim`/`lowercase`/`normalize`, kept distinct from validation.
- Built-in string formats — `email`, `url`, `uuid`, `regex`, length `min`/`max`.
- Built-in number rules — `min`/`max`, `int`, `positive`/`negative`, `multipleOf`.
- Built-in date rules — `before`/`after`, `min`/`max`.
- Custom refinement — arbitrary predicate → issue.
- Cross-field rules — e.g. `confirmPassword === password`, date ranges.
- Conditional rules — field required/validated only when another field matches.
- Schema composition — `extend` / `merge` / `pick` / `omit` / `partial`.
- Reusable rule fragments — named presets (`Username`, `Slug`, `PhoneUz`).
- Branded / nominal types — distinguish `Email` from `string` at type level.
- Recursive & lazy schemas — self-referential trees, deferred evaluation.

---

### A2. Execution mechanics

- Two entry shapes — throwing `parse` and result-returning `safeParse`.
- Granular scope — validate whole value, a single path, or a subtree.
- Sync and async execution paths in one API.
- Fail-fast (abort on first issue) vs exhaustive (collect all issues).
- Validation context — inject external data (current user, server state) into rules.
- Async refinement — `await` an external check (uniqueness, availability).
- Race-safety — cancel/ignore stale in-flight async results.
- Memoization — skip re-running on unchanged input.

---

### A3. Result & error model

- Discriminated result — `{ success, value }` | `{ success: false, issues }`.
- Typed transformed output on success (post-coercion/transform value).
- Structured issue — `path` + `code` + `message` + `params`.
- Stable machine-readable error codes (independent of message text).
- Multiple issues per field.
- Severity levels — `error` / `warning` / `info`.
- Tree ↔ flat-map conversions — nested issues or keyed-by-path.
- **Standard Schema** (`standardschema.dev`) interop — adopt as the public contract so any compliant lib (zod/valibot/arktype/own) plugs in.

---

### A4. Messages & i18n

- Default human message per built-in code.
- Templated messages with interpolated params (`"min {n} chars"`).
- Per-field / per-rule message override.
- Locale resolution + pluralization.
- Lazy formatting — resolve message text at render, not at validate.

---

## B. React forms binding

### B1. Form state

- State container — `values`, `errors`, `touched`, `dirty`, `submitCount`.
- Default values + `reset` (to defaults or to new values).
- Per-field meta — `isTouched` / `isDirty` / `isValidating` / `error`.
- Derived form flags — `isValid` / `isDirty` / `isSubmitting` / `isValidating`.
- Watch / subscribe — read field values without forcing parent re-render.
- Imperative API — `setValue` / `setError` / `clearErrors` / `trigger` / `focus`.

---

### B2. Field binding & triggers

- `useField` / register — connect any control to the form.
- Validation modes — `onChange` / `onBlur` / `onSubmit` / `onTouched` / `all`.
- Re-validation mode — strategy after first error (e.g. validate-on-change once invalid).
- Debounce/throttle per field for expensive (async) validators.
- Dependency-aware re-validation — re-run dependent fields on change.
- Controlled-input compatibility — must work with SDK's `useControlled` controls.

---

### B3. Dynamic structures

- Field arrays — add / remove / move / insert rows.
- Nested objects & arrays — deep paths (`address.city`, `items.0.qty`).
- Per-row validation + array-level rules (min items, unique).
- Stable keys for list reconciliation.

---

### B4. Submission & server errors

- Submit lifecycle — validate → `onSubmit(values)` → settle.
- Submit guards — block when invalid, expose `isSubmitting`.
- Map server (422) errors back onto fields by path.
- Form-level (non-field) error slot — e.g. "invalid credentials".
- Isomorphic schema — same schema validates on client and server.

---

## C. UI / SDK integration

### C1. Component wiring

- `<Form>` provider — owns state, exposes context to descendants.
- Bind to `FormControlContext` — auto-set `isInvalid`/`isRequired` from validation.
- `<Field>` / `useField` adapter for the 79 existing controls (no per-control rewrite).
- Derive HTML constraints from schema — `required`/`min`/`max`/`pattern` on the `<input>`.
- Zero-config path — `<Form schema={...}>` wires children automatically.

---

### C2. Error presentation

- Inline field error via existing `FormErrorMessage`.
- Form-level error summary — list of all errors, links to fields.
- Focus / scroll to first error on failed submit.
- First-error-only vs all-errors per field (configurable).
- Warning/info display distinct from blocking errors.

---

### C3. Accessibility

- `aria-invalid` + `aria-describedby` wiring (extends `FormControlContext`).
- `role="alert"` live-region announcement on error.
- Error-summary focus management (move focus to summary on submit fail).
- Required-field semantics (`aria-required`) from schema.

---

## D. Cross-cutting

### D1. TypeScript & DX

- Full inference — schema → value type, no duplicate type declarations.
- Typed field paths — autocomplete + compile-time path safety.
- Typed errors keyed by field.
- Minimal boilerplate — terminal goal is `<Form schema>` + controls.

---

### D2. Extensibility & interop

- Custom rule/validator registration.
- Adapter layer via Standard Schema — accept zod/valibot/arktype interchangeably.
- Override / extend built-in messages and codes.
- Plugin hooks — wrap validate (logging, analytics, telemetry).

---

### D3. Performance

- Tree-shakeable — pay only for rules used (beta SDK bundle budget).
- Isolated re-renders — one field's change doesn't re-render the whole form.
- Lazy async — don't run async validators until cheaper sync rules pass.

---

### D4. Non-form use cases (the "anything")

- API request/response validation at boundaries.
- Config / env-var validation at startup.
- Domain/business-rule invariants (reuse schema fragments).
- Runtime type guards / parsing of untrusted JSON.
- Data import validation (CSV/bulk rows → issue list).
- URL / query-param parsing.

---

### D5. Tooling & testing

- Test helpers — assert a value produces expected issue codes.
- Schema → mock/fixture generation (valid + invalid samples).
- Devtools — inspect form state / errors (optional).

---

## Library landscape (decide in review)

| Lib | Layer | One-liner |
|---|---|---|
| **Standard Schema** | contract | Interop spec (not a lib) zod/valibot/arktype implement — adopt as our boundary. |
| Zod | schema | Most-used TS-first schema; great inference; heavier bundle. |
| Valibot | schema | Modular + tree-shakeable + tiny; Standard Schema native. |
| ArkType | schema | Fastest, type-level; Standard Schema native. |
| Yup | schema | Older object-schema; pairs with Formik. |
| TanStack Form | binding | Headless, framework-agnostic, **controlled**, Standard-Schema native. |
| React Hook Form | binding | Perf-focused but **uncontrolled-first** — friction vs SDK's controlled controls. |
| Formik / Final Form | binding | Mature but older; heavier re-render model. |

---

## Key decisions for the review

- Own schema engine vs adopt (Valibot/Zod) vs **interop-only via Standard Schema**?
- Own form-state vs wrap **TanStack Form** (controlled, fits SDK) vs RHF (uncontrolled friction)?
- Where it lives in layering — core in `utils/` or new `validation/` foundation module; binding in `forms/`?
- Sync-default + async-opt-in, or async everywhere?
- Bundle budget + tree-shaking strictness for the beta SDK.
- Is Standard Schema the single public contract for both forms and the "anything" use cases?
