# Frontend Architecture

*Last updated: 2026-08-19*

> The slice tree a React/TS app is built on — five Clean-Arch layers at `src/`, each sliced by domain.
> Purpose — one inward dependency direction, so a layer reads without its callers.
> Use case — placing a new file, or splitting a domain that has outgrown one folder.

## Layers [REQUIRED]

Dependency runs inward: `presentation → application → domain`, `integration → domain`.
`bootstrap` wires all.

| Layer | Holds | Backend peer |
|---|---|---|
| `bootstrap/` | the composition root — `App.tsx` · `main.tsx` · providers · `routes.tsx` · layouts | Host |
| `presentation/` | components and screens; renders, never fetches | Presentation |
| `application/` | orchestration hooks, view-model mappers, submit orchestration, client state | Application |
| `domain/` | types, enums, extensions, pure ops (`build` · `parse` · `validate`); depends on nothing | Domain |
| `integration/` | HTTP client, endpoint fns, interceptors, auth; returns wire DTOs, no React | Infrastructure |

- must not import sideways — share via `common/` or lift a layer; `common/` and `bootstrap/` are exempt.
- should lint the direction (ESLint `no-restricted-paths`) — unlinted layering rots.

---

## Domains

- must slice every layer by domain — `codes` · `identity` · `billing` · `marketing`.
- must give each layer a `common/` slice for anything two or more domains use.
- must repeat a domain in every layer it touches — `presentation/codes/` · `domain/codes/`.

---

## Sub-domains

- must divide a domain into cohesive sub-domains — `codes` → `core` (the builder) · `content` (per type).
- must fold a concern into a sub-domain once it owns three or more components; keep it flat below that.
- may divide a sub-domain again by concern — `presentation/codes/core` → `design` · `shape` · `preview`.
- may hold components directly; a `components/` wrapper separates non-component files only, one style per domain.
- must name a folder either a sub-domain (a model noun — `core` · `design`) or a role-group (a plural role
  noun — `models/` · `enums/` · `pages/` · `hooks/` · `mappers/`), never the activity (`validation/`).
- must not treat a role-group as a sub-domain.
- must put in domain-`common/` whatever belongs to no sub-domain — shared components, composition role-groups.
- must place a routed page in domain-`common/pages/` — it composes sub-domains, so it belongs to none.

---

## Files

- must name files, folders and slice barrels per [naming](../../lla/notation/naming/naming.md).
- must give each component its own folder ([constructs](../constructs/constructs.md)).
- must suffix a component by its [kind](../constructs/component-catalog.md), a seam by a
  [headless role](../constructs/headless-suffixes.md).
- must name a hook `use{Noun}` ([hooks](../constructs/hooks.md)); data `use{Entity}` returns `{Entity}State`,
  and a data model is marked `*Dto`, a write contract `*Request`, a variant `*Content`.
- must export `{domain}Api` from `integration/{domain}`, its fns `{verb}{Noun}`.
- must name an extension object `{Noun}Extensions` (`as const`); constant casing is
  [naming](../../lla/notation/naming/naming.md)'s.

---

## Compound components

- must reach for a compound root only when it owns 2+ subparts that exist nowhere else — `Modal.Content` ·
  `Table.Row` · `Tabs.Panel`; a lone add-on stays a flat sibling.
- must keep the root's own role suffix, and name each subpart `Root{Part}`.
- must export each subpart both flat and attached, so `Root.Sub` and the flat name both resolve.
- must type the named export through `Object.assign`, so `import { Modal }` plus `<Modal.Content>` type-checks.
- must not attach the statics by casting the default export — the barrel re-exports the named binding, untyped.

```ts
ModalRoot.displayName = 'Modal';   // plain-fn roots keep the DevTools name; forwardRef roots name the inner fn
export const ModalContent = …;     // flat subparts stay exported
export const Modal = Object.assign(ModalRoot, { Content: ModalContent, Header: ModalHeader, … });
```

---

## Routing and responsive surfaces

A place is a URL, and a route renders the same place at every breakpoint.

- must give a place one route and a `*Page` — deep-linkable, refreshable, shareable.
- must give an action a routeless `*Modal` — ephemeral, so no URL and no cross-size mismatch.
- must not render one place as a modal on desktop and a page on mobile — that breaks copy-paste, refresh, back.
- must resolve a direct hit, refresh or new tab on a place-route to a standalone page; a desktop
  modal-over-context is allowed only through intercepting routes that keep that fallback.
- must put responsiveness in the component, not the route — a `*Modal` presents as `Modal` or `BottomSheet`.

---

---

## Slice tree

```
src/
  bootstrap/     App.tsx · main.tsx · index.css · AppLayout · routes.tsx · providers
  integration/   client.ts · interceptors.ts · auth.ts · common/ · codes/ identity/ billing/
  domain/        common/ · identity/ billing/
                 codes/ core/    (module · finder · preview · rule types + pure ops)
                        content/ (url · wifi · vcard = { def, Content, build, parse }) · registry.ts
  application/   common/ · identity/ (useAuth) · billing/
                 codes/  (useCodes · useCodeBuilder · toCodeRow mapper)
  presentation/  common/ · identity/ billing/ marketing/
                 codes/ core/     design/ (FillControls) · shape/ (ShapeControls) · preview/ (QrPreview)
                        content/  components/ (UrlForm · WifiForm) · ContentTypeForm
                        common/pages/   (CreateCodePage · CodesListPage)
```

---

## Neighbours

- [boundaries](boundaries.md) — what stays in the app, what extracts to the SDK, how the app is packaged
- [constructs](../constructs/constructs.md) — the kinds each slice holds
- [models](../constructs/data/models.md) — the model types a slice declares, and variant-set dispatch
- [routing](../domains/routing/routing.md) — how a place becomes a route, and the router wrapper that owns it
- [domains](../domains/domains.md) — the capabilities an app consumes
