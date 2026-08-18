# Routing

*Last updated: 2026-07-08*

> How a wow-two React app defines routes — a declarative `RouteConfig` passed to the SDK-owned `createAppRouter` wrapper. Apps author routes; the wrapper owns the react-router machinery.
> Purpose — one routing model across every app, with cross-cutting behavior added in one place. Sits with [architecture.md §Routing & responsive surfaces](../../architecture/architecture.md) (the place↔page / action↔modal doctrine).

## Ownership

- must route with **`createAppRouter(routes)`** over `react-router-dom` v7 (data router) — never call `createBrowserRouter` / `<BrowserRouter>` / `<Routes>` directly.
- the wrapper is the **single extension point** — it injects `<ScrollRestoration>`, a root `errorElement`, and the `*` → `NotFound`; cross-cutting behavior is added there, every app inherits it.
- must not keep view state in the URL hash — the data router owns real paths (permalinks depend on it).

---

## Home

- must author the wrapper **app-local in `bootstrap/router/`**, package-shaped (framework-only imports — `react` / `react-router-dom`, no `@/…`), until a 2nd consumer.
- must then **combine into the front SDK `@wow-two-beta/ui`** (a `/router` subpath — a 1-line import swap) when a 2nd consumer lands; a dedicated multi-repo split (a separate app package) is a later concern. The SDK's *presentation* components stay router-free — the router ships as its own subpath.

---

## The model — `AppRoute`

- must author routes as a `RouteConfig` (`readonly AppRoute[]`): `{ path · index · element | lazy · layout · redirect · handle · children · errorElement · id }`.
- must code-split every **place** via `lazy: () => import('@/presentation/…/XPage')` — accepts a `default` or a named `Component` export.
- must nest shared chrome via a **layout route** (`layout:` a `*Layout` in `bootstrap/` composing the SDK `AppShell` + `<Outlet>`).
- must attach per-route metadata via `handle: { crumb, title }` (read through `useMatches()`); a plain redirect via `redirect: '/path'`.

---

## Places = pages, actions = modals

- must give every **place** a route + a `*Page` (deep-linkable / refreshable / shareable); every **action** a routeless `*Modal` (`useState`-driven), presented as `ResponsiveModal` (Modal ↔ BottomSheet). Full doctrine: [architecture.md §Routing & responsive surfaces](../../architecture/architecture.md).
- must render responsiveness in the **component, not the route** — one route per place at every breakpoint; never fork routes by device.

---

## Composition

- must compose the shell in an app-owned `*Layout` (the layout route): the SDK `AppShell` (`@wow-two-beta/ui/presentation/layout`) with `<Outlet>` in `AppShell.Content`.
- must wire nav via **`<NavItem asChild><Link/></NavItem>`** — the SDK `NavItem` chrome forwarding to a router `<Link>`, active state from `useMatch`; the SDK components never import a router, the app owns navigation. Reusable as `AppNavLink`.
- should keep `presentation/` screens router-agnostic — `bootstrap/` + the `*Layout` own `<Outlet>` / `<Link>` / `useParams`; a screen takes value + callback props.

> **Resolved in `@wow-two-beta/ui` `0.0.88`.** `NavItem asChild` was broken in ≤ 0.0.79 (it fed a multi-child array — icon + label + trailing — into a single-child `Slot`, throwing `React.Children.only`); `0.0.88` adds `Slottable`, so `<NavItem asChild><Link/></NavItem>` works. `AppNavLink` uses it.

---

## Wrapper-provided (shipped)

- **`document.title` sync** — `createAppRouter(routes, { titleSuffix })` mounts a `DocumentTitle` in `AppRoot`; on every navigation it sets `document.title` to the deepest matched `handle.title` (falls back to the suffix alone when a route sets no `title`, e.g. `:id` detail routes).
- **route params** resolve via `useParams()` in the `*Page` — the wrapper adds no param plumbing (a loader's `params` arg becomes available when guards/loaders land).
- **baseline component names** (`AppRoot` · `AppLayout` · `AppErrorBoundary` · bare `NotFound` / `DocumentTitle`) — see [naming.md § App-shell baseline components](../../../lla/notation/naming/naming.md).

---

## Capability matrix

> What the router layer provides — app-local in `bootstrap/router/` now, combining into the front SDK `@wow-two-beta/ui` (`/router` subpath) later. `[x]` shipped · `[ ]` planned. Named for exact reference — the closed-loop "what the SDK supports" index.

**Core**
- [x] `createAppRouter(routes, options)` · `AppRoute` / `RouteConfig` model
- [x] `AppRoot` (`<ScrollRestoration>` + `<Outlet>`) · `AppErrorBoundary` (root) · `NotFound` (`*`)
- [x] `lazy` code-split places · `redirect` · `layout` nesting · `basename` · `history:'hash'`
- [x] `DocumentTitle` (`handle.title` + `titleSuffix`) · `DocumentMeta` (`handle.meta`) · `useParams`

**Navigation & UX**
- [x] `paths` typed registry + `definePath` param-inferring builders (no raw `to=` strings)
- [x] `NavigationProgress` — mode-switch bar ↔ backend heartbeat (`ProgressProvider` / `track()`)
- [x] `usePrefetch` / `prefetchProps` — intent (hover/focus) prefetch (wired into `AppNavLink`)
- [x] `AppNavLink` — `NavLink` active + View Transitions
- [x] `useNavigationBlocker` — dirty-form + `beforeunload` prompt
- [x] `RoutePersistence` + index-restore — tab-reopen returns to last route

**Access & data**
- [x] `AppRoute.guard` seam → loader redirect (chain-aware runner)
- [x] `returnTo` — `requireAuth` capture + `useReturnTo` restore (open-redirect-safe)
- [x] `useTypedSearchParams`

**a11y & meta**
- [x] `RouteAnnouncer` — focus reset + aria-live route announce
- [x] `PageViewTracker` — analytics sink on navigation (`onPageView` option)
- [x] `RouteHandle.meta` → `DocumentMeta` — description / name meta tags
- [x] `lazyRoute` — stale-deploy chunk retry-once (+ `reloadOnChunkError`)

**SDK dependency**
- [x] `NavItem asChild` (Slottable) — fixed in `@wow-two-beta/ui` `0.0.88`; adopted in `AppNavLink`
