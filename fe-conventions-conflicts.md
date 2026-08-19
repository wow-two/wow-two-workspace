# Frontend conventions — rule conflicts

*Last updated: 2026-08-19*

> Defects **inside** the conventions: two docs stating opposite verdicts on one identifier, a rule refuted by
> its own example, the index describing a doc differently from the doc itself, or one rule restated in a second
> doc instead of linked ([conventions.md](conventions/conventions.md) § *One owner per rule*).
> Purpose — a rule that contradicts another cannot gate code; every row here needs a verdict, not a sweep.
> Use case — pick a row, decide the winning side, edit both docs, tick it. Code debt lives in the SDK's
> [conventions sweep](workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/planning/ui-sdk-conventions-sweep.md).

Re-measured 2026-08-19, after the de-duplication pass removed ~940 lines across 68 docs. Coordinates are current.
Paths are relative to `conventions/development/frontend/`.

**28 open.** The `suffixes.md` dissolve closed 13 — every row where a kind doc cited a list that doc never carried.

---

## Cross-doc contradictions — 20

| # | Identifier | Doc A says | Doc B says |
|---|---|---|---|
| 4 | API failure carrier | `data/result.md:24`,`:28` — return a `Result`, never throw | `state-and-data.md:34` · `submission.md:12` · `forms.md:23` — throw `ApiError` |
| 5 | one component per folder | `components.md:23-26` — SDK must, an app may flatten | `architecture.md:52` · `react/components.md:27` · `frontend-conventions.md:62` |
| 7 | capability modules vs 5 layers | `architecture.md:14-20` — five layers | `headless-suffixes.md:12` · `provider.md:27` · `primitive.md:27` |
| 8 | `components.md` § Folder scope | `components.md:30` — excludes views and pages | `page.md:34` · `view.md:32` · 11 more kind docs at `:32` |
| 10 | constant casing | `naming.md:93` · `constants.md:17` — PascalCase | `extensions.md:46` — `UPPER_CASE` fields |
| 11 | `T[]` / `readonly T[]` | `typescript.md:44`,`:96` · `type-mapping.md:74` | `routing.md:32` — `readonly AppRoute[]` |
| 12 | `changeOrigin` | `boundaries.md:54` — `false` | `state-and-data.md:20` — `true` |
| 13 | `*Registry` | `models.md:47` — `Catalog`, not `Registry` | `headless-suffixes.md:38` keep-list |
| 14 | `{Noun}Extensions` doc verb | `documentation.md:57` — `Extends` | `extensions.md:53`,`:16` — `Provides` |
| 15 | hook home | `architecture.md:18`,`:42` — `application/{domain}/hooks/` | `hooks.md:19-20` — `src/hooks/` |
| 16 | `{Noun}Extensions` home | `architecture.md:19` — `domain/` | `extensions.md:61-63` — `lib/` |
| 17 | write-contract suffix | `models.md:32` — `*ApiRequest` | `architecture.md:56` — `*Request` |
| 18 | `*State` | `suffixes.md:83` · `state.md:17` — a component | `architecture.md:55` · `state-and-data.md:58` — a data type |
| 19 | `Skeleton` | `state.md:17` — a state | `feedback.md:17` — a feedback, and `:13` excludes a content stand-in |
| 20 | `LoadingOverlay` | `state.md:17`,`:28` — a state | `overlay.md:17`,`:27` · `suffixes.md:17` — an overlay |
| 21 | app-internal import path | `imports.md:84` — the `@/` alias | `vue-sfc.md:29-30` — relative paths |
| 22 | component construct | `architecture.md:5` · `naming.md:11` — React, `.ts`/`.tsx` | ` ```vue ` examples in all 15 kind docs |
| 23 | `class` | `typescript.md:67` — `Error` subclass or builder | `react/boundaries.md:28` — an error boundary |
| 24 | hook naming | `architecture.md:55` — `use{Noun}` | `hooks.md:11` |
| 24b | React/Vue vocabulary in one doc | `hooks.md:54-56`,`:62` — "composable" + `onScopeDispose` inside a React doc | — |
| 36 | URL-hash routing | `state-and-data.md:60` — retired | `routing.md:84` — `[x] history:'hash'` shipped |

---

## Rule refuted by its own example — 3

| # | Identifier | Rule says | Its own example says |
|---|---|---|---|
| 25 | `disabled` | `props.md:58` — a DOM attribute passes through unrenamed | `props.md:66`,`:78` — `isDisabled` |
| 32 | `WHITESPACE_REGEX` | `naming.md:93` · `constants.md:17` | `extensions.md:19`,`:21`,`:46` |
| 37 | write-contract suffix, inside one doc | `models.md:17`,`:32` — `*ApiRequest` | `models.md:39`,`:48`,`:50` — `*Request` |

---

## Index drift — 4

| # | Where | Drift |
|---|---|---|
| 33 | `frontend-conventions.md:70-71` | names `screen` among the kind docs; no `screen` kind exists |
| 34 | `frontend-conventions.md:62` | calls one-per-folder unconditional; `components.md:26` scopes it to the SDK |
| 35 | `frontend-conventions.md:39-40` | lists `service-free` `constants` `enums` `extensions` under `lla/`; all live in `mla/components/` |
| 38 | `frontend-conventions.md:14` · `mla/mla.md:20-27` | both omit `frameworks/` from `mla/`'s buckets, which `:84` documents |

---

## Structural — `service-free.md`

| # | What |
|---|---|
| 46 | `:30`,`:34-38` mandate a `## Location` → `## Declaration` → `## Content` shape that `constants.md`, `enums.md` and `extensions.md` do not carry |
| 47 | `:6` says keep the app-free roles out of MLA; `:12` says place an inert one in `mla/components/`, where the file itself sits |
| 48 | its H1 is `# Components`, colliding with `components.md`; `notation.md:32` and `constructs.md:37` both link it as "components" |

---

## Closed

| Identifier | Closed by |
|---|---|
| `*Dto` reach past `integration/` · its `Invoice` example · `*Input` as a form model | the `models.md` rewrite |
| acronym `JSONEditor` in `suffixes.md:88` | `JsonEditor` |
| barrel import vs the slice's public surface, and its own `:40-41` example | `imports.md:89` restated as *the barrel that owns it* |
| `T \| null` banned vs `use with care`, and `typescript.md:47` | scoped — absence is `field?: T`, a stated `null` is a prop value |
| `presentation/{kind}/` vs domain slicing | kind folders are SDK layout; a product slices by domain |
| props destructuring | `components.md:56-58` scopes access per framework |
| three broken `§` anchors — `css.md:39` · `react/boundaries.md:32` · `routing.md:72` | repointed to headings that exist |
| 9 citations pointing at lists `suffixes.md` never carried | the dissolve — each kind doc owns its own names |
| `suffixes.md` as a central keep-list | dissolved; 15 kind docs · `components.md` § *Naming* · `component-catalog.md` routing |
| 4 rows where a kind doc's example refuted `suffixes.md` | the same dissolve — the kind doc now owns the rule its example shows |
| acronym casing — docs showed the SDK's real all-caps names | renamed in code and docs together, 4 gates green |

---

## Restated rules

Swept 2026-08-19 across four disjoint lanes — ~940 lines removed from 68 docs. What the pass created is tracked
above as rows 39-45. The meta rule is [conventions.md](conventions/conventions.md) § *One owner per rule*.

---

## Backend

- `conventions/development/backend/` needs the same SDK-vs-product split: an architecture doc states product
  structure only, and package/SDK layout moves to its own doc. Another chat owns that tree.

---

## Neighbours

- [frontend conventions](conventions/development/frontend/frontend-conventions.md) — the docs this audits
- [handoff](fe-sweep-handoff.md) — session state
