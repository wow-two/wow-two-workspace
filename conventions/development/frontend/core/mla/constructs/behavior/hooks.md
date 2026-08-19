# Hooks

*Last updated: 2026-08-19*

Custom hooks encapsulate state, lifecycle, and operations. Data-fetching hooks own the API call + mapping
([state & data](../../domains/data/state-and-data.md)).

## Naming

- **Always prefix `use`** — `useAuth`, `useSupplyListings`.
- **Name the resource or action, not the noun** — `useFilterOptions`, not `useFilters`.
- File is PascalCase (`UseSupplyListings.ts`), export is camelCase (`useSupplyListings`)
  ([naming](../../../lla/notation/naming/naming.md)).

---

## Location

- layer and slice → [architecture](../../../../shapes/app/architecture/architecture.md) § *Sub-domains*,
  in a `hooks/` role-group.
- a cross-app hook ships from the repo's shared package
  ([boundaries](../../../../shapes/app/architecture/boundaries.md) § *Packaging*).

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

Verbs → [documentation](../../../lla/notation/documentation/documentation.md) § *Verb starters* — `Hook` and
`Context-accessor hook` are the two rows.

---

## Lifecycle rules

- Abort in-flight fetches on unmount / dependency change with `AbortController`; ignore `AbortError`.
- Keep effects narrow — one concern per `useEffect`; don't fetch + subscribe in the same effect.
- must return a **disposer** from any factory that subscribes, times, opens a socket, or observes — and must
  leave nothing running once it is called.
- must let the hook that owns the subscription dispose it itself, in its framework's teardown seam
  ([vue](../../frameworks/vue/reactivity.md) · [react](../../frameworks/react/hooks.md)).

---

## One export site

- must export a hook from exactly **one** module, and must not re-export it from a second barrel.
- must not alias it on the way out — a second name makes one hook read as two.
- a slice that needs a sibling's hook imports it; it does not republish it.

---

## Neighbours

- [state and data](../../domains/data/state-and-data.md) — the API client these wrap
- [documentation](../../../lla/notation/documentation/documentation.md) — the verb table
- [naming](../../../lla/notation/naming/naming.md) — the file / export casing
