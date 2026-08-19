# Hooks

*Last updated: 2026-08-19*

Custom hooks encapsulate state, lifecycle, and operations. Data-fetching hooks own the API call + mapping
([state & data](../domains/data/state-and-data.md)).

## Naming

- **Always prefix `use`** — `useAuth`, `useSupplyListings`.
- **Name the resource or action, not the noun** — `useFilterOptions`, not `useFilters`.
- File is PascalCase (`UseSupplyListings.ts`), export is camelCase (`useSupplyListings`)
  ([naming](../../lla/notation/naming/naming.md)).

---

## Location

- pnpm workspace: cross-app hooks in `packages/common/src/hooks/`; app-specific (domain data) in `{app}/src/hooks/`.
- single app: `src/hooks/` (or `src/{feature}/hooks/`).

---

## Return shape

- **Object return** for multiple values: `{ listings, loading, error, refetch }`.
- **Tuple return** only for simple state-like hooks: `[value, setValue]`.

```typescript
/** Manages the supply listings fetch lifecycle with pagination and filtering. */
export function useSupplyListings() {
  return { listings, loading, error, refetch };
}

/** Manages dropdown open/close state with outside-click-to-close behavior. */
export function useDropdown(): [boolean, () => void] { }
```

---

## JSDoc

| Hook kind | Verb | Example |
|---|---|---|
| State / lifecycle (≈90%) | `Manages` | `/** Manages the supply listings fetch lifecycle. */` |
| Thin context accessor | `Provides access to` | `/** Provides access to auth state from AuthContext. */` |

---

## Lifecycle rules

- Abort in-flight fetches on unmount / dependency change with `AbortController`; ignore `AbortError`.
- Keep effects narrow — one concern per `useEffect`; don't fetch + subscribe in the same effect.
- must return a **disposer** from any factory that subscribes, times, opens a socket, or observes — and must
  leave nothing running once it is called.
- must let a composable that owns the subscription dispose it itself, through `onScopeDispose`.

---

## One export site

- must export a composable from exactly **one** module, and must not re-export it from a second barrel.
- must not alias it on the way out — a second name makes one composable read as two.
- a slice that needs a sibling's composable imports it; it does not republish it.

---

## Neighbours

- [state and data](../domains/data/state-and-data.md) — the API client these wrap
- [documentation](../../lla/notation/documentation/documentation.md) — the verb table
- [naming](../../lla/notation/naming/naming.md) — the file / export casing
