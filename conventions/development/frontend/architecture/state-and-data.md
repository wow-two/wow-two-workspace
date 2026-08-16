# State & data

*Last updated: 2026-07-09*

## API client — same-origin `/api`

The SPA is served from the .NET host's `wwwroot` in production, so **all API URLs are relative** (`/api/...`). In dev, Vite proxies `/api` to the backend's **HTTPS** port — the frontend always reaches the backend over HTTPS. No base-URL config, no CORS in prod.

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

**Always proxy to the backend's HTTPS (even) port** with `secure: false` (the .NET dev cert is self-signed) — never the HTTP port. The Vite dev server itself is HTTPS where mkcert is set up.

## Client shape

A thin `fetch` wrapper in `src/api/`:

- **`client.ts`** — `request<T>()` helper + an `api` object of typed methods (`getStatus`, `listServers`, …). Each method documents its route: `/** GET /api/servers — all registered servers. */`.
- **`types.ts`** — request/response DTOs + `ProblemDetails` (RFC 7807).
- **`ApiError`** — a typed `Error` carrying `status` + parsed `ProblemDetails`; the client throws it on non-2xx and on network failure (status `0`). Components/hooks catch it for messaging.
- Handle `204` / empty bodies (return `undefined as T`); set `Accept: application/json` and `Content-Type` only when there's a body.

```ts
/** Error carrying the server's RFC 7807 detail (or a transport-level message). */
export class ApiError extends Error {
  readonly status: number;
  readonly problem: ProblemDetails | null;
}
```

## State management

| Concern | Choice |
|---|---|
| Local UI state | `useState` / `useReducer` |
| Shared app state | **React Context + hooks** — no Redux/Zustand |
| **Server-state** (backend data) | **TanStack Query** behind a `use{Resource}` hook that keeps its `{Entity}State` shape — wrapped by the SDK query layer (`createQueryClient` + `useApp{Query,InfiniteQuery,Mutation}`). Maps DTO → domain at the hook; see [hooks.md](../presentation/hooks.md). **Not** for UI state. |
| Persistence | `localStorage`, namespaced key `{brand}:{app}:{feature}` |
| View routing | the `createAppRouter` data router — see [routing.md](routing.md). URL-hash routing is retired. |

- **Server-state vs UI-state** — Query holds only *cached copies of what the server owns* (lists, entities, their loading/error, pagination, poll). Everything else stays `useState`/Context: form inputs & drafts, toggles/open-closed/selection, theme, and **client-process state** (e.g. a batch runner's jobs/ticker). One-line test: *"would it survive a reload by re-fetching from the server?"* → Query; else local.

- Fetch inside hooks, not components; abort on unmount with `AbortController`.
- Map DTO → domain model at the hook boundary (see [models.md](../code-style/models.md)); never leak raw DTOs into the view tree.

## Mutations — passive only (no optimistic updates)

- must reflect **only the backend-confirmed result** — never pre-write the cache from the mutation input, never roll back.
- on **success** → reconcile the cache from the server's *returned value* (`invalidateQueries`, or `setQueryData` with the response); the UI updates to confirmed state.
- on **failure** → leave the cache untouched (the UI already shows the correct prior state) and surface the `ApiError`.
- the SDK `useAppMutation` wrapper has **no `onMutate` seam** — optimistic updates are not expressible by construction; mutations never auto-retry.
- rationale: a UI that mutates then twitches back on failure — or leaves related fields inconsistent — is worse than a brief wait. Fidelity > perceived speed.

## Query layer — capability matrix

> What the data layer provides — app-local in `bootstrap/query/` now, combining into the front SDK `@wow-two-beta/ui/query` (mirrors the router's `/router`). `[x]` shipped · `[ ]` planned. The closed-loop "what the SDK supports" index.

**Core**
- [x] `createQueryClient({ retry?: RetryPolicy })` — house defaults (30s stale · 5m gc · no focus-refetch · mutations no-retry) + a **configurable retry policy** (backoff · jitter · retryable statuses, from `foundation/resilience`) + global `onError` → `ApiError`
- [x] `QueryProvider` — mounts the client above `<RouterProvider>` · `toApiError` (coerce any throw → SDK `ApiError`) · `queryKeys` (typed key registry — the data-layer `paths`)

**Hooks — every read/write shape**
- [x] `useAppQuery` (single) · `useAppInfiniteQuery` (cursor + **poll-while-running**) · `useAppPaginatedQuery` (page/offset, keep-previous)
- [x] `useAppQueries` (dynamic N parallel) · `useAppSuspenseQuery` (suspends, pairs with lazy routes) · `useAppLazyQuery` (imperative / on-demand)
- [x] `useAppMutation` — **passive** (no `onMutate`) · `invalidates` / `onConfirmed`
- [x] `usePrefetchQuery` / `prefetchProps` (intent data prefetch) · `useQueryCache` (imperative get/set/invalidate/remove/prefetch)

**Integrations & infra**
- [x] `QueryProgressBridge` — RQ activity → the router's `NavigationProgress` backend heartbeat
- [x] `setupQueryPersistence` (localStorage cache, opt-in) · `QueryDevtools` (dev-only) · `QueryTestUtils` (test-only entrypoint)
- [x] **Retry** — `foundation/resilience`: `RetryPolicy` (backoff constant/linear/exp · jitter none/full/equal/decorrelated · retryable statuses) + `computeRetryDelay`/`shouldRetry`; reusable beyond query

**Interlocks with the router:** `queryKeys`↔`paths` · heartbeat↔`NavigationProgress` · data-prefetch↔chunk-prefetch · suspense↔lazy routes · cache-persist↔`RoutePersistence`.

## See also

- [hooks.md](../presentation/hooks.md) — data-fetching hooks
- [models.md](../code-style/models.md) — DTO ↔ domain mapping
- [../backend/presentation/response-models.md](../../backend/dotnet/mla/components/data/response-model.md) — the `ApiResponse<T>` success envelope this consumes
- [../backend/presentation/problem-details.md](../../backend/dotnet/mla/platform/problem-details.md) — the `Problem()` / ProblemDetails error shape this consumes
