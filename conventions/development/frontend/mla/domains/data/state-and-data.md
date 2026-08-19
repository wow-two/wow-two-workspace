# State & data

*Last updated: 2026-08-19*

## API client — same-origin `/api`

- must call the API with relative URLs (`/api/...`) — the SPA is served from the .NET host's `wwwroot` in
  production, so there is no base-URL config and no CORS.
- must proxy `/api` in dev to the backend's **HTTPS (even) port** with `secure: false` (the .NET dev cert is
  self-signed), never the HTTP port — the frontend always reaches the backend over HTTPS.
- the Vite dev server itself is HTTPS where mkcert is set up.

```ts
// vite.config.ts — dev proxy to the backend's HTTPS (even) port
export default defineConfig({
  base: '/',                                   // root-relative assets
  plugins: [react(), tailwindcss()],
  server: {
    // secure:false → accept the .NET dev self-signed cert
    proxy: { '/api': { target: 'https://localhost:8210', changeOrigin: true, secure: false } },
  },
});
```

---

## Client shape

A thin `fetch` wrapper in `src/api/`:

- **`client.ts`** — `request<T>()` helper + an `api` object of typed methods (`getStatus`, `listServers`, …);
  each method documents its route: `/** GET /api/servers — all registered servers. */`.
- **`types.ts`** — request/response DTOs + `ProblemDetails` (RFC 7807).
- **`ApiError`** — a typed `Error` carrying `status` + parsed `ProblemDetails`; the client throws it on non-2xx
  and on network failure (status `0`). Components and hooks catch it for messaging.
- must handle `204` / empty bodies (return `undefined as T`), and set `Accept: application/json` and
  `Content-Type` only when there is a body.
- consumes the backend `ApiResponse<T>` success envelope
  ([api messages](../../../../backend/dotnet/mla/domains/api/api-messages.md)) and its `Problem()` error shape
  ([problem details](../../../../backend/dotnet/mla/platform/responses/problem-details.md)).

```ts
/** Error carrying the server's RFC 7807 detail (or a transport-level message). */
export class ApiError extends Error {
  readonly status: number;
  readonly problem: ProblemDetails | null;
}
```

---

## State management

| Concern | Choice |
|---|---|
| Local UI state | `useState` / `useReducer` |
| Shared app state | **React Context + hooks** — no Redux/Zustand |
| **Server-state** | **TanStack Query** behind a `use{Resource}` hook keeping `{Entity}State`; not for UI state |
| Persistence | `localStorage`, namespaced key `{brand}:{app}:{feature}` |
| View routing | the `createAppRouter` data router ([routing](../routing/routing.md)); URL-hash routing is retired |

- **server-state vs UI-state** — Query holds only cached copies of what the server owns (lists, entities, their
  loading/error, pagination, poll). Everything else stays `useState` / Context: form inputs and drafts,
  toggles, open-closed, selection, theme, and client-process state (a batch runner's jobs/ticker). The test:
  *would it survive a reload by re-fetching from the server?* → Query; else local.
- must fetch inside hooks, not components ([hooks](../../constructs/hooks.md)); abort on unmount with
  `AbortController`.
- must map DTO → domain model at the hook boundary ([models](../../constructs/data/models.md)); never leak a
  raw DTO into the view tree.

---

## Mutations — passive only (no optimistic updates)

- must reflect **only the backend-confirmed result** — never pre-write the cache from the mutation input, and
  never roll back.
- must reconcile the cache on **success** from the server's returned value (`invalidateQueries`, or
  `setQueryData` with the response); the UI updates to confirmed state.
- must leave the cache untouched on **failure** — the UI already shows the correct prior state — and surface
  the `ApiError`.
- the SDK `useAppMutation` wrapper has **no `onMutate` seam**, so an optimistic update is not expressible; a
  mutation never auto-retries.

---

## Query layer — capability matrix

> What the data layer provides — app-local in `bootstrap/query/` now, combining into the front SDK
> `@wow-two-beta/ui/query`. `[x]` shipped · `[ ]` planned.

**Core**
- [x] `createQueryClient({ retry?: RetryPolicy })` — house defaults (30s stale · 5m gc · no focus-refetch ·
  mutations no-retry) + a configurable retry policy (backoff · jitter · retryable statuses, from
  `foundation/resilience`) + global `onError` → `ApiError`
- [x] `QueryProvider` — mounts the client above `<RouterProvider>` · `toApiError` (coerce any throw → SDK
  `ApiError`) · `queryKeys` (typed key registry — the data-layer `paths`)

**Hooks — every read/write shape**
- [x] `useAppQuery` (single) · `useAppInfiniteQuery` (cursor + **poll-while-running**) ·
  `useAppPaginatedQuery` (page/offset, keep-previous)
- [x] `useAppQueries` (dynamic N parallel) · `useAppSuspenseQuery` (suspends, pairs with lazy routes) ·
  `useAppLazyQuery` (imperative / on-demand)
- [x] `useAppMutation` — **passive** (no `onMutate`) · `invalidates` / `onConfirmed`
- [x] `usePrefetchQuery` / `prefetchProps` (intent data prefetch) · `useQueryCache` (imperative
  get/set/invalidate/remove/prefetch)

**Integrations & infra**
- [x] `QueryProgressBridge` — RQ activity → the router's `NavigationProgress` backend heartbeat
- [x] `setupQueryPersistence` (localStorage cache, opt-in) · `QueryDevtools` (dev-only) · `QueryTestUtils`
  (test-only entrypoint)
- [x] **Retry** — `foundation/resilience`: `RetryPolicy` (backoff constant/linear/exp · jitter
  none/full/equal/decorrelated · retryable statuses) + `computeRetryDelay` / `shouldRetry`; reusable beyond
  query

**Interlocks with the router:** `queryKeys`↔`paths` · heartbeat↔`NavigationProgress` ·
data-prefetch↔chunk-prefetch · suspense↔lazy routes · cache-persist↔`RoutePersistence`.
