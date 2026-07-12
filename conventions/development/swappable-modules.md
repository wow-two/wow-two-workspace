# Swappable Modules

*Last updated: 2026-07-11*

> Governs any SDK module that wraps a third-party engine or could ever need one (forms, query, router, dnd, storage, analytics, …) — frontend and
> backend alike. Purpose — vendor freedom: apps code against a house contract once; engines swap via a one-line pin, proven by a shared conformance
> suite. Reference implementation: `@wow-two-beta/ui` `/forms-engine` (contract + `house` + `tanstack`, one 34-case suite).

## Contract

- must define a house contract first — the types apps import (`AppForm`, `FormEngine`-style interface); adapters implement it, never leak vendor types
- must keep the contract at the 90% surface derived from real product usage — grow it only from evidence, never from a vendor's feature list
- must expose the native engine instance as a typed escape hatch (`form.engine`); per-consumer coupling is allowed, contract-level coupling is not
- should promote an escape-hatch pattern into the contract once 2+ consumers reach for the same native feature
- must not fold engine variants into option flags — behavior variants are sibling hooks / factories (`useAppMutation` vs `useOptimisticMutation`)

---

## Adapters

- must ship each engine as its own subpath (`/forms-engine/tanstack`, `/forms-engine/house`) with an identical entry signature
- must carry vendor deps as optional peers (`peerDependenciesMeta`) on the adapter subpath only — importing the contract or a sibling adapter must not
  pull the vendor (verify in `dist` chunks)
- must own semantic alignment inside the adapter (overlay state, timing shims) — the contract's semantics win; vendor drift never reaches the app
- should ship two adapters from day one (lib + `house` micro-engine, or two libs) — the second adapter is what keeps the contract honest
- may cap a `house` micro-engine with a documented feature ceiling; it is a hedge, not a competitor

---

## Conformance

- must maintain one engine-agnostic behavioral suite (`describe{X}EngineConformance(name, factory)`) pinning timing, merge, reset, error semantics
- must run the full suite against every adapter; a new adapter ships only when it passes unmodified
- must not fork the suite per adapter — an adapter needing suite edits means the contract or the adapter is wrong

---

## App usage

- must pin the engine in one app-local re-export (`src/form.ts` → the adapter subpath); app code imports only that file and the contract types
- must not import vendor packages directly in app code — the escape hatch is reached through the pinned adapter's typed `engine`

---

## Retrofit

- must sweep pre-convention modules toward this shape when touched (contract extraction first, adapters second); track the sweep as an iteration in the
  owning repo's planning doc
