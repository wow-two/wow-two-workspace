# Conventions — Development — Frontend

*Last updated: 2026-08-17*

> Conventions for every frontend under `wow-two-ws/`. Lookup table — open a file when the task
> touches it; do not pre-read. Cut by **scope**: how far a rule reaches.
> How to write a doc here → template + rules in [conventions](../../conventions.md).

## The three scopes

| Scope | Reaches | Holds |
|---|---|---|
| `lla/` | one symbol | naming · doc blocks · file layout · banned constructs |
| `mla/` | one app, and everything it talks to | `components/` · `architecture/` · `platform/` · `domains/` |
| `hla/` | between our own frontends | micro-frontend composition · shared runtime · cross-app routing · a shared session |

**Routing.** A kind of thing you declare → `mla/components/{kind}.md`. How any symbol is written → `lla/`.
Where a type lives → `mla/architecture/`. How the app builds and boots → `mla/platform/`. A concrete
technology or capability → `mla/domains/{domain}/`. A rule spanning apps we both own → `hla/`.

**Only `lla/` is language-bound.** It is TypeScript, and it needs no language folder because TypeScript is the only
frontend language; a second one would add `lla/{lang}/`. `mla/` and `hla/` are not TypeScript's — a layer, a Tailwind
token and a micro-frontend contract are none of them properties of the language, so nothing nests under it.

**The framework is a provider, not a scope.** Vue and React sit inside `mla/`, in the folder whose contract they
implement — the same shape the backend uses for `persistence/{ef,dapper,sql}`. A rule true of both frameworks lives
in the lead; only the delta gets a `vue/` or `react/` folder. Nothing framework-shaped ever reaches `lla/`.

**The test between `mla/` and `hla/`:** do we own both ends? A third-party widget is adapted in `mla/`, never contracted in `hla/`.

**The test between baseline and a domain:** would the rule survive if the feature were deleted? Yes → baseline. No → the domain that owns it.

---

## What each scope owns

### `lla/` — one symbol
What **TypeScript itself** defines, plus how we write it down: names, doc blocks, file layout, and the constructs
banned outright. The test is whether the language supplies the term. `Dto`, `Entity`, `Component` are ours and
aligned to our architecture, so they are `mla/` however familiar they look. This is the layer Vue and React share
entirely.

### `mla/` — one app
Four buckets. `components/` = what am I building, one file per role. `architecture/` = where it lives — the five
layers and the slice tree. `platform/` = how the app builds, styles and serves. `domains/` = a capability, its
contract and its providers.

- **A component has one home layer.** A kind is declared and documented in one layer even when used from others.
- **The SDK boundary.** *How to use* and *what to use* from `@wow-two-beta/ui` is a convention and lives here; the
  SDK's own internals live in the SDK's docs.

### `hla/` — between our own frontends
Rules that only exist once one frontend has to agree with another at runtime. The SDK **targets** this scope; it has
simply shipped nothing into it yet, the same way the backend names it ahead of gRPC and the gateway.

---

## Files

### `lla/` — language level

| Level | Answers | Lives in |
|---|---|---|
| **construct** | what TypeScript offers, and which of it we use or forbid | [constructs](lla/constructs/constructs.md) |
| **role** | what a construct may stand for, and the starter that follows | [components](lla/components/components.md) |
| **definition** | the whole thing — file, name, doc, content | each component's own file |

| Folder | Holds |
|---|---|
| [constructs/](lla/constructs/constructs.md) | every TS construct, what each is for, construct-level bans |
| [components/](lla/components/components.md) | [constants](lla/components/constants.md) · [enums](lla/components/enums.md) · [extensions](lla/components/extensions.md) — the roles that need no app around them |
| [notation/](lla/notation/notation.md) | [naming](lla/notation/naming/naming.md) · [documentation](lla/notation/documentation/documentation.md) · [style](lla/notation/style/style.md) · [imports](lla/notation/style/imports.md) |

**Membership in `components/`** — a role passes only when it owns **both its shape and its role with no app around it**.
A `Component` fails: it needs a renderer. A `Hook` fails: it needs a component tree. Those land in `mla/components/`.

**Notation is a default set** — every rule there applies to every symbol, and a component may override it in its own
file. A component that does not override cites `notation/` rather than restating it.

---

### `mla/components/` — a kind of thing you declare

| File | What it covers |
|---|---|
| [components](mla/components/components.md) | One-per-folder, `readonly` props, `{Component}Props` |
| [component catalog](mla/components/component-catalog.md) | What exists, by kind — screens · views · controls · fields · displays |
| [hooks](mla/components/hooks.md) | `use*` naming, object vs tuple return, abort on unmount |
| [models](mla/components/data/models.md) | The `*Dto` family · `*Content` · `*Request` · descriptor / catalog · field nullability |
| [vue SFC](mla/components/vue/vue-sfc.md) | The Vue delta — blocks, macro order, emit / slot / computed verbs, `useAttrs`, `@vue-ignore` |

### `mla/architecture/` — where a type lives

| File | What it covers |
|---|---|
| [architecture](mla/architecture/architecture.md) | The five layers (`bootstrap` · `integration` · `domain` · `application` · `presentation`) × domain slices · inward dependency · packaging · SDK extraction · the role→suffix table |

### `mla/platform/` — how the app is built, styled and served

| File | What it covers |
|---|---|
| [styling](mla/platform/styling.md) | Tailwind v4 `@import` / `@theme`, tokens, `cn()`, `tailwind-variants`, dark mode |

### `mla/domains/` — a capability, its contract and its providers

The shape every domain follows, the built four and the eleven recognized → [domains](mla/domains/domains.md).

| Domain | What it covers |
|---|---|
| [data](mla/domains/data/state-and-data.md) | Same-origin `/api` client, dev proxy, `ApiError` / ProblemDetails, server-state vs UI-state |
| [forms](mla/domains/forms/forms.md) | The engine pin, `*Values` + schema, field chrome, ProblemDetails → field errors |
| [routing](mla/domains/routing/routing.md) | The route contract and its router providers |
| [api](mla/domains/api/type-mapping.md) | The .NET ↔ wire ↔ TS scalar contract — `Guid` · `Temporal.*` · enums · `ReadonlyArray<T>` |

---

## Open

Not yet covered — write each as a focused file when the supporting practice lands in a repo.

| Gap | Why it matters |
|---|---|
| **Accessibility** | No keyboard / ARIA / focus baseline; the SDK ships the primitives, consumer rules are unstated |
| **i18n** | EN / RU / UZ handled ad-hoc; no locale convention, and it gates the enum-label → backend-translation move |
| **Environment & config** | `import.meta.env` handling, build-time vs runtime config, the secrets boundary |
| **Error & loading states** | `ApiError` exists; error boundaries, skeletons and empty states have no shared pattern |
| **Icons & assets** | `lucide-*` is the de-facto icon set but unwritten; static-asset handling unspecified |

Resolved and removed since the previous index: routing (→ `mla/domains/routing/`), formatting and linting
(Prettier at 120 + ESLint `max-len`), the server-state library (TanStack Query, in the SDK), and the testing
stance (the four-gate ladder).
