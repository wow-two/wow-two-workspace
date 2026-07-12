# Conventions — Development — Frontend (React / TypeScript)

*Last updated: 2026-07-10*

> React 19 / TypeScript (strict) / Vite / Tailwind v4 / `@wow-two-beta/ui` code-style conventions for
> every frontend under `wow-two-ws/`. Lookup table — open a file when the task touches it; do not
> pre-read. Repo layout is one level up: [../repo/structure/repo-structure.md](../repo/structure/repo-structure.md). The .NET
> sibling: [../backend/](../backend/).

## code-style/

| File | What it covers |
|---|---|
| [naming.md](code-style/naming.md) | Files PascalCase (barrels lowercase), folders camelCase, `*Extensions`/`*Styles`/`*Helpers` suffixes, exports |
| [imports.md](code-style/imports.md) | `import` layout — 5 group order (side-effect / third-party / SDK / `@/` / relative) blank-line-separated · alphabetical intra-group · inline vs standalone `type` · published-subpath + `@/`-over-relative rules |
| [documentation.md](code-style/documentation.md) | JSDoc one-liner rule + verb-starter table (Defines / Renders / Manages / Provides) |
| [code-organization.md](code-style/code-organization.md) | `const`/`let`, `// ── Section ──` dividers, 7-group import order, React named-type imports (no UMD `React.*`), file-internal order |
| [models.md](code-style/models.md) | The `*Dto` family (entity/form/sub-model) · `*Content` · `*Request` · descriptor/catalog · fields (`T` / `T?`) · `interface`/`type` · doc rules (`Defines` type / `The …` member, blank line between members) |
| [type-mapping.md](code-style/type-mapping.md) | The .NET ↔ wire ↔ TS scalar contract — `Guid`/`number`/`boolean` · `Temporal.*` dates wired by one global reviver · enums · `ReadonlyArray<T>` (never `T[]`) · `?`-nullability |
| [enums.md](code-style/enums.md) | const object `as const` — PascalCase key / camelCase value · derived `type` · `Unresolved` first · `//` comment · `Displays` (presentation) + `Payloads` (backend) extensions |
| [constants.md](code-style/constants.md) | PascalCase scalars / data · `as const` · JSDoc one-liner · const-vs-enum decision |
| [extensions.md](code-style/extensions.md) | `{Noun}Extensions` `as const` objects (no class/namespace) — the C# static-helper analog |

## architecture/

| File | What it covers |
|---|---|
| [architecture.md](architecture/architecture.md) | **Layer model** — `bootstrap · integration · domain · application · presentation` × domain slices · inward dependency · `common/` · barrels · naming vocabulary · discriminated dispatch · **packaging** (single-app vs pnpm workspace + `@{brand}/*` + boundaries) · dev server + preview |
| [state-and-data.md](architecture/state-and-data.md) | Same-origin `/api` client, dev proxy, `ApiError`/ProblemDetails, Context+hooks, localStorage keys |

## presentation/

| File | What it covers |
|---|---|
| [components.md](presentation/components.md) | One-component-per-folder, props (`readonly`, **destructure** w/ inline defaults), file structure, UI terminology, variants |
| [component-catalog.md](presentation/component-catalog.md) | The reference frontend's components by **kind** (screens · views · controls · fields · displays) — a "what exists" lookup |
| [forms.md](presentation/forms.md) | `useAppForm` engine pin (`src/form.ts`) · `*Values` + zod schema · `form.Field` × `Field` chrome · ProblemDetails → field errors · `validateOn` · arrays · `form.engine` escape hatch · house-engine `play()` stories |
| [hooks.md](presentation/hooks.md) | `use*` naming, object vs tuple return, `Manages`/`Provides access to`, abort on unmount |
| [styling.md](presentation/styling.md) | Tailwind v4 `@import`/`@theme`/`@source`-ing `@wow-two-beta/ui`, tokens, `cn()`, `tailwind-variants`, dark mode |

## Notes

- Initial extraction (2026-06-09) generalized from Haven's `frontend-development-guidelines.md` +
  `frontend-architecture.md`, the `@wow-two-beta/ui` `CLAUDE.md`, and current drydock practice.
- Haven-specifics stripped: `@haven/*` → `@{brand}/*`; Supabase/n8n/i18n details dropped as product-level.
- These apply to **every** frontend repo under `wow-two-ws/`; a repo-level rule overrides for that repo.
- Backend sibling: [../backend/](../backend/).

## Gap analysis — conventions still missing

Not yet covered (no source content exists, or needs a deliberate decision). Prioritized; write each as a
focused file when the supporting practice lands in a repo.

### P1 — needed before more apps ship

| Gap | Why it matters | Note |
|---|---|---|
| **Testing** | Beta UI is explicitly "no tests"; products need a real stance (Vitest + RTL? Playwright? what's required vs optional) | No FE test convention exists in any source today |
| **Error & loading states** | `ApiError` exists ([state-and-data.md](architecture/state-and-data.md)) but no shared pattern for error boundaries, loading skeletons, empty states (`EmptyState`/`Alert`/`Spinner` exist in beta UI but usage isn't codified) | Partially implied; needs its own file |
| **Routing** | Today: URL-hash routing for light apps. No decision for multi-route apps (React Router? TanStack Router? file-based?) | `useHashRouter` is Haven-only; not generalized |

### P2 — soon

| Gap | Why it matters |
|---|---|
| **Accessibility (a11y)** | No keyboard/ARIA/focus-management baseline; beta UI uses Radix/floating-ui primitives but consumer rules aren't stated |
| **i18n** | Haven landing uses EN/RU/UZ ad-hoc; no shared translation/locale convention (ties into the enum label-Record → backend-translation migration) |
| **Server-state / data-fetching library** | Current rule is hand-rolled hooks + `fetch`. If TanStack Query (or similar) is adopted, caching/invalidation/retry conventions need codifying |
| **Environment & config** | `.env`/`import.meta.env` handling, build-time vs runtime config, secrets boundary |

### P3 — later

| Gap | Why it matters |
|---|---|
| **Code-splitting / performance** | Lazy `React.lazy`/`Suspense` boundaries, bundle budgets, `default` export carve-out exists but no perf guidance |
| **Linting / formatting** | ESLint flat-config + Prettier baseline (beta UI uses `eslint-plugin-boundaries`; products have no stated config) |
| **Icons & assets** | `lucide-react` is the de-facto icon set but it's not written as a rule; static asset handling unspecified |
| **Storybook** | Required in the beta UI library; unspecified (likely not required) for product apps |
| **Analytics / logging** | Client error reporting + telemetry boundary (intersects the GWDNBM no-engagement-bait principle) |
