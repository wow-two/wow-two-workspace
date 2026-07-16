# Frontend Architecture

*Last updated: 2026-07-07*

A React/TS app is a Clean-Arch stack — layers at `src/` root, each sliced by domain, one inward dependency direction. Drill down: **layer → domain → sub-domain → file**.

## Layers — the top-level split

Five layers at `src/` root (no `layers/` wrapper). Dependency runs **inward**: `presentation → application → domain` · `integration → domain` · `bootstrap` wires all.

- **`bootstrap/`** — the composition root. `App.tsx` · `main.tsx` · `index.css` · providers · `routes.tsx` · layouts. Wiring only, no feature logic. *(backend peer: Host)*
- **`presentation/`** — pure UI: components + screens. Renders; never fetches. e.g. `ShapeControls` · `CreateCodeScreen`. *(Presentation)*
- **`application/`** — stateful use-cases: orchestration hooks (`useCodes`), view-model mappers (`toCodeRow`), validation + submit orchestration, client-state logic. *(Application)*
- **`domain/`** — the model: types, enums, extensions, and the model's pure ops (`build` / `parse` / `validate` / `encode`). Depends on nothing. *(Domain)*
- **`integration/`** — stateless adapters: HTTP client, endpoint fns (`createCode()`), interceptors, auth. Returns wire DTOs; no React. *(Infrastructure)*

- must not import **sideways** — `domain/codes` ↛ `domain/identity`; share via `common/` or lift a layer.
- `common/` + `bootstrap/` are import-exempt; should lint the rule (ESLint `no-restricted-paths` / import-linter) — unlinted layering rots.

## Domains — each layer sliced

- must slice every layer by domain — `codes` · `identity` · `billing` · `marketing`.
- must give each layer a **`common/`** slice for cross-domain items (a type / hook / api used by ≥ 2 domains).
- a domain appears once per layer it touches — `presentation/codes/` · `application/codes/` · `domain/codes/` · `integration/codes/`.

## Sub-domains — a domain splits as it grows

- a domain divides into cohesive **sub-domains** — `codes` → `core` (the QR builder) + `content` (per content-type).
- must fold a concern into a sub-domain once it owns ≥ 3 components — otherwise keep it flat.
- e.g. `domain/codes/core/` (module · finder · preview · rule) · `domain/codes/content/` (one module per content type).
- a sub-domain may itself **divide by concern** as it grows — `presentation/codes/core` → `design` · `shape` · `routing` · `preview` (a noun per concern).
- a component sub-domain may hold its components **directly** (`core/design/FillControls.tsx`); the `components/` wrapper is optional — use it only to separate non-component files (hooks, helpers). Keep one style within a domain.
- **two kinds of folder** inside a domain: a **sub-domain** (a model noun — `core` · `content` · `design`) and a **role-group** (a role word — `models/` · `enums/` · `screens/` · `components/` · `hooks/`). A role-group is never a sub-domain. Model files live in a `models/` role-group and enum files in an `enums/` role-group (mirrors the backend), symmetric with `components/` / `hooks/`.
- **domain-level `common/`** — the home for whatever belongs to no single sub-domain: cross-sub-domain **shared** components/hooks (e.g. a `PresetIconButton` used by `design` + `shape`) **and** the domain's **composition** role-groups. Symmetric with the layer-level `common/` (cross-domain).
- **routed screens** compose sub-domains, so they belong to none — they live under domain-`common/`: `presentation/{domain}/common/screens/`, never as a peer to the sub-domains.

## Files — where general naming applies

- files `PascalCase`, folders `camelCase`, one lowercase `index.ts` **barrel** per slice (its only public surface) — per [naming.md](../code-style/naming.md).
- one component per its own folder ([components.md](../presentation/components.md)); hooks `use{Noun}` ([hooks.md](../presentation/hooks.md)); types — `*Dto` (entity · form · sub-model) / `*Content` / `*Request` ([models.md](../code-style/models.md)).
- **role-specific naming** (component-role suffixes, type/api/const markers) → the [Naming](#naming--role--suffix) section below.

## Naming — role → suffix

*(SDK-grounded role vocabulary. A few forks still open — see the end of this section.)*

Name a **component** by its role (SDK-grounded categories):

**Composition / horizons**

| Role | Suffix |
|---|---|
| shell (navbar + chrome) | `*Layout` |
| routed content | `*Page` |
| sub-view (display mode) | `*View` |
| tab content | `*Tab` |
| collapsible section | `*Section` |
| overlay (blocking) | `*Modal` |
| bordered container | `*Card` |
| conditional-render guard | `*Gate` |

**Forms & control sets** — *submit-ownership decides `*Form` vs `*Controls`*

| Role | Suffix |
|---|---|
| submittable form | `*Form` |
| submittable editor (edit content with a format) | `*EditorForm` |
| subject control set (embedded, no submit) | `*Controls` |
| homogeneous group of one control | `{Control}Group` |

**Atomic controls**

| Kind | Suffix |
|---|---|
| raw typeable | `*Input` |
| labeled control (clickable / selectable) | `*Field` |
| panel selector (large / continuous space) | `*Picker` |
| action (no value) | `*Button` |
| generic labeled wrapper | `Field` |

- `Field` = the generic wrapper · `*Field` = a specific labeled control (`SelectField`) · a raw unlabeled widget keeps its bare name (`Select` · `Switch`). No `Form` prefix outside the submittable `*Form`.

**Display & feedback**

| Role | Suffix |
|---|---|
| asset / media render | `*Preview` · `*Carousel` · `*Gallery` |
| tabular | `*Table` · `*Grid` · `*Row` · `*Cell` |
| status chip | `*Badge` · `*Tag` · `*Status` |
| inline note | `*Callout` |
| hover popup | `*Tooltip` |
| transient note | `*Toast` |
| section note | `*Alert` · `*Banner` |
| dynamic renderer | `*Renderer` |
| context | `*Provider` (+ `*Context`) |

- modifiers: `Overlay*` prefix (positioned variant) · `*Compact` suffix (condensed).
- **hooks** — `use{Noun}`; data `use{Entity}` returns a `{Entity}State` object, UI `use{Feature}`.
- **types** — `*Dto` marks every data model (entity `CodeDto` · form `CreateEdit*Dto` · sub-model · `*RowDto` · `*QueryDto`), placed by role in `domain` / `application` / `integration` · `*Request` (write contract, `integration`) · `*Content` (variant) · `*Props` · `*State` (hook) · enum bare + `{Enum}Labels`. Full scheme → [models.md](../code-style/models.md).
- **api** — `integration/{domain}` exports `{domain}Api`; fns `{verb}{Noun}`; `ApiError`; private `request<T>`.
- **constants** — PascalCase; **extensions** — `{Noun}Extensions` (`as const`).
- **unresolved forks:** hook file casing (`useX.ts` vs `UseX.ts`) · enum labels (`{Enum}Labels` vs `{ENUM}_LABEL`) · api object (`{domain}Api` vs `api`).

### Compound (namespaced) components

A distinct **structural** category (orthogonal to the role suffix): a **root + tightly-coupled subparts** consumed as `Root.Sub` — `Modal.Content` · `Drawer.Body` · `Table.Row` · `Tabs.Panel` · `Menu.Item` · `Toolbar.Button` · `Collapsible.Trigger` · `List.Item`. The root keeps its role name (`*Modal` overlay · `*Table`/`List`/`Tree` display · `Menu`/`Toolbar` action-set); the subparts are the pieces that only exist inside it.

- use it when a component owns **≥ 2 subparts that only make sense inside it**. A lone add-on stays a flat sibling.
- name each subpart `Root{Part}` and export it **flat** (`ModalContent`, `TableRow`) **and** attach it as a `Root.Sub` static — flat form is tree-shakeable, namespace form is ergonomic. Ship both.
- **type the NAMED export** via `Object.assign`, so `import { Modal }` + `<Modal.Content>` type-checks (barrels re-export the *named* binding via `export *`; the `default` export is not re-exported):

```ts
function ModalRoot(props: ModalProps) { … }          // private root — forwardRef roots: `const ModalRoot = forwardRef(function Modal…)`
ModalRoot.displayName = 'Modal';                     // preserve the DevTools name for plain-fn roots
export const ModalContent = …;                       // flat subparts stay exported
export const Modal = Object.assign(ModalRoot, { Content: ModalContent, Header: ModalHeader, … });
export default Modal;                                // optional back-compat; not what barrels use
```

- **anti-pattern (banned):** `type XComponent = typeof X & {…}; (X as XComponent).Sub = …; export default X as XComponent;` — the statics' type lands only on `default`, so the barrel-exported *named* `X` is untyped and `<X.Sub>` fails to type-check for consumers **and** stories.

## Routing & responsive surfaces

A **place** is a URL; a **route renders the same place at every breakpoint** — never fork routes or redirect by device width.

- **places → pages** (`*Page`, one route) — a record, a detail view, `new-*`, settings. Deep-linkable, refreshable, shareable (a permalink relies on this).
- **actions → modals** (`*Modal` / sheet, **no route**) — format pickers, confirms, quick-filters. Ephemeral, no URL → no cross-size mismatch.
- must **not** render the same place as a modal on desktop and a page on mobile — that mismatch is what breaks copy-paste / refresh / back.
- a direct hit / refresh / new tab on any place-route must resolve to a **standalone page**. A desktop "modal-over-context" for a place is allowed **only** via intercepting-routes carrying that standalone-page fallback — otherwise default to a page.
- responsiveness lives in the **component, not the route**: a `*Modal` presents as `Modal` (desktop) ↔ `BottomSheet` / full-height sheet (mobile); a `*Page` reflows. Same route, adaptive render.

## Discriminated dispatch

- must model a variant set (e.g. content types) as a **discriminated union** on a `type` field.
- must dispatch via a `Record<{Id}, Spec>` registry — exhaustive by construction (a missing variant is a compile error: the TS analog of a C# exhaustive `switch`).
- static vs dynamic is a `mode` field on the spec — one switch in the screen gates the rules / fallback UI; no `if (static)` scattered *(baseline — refine later)*.

## Restraint

- must start at the screen; extract a shared component / hook only when a second consumer is real — no speculative widgets / features (the FSD 2.x lesson).

## Future

- **application ports** — once frontend testing is established, `application` may declare a port interface that `integration` implements, for test doubles (the backend abstraction↔adapter seam). Idea-logged, not adopted yet.

## Template — the slice tree (`codes`)

```
src/
  bootstrap/     App.tsx · main.tsx · index.css · AppLayout · MarketingLayout · routes.tsx · providers
  integration/   client.ts · interceptors.ts · auth.ts · common/
                 codes/ identity/ billing/                       ← endpoint fns, one module per domain
  domain/        common/
                 codes/ core/      (module · finder · preview · rule types + pure ops)
                        content/   (url · wifi · vcard … = { def, Content, Values, build, parse, validate }) · registry.ts
                 identity/ billing/
  application/   common/
                 codes/ (useCodes · useCodeBuilder · toCodeRow mapper)  identity/ (useAuth)  billing/
  presentation/  common/
                 codes/ core/ design/ (FillControls · EmojiControls · ContrastHint) · shape/ (ShapeControls)
                              routing/ (RuleBuilder) · preview/ (QrPreview)
                        content/components/ (UrlForm · WifiForm …) · ContentTypeForm
                        screens/ (CreateCodeScreen · CodesListScreen)
                 identity/ billing/ marketing/
```
Each slice folder carries a lowercase `index.ts` barrel — the slice's only public surface.

## Packaging

Two shapes, by app count — both under `engineering/codebase/{slug}.frontend-services/` (`@{brand}` = the repo's package scope).

- **single app (default)** — one Vite app with the layered `src/` above; no workspace. Use until a 2nd app or genuine cross-app reuse appears — don't pre-build a workspace.
- **pnpm workspace (multi-app)** — `packages/{common,ui,domain}` (`@{brand}/*`) + lowercase app folders, each with the same layered `src/`. `"workspace:*"` ≈ .NET `<ProjectReference>` · `pnpm-workspace.yaml` ≈ `.sln` · `packages/common/` ≈ a `Common/` project.
- **package boundaries** — `@{brand}/ui` = dumb components (no data/context/localStorage) · `@{brand}/common` = shared hooks/utils/identity (side effects OK) · `@{brand}/domain` = pure types/enums (no React). Extract to a package only when **≥ 2 apps** need it.
- `@wow-two-beta/ui` = the ecosystem library every product consumes; a repo's `@{brand}/ui` holds only product components not worth upstreaming yet.

## Dev server

- must run HTTPS via `vite-plugin-mkcert`; bind an **even** port (track in [ports.md](../../../deployment/hosting/ports.md)).
- must proxy `/api` → the backend's HTTPS (even) port (`secure: false`, `changeOrigin: false`) — see [state-and-data.md](state-and-data.md).
- gate mkcert behind `VITE_HTTPS=false` for a headless HTTP fallback (+ a matching `*-http` launch config); normal dev stays HTTPS.

## Preview (agent)

- mocks / design → render inline (`show_widget`), no server. Full app → drive the headless preview via the `*-http` config, screenshot at desktop width, then **stop it** (the human reviews in their own browser).
- app / builder routes sit behind the auth gate → the backend + its DB must be running.
