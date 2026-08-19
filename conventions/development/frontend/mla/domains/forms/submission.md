# Submission

*Last updated: 2026-08-18*

> What happens between a submit and a rendered error — the submit path, server-error mapping, validation timing
> and how a form is tested. Authoring the form itself: [forms](forms.md).

## Submit [REQUIRED]

- must let `onSubmit` be the only failure path — `onSubmit: (values) => mutation.mutateAsync(values)` on `/query`,
  else a direct client call; must not `try/catch` in the screen, the pipeline owns failures.
- must throw the SDK `ApiError` (`foundation/http`) from the submit call — the default `mapSubmitError` is
  `instanceof`-gated, so an app on a hand-rolled client silently maps nothing.
- must render the unmapped remainder — `submitError: ApiError | null` — as a form-level `Alert` through
  `form.Subscribe`.
- must read progress from `isSubmitting`, never a hand-rolled `saving` flag.
- must re-trim in `onSubmit` when a schema `.trim()` or transform shapes the DTO — the engine validates only,
  and `onSubmit` receives the raw values.
- must not hand-roll a re-entry guard — the submit path is single-flight, so a double-click, Enter-spam or a
  `submitOn: 'change'` burst coalesces onto the in-flight run.
- may branch on the verdict — `await form.handleSubmit()` returns `Promise<boolean>`, and `isSubmitSuccessful`
  is the same fact as a slice.
- may clear a dismissible banner with `form.clearSubmitError()`.
- may apply an out-of-pipeline server result with `setFieldErrors(errors)`, replacing the server-error overlay.

---

## Server errors

- ProblemDetails field errors land on fields automatically — the default `mapSubmitError` reads `fieldErrors` in
  both .NET shapes (the ModelState dict and the wow-two `[{ property, message }]` array).
- `defaultMapFieldPath` rewrites the paths — `Rules[0].Destination` → `rules[0].destination`.

---

## Auto-submit

- may set `submitOn: 'change' | 'blur' | 'manual'` (default `'manual'`) — it routes through the SAME path as
  `handleSubmit`, so validation, `submitInvalid`, error mapping, verdict and the concurrent guard all apply.
- should pair `'change'` with `submitDebounceMs` (trailing, coalescing a burst) for settings and live-save, and
  use `'blur'` for save-on-blur.
- must expect only user-origin writes to auto-submit — `reset()`, `reset(data)` and prefill never do.
- may submit past client errors with `submitInvalid: true` (default `false`) — errors still render but stay
  advisory, the **backend is the source of truth**, and the verdict then reflects `onSubmit`.

---

## Validation timing

- must keep the default `validateOn: 'submit'` — the first attempt validates everything, after which touched
  fields re-validate on change.
- may override per form — `'change'` when the field is the product (live parse or preview), `'blur'` when errors
  must surface earlier.
- must treat touched as blur or submit attempt — errors never surface on the first keystroke, and a server
  message clears on the next change to its field.
- must gate an unsaved-changes guard on `isDirty` (baseline-compared), paired with `useNavigationBlocker`.
- must derive live UI through a selector — `form.Subscribe` / `form.useFormState(selector)` re-render on the
  selected slice only; pass `isEqual` to a selector returning a fresh object, or it re-renders every change.
- must write a derived or cross-field value with `form.setValue(path, value)`, not the `.engine` escape hatch.
- may validate without submitting — `await form.validate()` runs the schema, displays errors, marks fields
  touched and returns client validity WITHOUT calling `onSubmit`; the clean wizard-step gate.
- may seed initial validity with `validateOnMount: true` (default `false`) — fields stay untouched, so the pass
  shows validity without asserting the user interacted.

---

## Escape hatch

- `form.engine` is the native engine instance, typed by the adapter import — for the tenth of cases past the
  contract (typed deep paths, per-field async validators, listeners).
- may couple one form to the pinned adapter through it, visible at the import site; must not pass `engine` into
  a shared component or hook.
- must promote the pattern into the facade once two or more forms reach for the same native feature
  ([swappable modules](../../../../swappable-modules.md)), never copy-paste it.
- must flip the app's pin to `/forms-engine/tanstack` when a form outgrows the house engine's ceiling — it has
  no typed deep paths, per-field async validators or listener graphs.

---

## Testing

- must exercise forms in interaction `play()` stories driven through the house engine — it is zero-dependency,
  so the Storybook surface never needs the `@tanstack/react-form` peer.
- must not re-test a form per engine — `describeFormEngineConformance` pins identical semantics per adapter.
- must assert through the rendered chrome (`FormErrorMessage` text, a disabled or loading submit), never engine
  internals.

---

## Neighbours

- [forms](forms.md) — the form contract this path runs on
- [state and data](../data/state-and-data.md) — the mutation and cache invalidation a submit drives
