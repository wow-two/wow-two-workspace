# Conventions — Development — Frontend

*Last updated: 2026-08-19*

> Conventions for every frontend under `wow-two-ws/`. Lookup table — open a file when the task
> touches it; do not pre-read. Cut by **scope**: how far a rule reaches.
> How to write a doc here → template + rules in [conventions](../../conventions.md).

## The three scopes

| Scope | Reaches | Holds |
|---|---|---|
| `lla/` | one symbol | constructs per platform · a form used end to end · naming · doc blocks · style |
| `mla/` | one app, and everything it talks to | six buckets → [mla](mla/mla.md) |
| [`hla/`](hla/hla.md) | between our own frontends | micro-frontend composition · shared runtime · cross-app routing |

**Routing.** A role you declare over and over → `mla/constructs/{role}.md`; which one to reach for, and with
what values → `mla/components/`. A language form used end to end → `lla/components/{form}.md`; how any
symbol is written → `lla/notation/`.
Where a type lives → `mla/architecture/`. How the app builds and boots → `mla/platform/`. A concrete
technology or capability → `mla/domains/{domain}/`. A rule spanning apps we both own → `hla/`.

- only `lla/` is platform-bound — a layer, a domain contract and a micro-frontend seam belong to the app, so
  nothing nests under a platform outside `lla/constructs/`.
- what a framework *offers* is a construct (`defineProps`, `useState`); how we *build a component* with it is
  `mla/`. Each cites the other rather than restating it.
- a framework is a **provider** inside a domain — `vue/` and `react/` are provider folders, the shape the
  backend uses for `persistence/{ef,dapper,sql}`.
- the test between `mla/` and `hla/`: do we own both ends? A third-party widget is adapted in `mla/`.
- the test between baseline and a domain: would the rule survive if the feature were deleted?

---

## `lla/` — one symbol

The test is whether TypeScript, a framework or the browser supplies the term; `Dto`, `Entity` and `Page`
are ours, so they sit in `mla/` however familiar they read.

- [constructs](lla/constructs/constructs.md) — one folder per platform: every construct, what each is for,
  and its ban.
- [components](lla/components/components.md) — a language form used end to end:
  [constants](lla/components/constants.md) · [enums](lla/components/enums.md) ·
  [extensions](lla/components/extensions.md).
- [notation](lla/notation/notation.md) — [naming](lla/notation/naming/naming.md) ·
  [props](lla/notation/naming/props.md) · [documentation](lla/notation/documentation/documentation.md) ·
  [style](lla/notation/style/style.md) · [imports](lla/notation/style/imports.md).

- `constructs/` states the form and the verdict on writing it; `components/` carries that same form through
  declaring, keeping, wiring and reading it.
- a role **we** coined is never `lla/` — `Page`, `Overlay`, `Model` and `Result` are ours, so they sit in
  `mla/constructs/`, and the judgement over them in [`mla/components/`](mla/components/components.md).
- notation is a **default set** — a component may override a rule in its own file, and one that does not
  override cites `notation/` rather than restating it.

---

## `mla/` — one app

The scope lead and the SDK boundary → [mla](mla/mla.md).

---

## `mla/constructs/` — what a role is

| File | What it covers |
|---|---|
| [constructs](mla/constructs/constructs.md) | One-per-folder, `readonly` props, naming, the suffix gate |
| [component catalog](mla/constructs/component-catalog.md) | The index of kinds, and which suffix routes to which |
| [headless suffixes](mla/constructs/headless-suffixes.md) | The keep-list for a seam — `*Client` · `*Bus` |
| [hooks](mla/constructs/hooks.md) | `use*` naming, object vs tuple return, abort on unmount |
| [data](mla/constructs/data/data.md) | The `*Dto` family, `*Model`, `*Content`, and the `Result` carrier |

The fifteen kind docs are linked one per row from the
[component catalog](mla/constructs/component-catalog.md) — `page` through `primitive`. A kind doc says what the
kind **is**; one component's own props, slots and states belong to its `{Component}.spec.md` in the SDK repo.

---

## `mla/components/` — which one to reach for, and with what values

- [components](mla/components/components.md) — the three registers, the gate, and the authoring template.

The folder carries the judgement register only. `constants`, `enums` and `extensions` are forms TypeScript
supplies, so they sit in [`lla/components/`](lla/components/components.md).

---

## `mla/architecture/` — where a type lives

- [architecture](mla/architecture/architecture.md) — five layers × domain slices, inward dependency, the
  slice tree, compound components.
- [boundaries](mla/architecture/boundaries.md) — in-app restraint, the SDK-extraction trigger, packaging,
  the dev server.

---

## `mla/frameworks/` — the framework delta

- [react](mla/frameworks/react/react.md) — [components](mla/frameworks/react/components.md) ·
  [hooks](mla/frameworks/react/hooks.md) · [jsx](mla/frameworks/react/jsx.md) ·
  [boundaries](mla/frameworks/react/boundaries.md).
- [vue](mla/frameworks/vue/vue.md) — [SFC](mla/frameworks/vue/vue-sfc.md) ·
  [composition](mla/frameworks/vue/composition.md) · [macros](mla/frameworks/vue/macros.md) ·
  [reactivity](mla/frameworks/vue/reactivity.md) · [template](mla/frameworks/vue/template.md) ·
  [builtins](mla/frameworks/vue/builtins.md).

---

## `mla/platform/` — how the app is built, styled and served

- [styling](mla/platform/styling.md) — Tailwind v4 `@import` / `@theme`, tokens, `cn()`, variants, dark mode.

---

## `mla/domains/` — a capability, its contract and its providers

One row per domain, its contract and its shipped providers → [domains](mla/domains/domains.md). The four with
the most surface: [data](mla/domains/data/state-and-data.md) (the `/api` client, dev proxy, `ApiError`) ·
[forms](mla/domains/forms/forms.md) (engine pin, values, schema, field chrome) ·
[submission](mla/domains/forms/submission.md) (submit path, field errors, validation timing) ·
[api](mla/domains/api/type-mapping.md) (the .NET ↔ wire ↔ TS scalar contract).

---

## Open

| Gap | Why |
|---|---|
| **Accessibility** | No keyboard / ARIA / focus baseline; the SDK ships primitives, consumer rules unstated |
| **i18n** | EN / RU / UZ handled ad-hoc; no locale convention, and it gates the enum-label move |
| **Environment & config** | `import.meta.env`, build-time vs runtime config, the secrets boundary |
| **Error & loading states** | error boundaries, skeletons and empty states share no pattern |
| **Icons & assets** | `lucide-*` is the de-facto icon set but unwritten; static-asset handling unspecified |
