# Frontend conventions — rule conflicts

*Last updated: 2026-08-19*

> Defects **inside** the conventions: two docs stating opposite verdicts on one identifier, a rule refuted by
> its own example, an index describing a doc differently from the doc itself, or one rule restated in a second
> doc instead of linked ([conventions.md](conventions/conventions.md) § *One owner per rule*).
> Purpose — a rule that contradicts another cannot gate code; every row needs a verdict, not a sweep.
> Use case — pick a row, decide the winning side, edit both docs, tick it. Code debt lives in the SDK's
> [conventions sweep](workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/planning/ui-sdk-conventions-sweep.md).

Fourth measurement, 2026-08-19, after the `visual/` · `behavior/` · `data/` recut of `mla/constructs/`.
Paths are relative to `conventions/development/frontend/`.

**6 open, 34 closed this pass.** Mechanically the tree is clean: 1078 links resolve, 72 `§` references
resolve, 0 unreachable docs, 0 missing timestamps, 4 lines over 120 (all pre-existing).

---

## Open — needs a decision

Each row is two live rules that disagree, where choosing changes what code does, or a naming preference with
no evidence favouring either side.

### 18 — `*State`, one suffix and two referents

- `visual/state.md:57` — *must end `*State` — the whole-region stand-in for content that is absent,
  pending, or failed.*
- `architecture.md:58` — *data `use{Entity}` returns `{Entity}State`*; `state-and-data.md:59` repeats it.
- Neither side is stale, and picking one renames real exports — `CodesState` reads as both.

---

### 62 — `*Field` provides, but the code consumes

- `visual/field.md` — a field **provides** the form-control context its child reads.
- The code inverts it: `ColorField` · `DateField` · `TimeField` · `DateTimeField` all call
  `useFormControl()`, while `ColorPicker` is what mounts `FormControlProvider`.
- Either the gate is wrong, or four components are named for a role they do not play.
- Found by the application pass, from the code side; no doc says it.

---

### 19 — `Skeleton`, claimed by two kinds

- `visual/state.md:17` lists it ✅, and `state.md:11` admits it — *must **replace** the content of a region,
  not sit beside it*.
- `visual/feedback.md:17` lists it ✅, but `feedback.md:14` excludes it — *must carry its own copy; a bare
  mark with no text is an [indicator]*.
- Not resolvable on the gates alone: `feedback.md:17` also lists `Spinner` and `ProgressBar`, which fail the
  same copy gate, and `state.md:18` explicitly sends `Spinner` to feedback. Moving `Skeleton` alone leaves
  the copy gate refuted by its own siblings.

---

### 22 — which framework a kind doc's example is written in

- `architecture.md:5` — *the slice tree a **React/TS** app is built on*; `naming.md:11` names `.ts` / `.tsx`
  only; `react/components.md:15` counts 281 SDK files.
- All 15 kind docs demonstrate every rule in ` ```vue ` fences, and `visual/provider.md:52` mandates
  `provide()` plus a `use{Capability}()` composable.
- Both frameworks ship. The fork is one example language, or both per doc.

---

### 49b — the suffix a primitive takes

- `constructs.md:42` — *must suffix every component, however well known the bare word is*.
- `visual/primitive.md:59` — *must take no suffix; the behaviour's own word is the whole name — `Slot` ·
  `Portal` · `Presence`*, routed by `visual/visual.md:72` as `none — the behaviour's own word`.
- The other five bare-name carve-outs are gone (**49a**, below). This one is not a carve-out but the kind's
  own fixed form; retiring it needs a suffix that does not exist yet, which runs `constructs.md`
  § *Adding a new suffix*.

---

### 56 — register bleed, with nowhere to move to

- `constructs.md:131` — *should reach for a `@wow-two-beta/ui` component before hand-rolling*.
- `constructs.md:141` — *must set Prettier `printWidth: 120`*.
- `hooks.md:27-28` — object return versus tuple return.
- `data/result.md:27` — *must reach for `AppError` first*.
- All four are the judgement register inside definition docs (`mla/components/components.md:12-16`).
  `mla/components/` holds only its own lead, so the fix writes the destination doc first — new content,
  not a repoint.

---

## Closed this pass — 34

### The failure carrier — row 4

`ApiError` no longer appears anywhere in the tree. `state-and-data.md:34-36` returns `Result<T>` and maps the
failure to `AppError`, its code fence reading through `isFail`; `submission.md:12-15` and `forms.md:23`
follow; `toApiError` → `toAppError` in the query matrix; `frontend-conventions.md:117` repointed.

---

### `screen` retired — row 60

Rewritten at `architecture.md:17` · `boundaries.md:11` · `page.md:63`,`:99` · `routing.md:60-61` ·
`forms.md:29`,`:60` · `submission.md:11` · `auth.md:6`,`:23` · `html/headings.md` (4 sites) ·
`html/landmarks.md` (6 sites). Left alone: `screen reader`, the Tailwind `*-screen` utilities, `off-screen`,
and `uploads.md:12`'s verb — none is a component word.

---

### The bare-name carve-out — row 49a

Five carve-out lines deleted — `control.md` · `layout.md` · `display.md` · `nav.md` · `field.md`. Neither
`visual.md:52` nor `naming.md:118` advertises "the bare names that take none" any more. The ✅ rosters in
those docs still carry bare entries (`Box`, `Combobox`, `Avatar`, `Pagination`); each needs a coined name, so
they ride with **49b**.

---

### One owner per rule — 12 rows

| # | Restated where | Owner it links to now |
|---|---|---|
| 5 · 34 | `architecture.md:53` · `react/components.md:27` | `constructs.md` § *Folder* |
| 12 | `boundaries.md:54` fixed `changeOrigin: false` | `state-and-data.md` § *API client* |
| 14 | `extensions.md` § JSDoc said `Provides` | `documentation.md` § *Verb starters* |
| 15 | `hooks.md` § Location put hooks in `src/hooks/` | `architecture.md` § *Sub-domains* |
| 16 | `extensions.md` § Location put them in `lib/` | `architecture.md` · `boundaries.md` |
| 24 | `architecture.md:56` restated `use{Noun}` | `hooks.md` § *Naming* |
| 36 | `state-and-data.md:60` retired hash routing | `routing.md:16` |
| 50 | `extensions.md:42` cited the wrong doc for `class` | `typescript.md` § *Absence* |
| 51 | `enums.md:102` named `constructs.md` as `is*` owner | `enums.md:76-78` keeps it |
| 52 | `hooks.md` § JSDoc restated the hook verbs | `documentation.md` § *Verb starters* |
| 53 | `imports.md:80` restated the React-UMD ban | `style.md` § *React types* |
| 54 | `visual.md` § Headless restated the keep-list | `headless-suffixes.md` |

Row 14 also picked the winner: `documentation.md:57` says `Extends`, and its own `:61` reserves `Provides`
for something else — so `extensions.md`'s example verb changed with it.

---

### Suffix and casing — 5 rows

| # | Was | Now |
|---|---|---|
| 10 · 32 | `extensions.md:46` mandated `UPPER_CASE` fields | casing is `naming.md`'s |
| 10 · 32 | its example ran `WHITESPACE_REGEX` | `WhitespaceRegex` · `DefaultInitials` |
| 11 | `routing.md:32` typed `readonly AppRoute[]` | `ReadonlyArray<AppRoute>` |
| 17 · 37 | `architecture.md` · `constructs.md` · `models.md:40`,`:50` said `*Request` | `*ApiRequest` |
| 20 | `state.md:17` listed `LoadingOverlay` as a state | dropped; `overlay.md:58` owns it |
| 25 | `props.md:58` passed `disabled` through unrenamed | off the native list, `is*` stated |

---

### Scope and vocabulary — 5 rows

| # | Was | Now |
|---|---|---|
| 7 | the five layers read as universal | `architecture.md:24-25` scopes them to a product |
| 8 | `constructs.md:83` excluded views and pages | applies to every rendering kind |
| 21 | `vue-sfc.md:29` mandated relative imports | scoped to a published library's `src/` |
| 23 | `typescript.md:67` allowed no boundary class | React's error boundary is the third case |
| 24b | `hooks.md` carried "composable" + `onScopeDispose` | one word — "hook"; teardown cites the two |

Row 7's pointer is `visual.md` § *Placement*; row 24b's are `vue/reactivity.md` and `react/hooks.md`, which
own the teardown seam.

---

### Index drift — 6 rows

| # | Was | Now |
|---|---|---|
| 13 | `models.md:48` bans `Registry`, `headless-suffixes.md:39` mandates it | two rules — `models.md:48` says which |
| 46 · 55 | `mla/components/` fixed `lla/components/` doc shape | § *Adding a doc here*, scoped to its folder |
| 57 | i18n · config · states · icons listed as gaps | all four ship; a11y + static assets remain |
| 58 | `visual.md:44` omitted the loading case's home | `display/` `feedback/` |
| 59 | three folders carry no `{folder}.md` | refuted by `conventions.md:90` |
| 61 | 18 docs sat beside `data/` | refuted — the recut left three folders |

Row 59: a folder holding one doc needs no lead, and `domains.md:26` now states the threshold.

---

### Also fixed in passing

- `typescript.md`'s `## Banned constructs` → `## Banned`, so `lla/constructs/constructs.md:27`'s pointer
  resolves in every one of the 40 group docs.
- `visual.md:74-75` split into two bullets, so the coining-gate `§` reference carries its own link.

---

## Mechanical checks

| Check | Count |
|---|---|
| relative links resolving | 1078 / 1078 |
| `§ *Section*` references resolving | 72 / 72 |
| docs with no inbound link | 0 |
| docs missing `*Last updated:*` | 0 |
| lines over 120 | 4 |

The four long lines predate this pass: `observability.md:20` · `css/css.md:14` · `html/html.md:22` ·
`vue-sfc.md:118`. The last is a single markdown link to a workbench path, which cannot wrap.
Measured with `LC_ALL=en_US.UTF-8 awk 'length($0)>120'`.

---

## Backend

- `conventions/development/backend/` needs the same SDK-vs-product split: an architecture doc states product
  structure only, and package/SDK layout moves to its own doc. Another chat owns that tree.

---

## Neighbours

- [frontend conventions](conventions/development/frontend/frontend-conventions.md) — the docs this audits
