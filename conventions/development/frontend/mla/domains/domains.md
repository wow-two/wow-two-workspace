# Domains

*Last updated: 2026-08-17*

> One folder per capability an app consumes — the contract it guarantees, and each provider that implements it.
> Purpose — a route model is not tied to a router, a `beforeEnter` is; the split keeps them apart.
> Use case — pinning an engine, adding a second one, or reading how a shipped one is wired end to end.

## The shape [REQUIRED]

```
{domain}/
  {domain}.md        ← the contract: what the capability guarantees, provider-free
  {provider}/        ← one folder per implementation, everything technology-tied
```

- must keep the lead doc provider-free — a rule naming a library sits in that library's folder.
- must name each provider folder for the technology — `tanstack/`, `vue-router/`, `zod/`.
- must treat a framework as a provider, never a scope — `vue/` and `react/` are folders here, not levels above.
- must let a second domain cite this contract rather than restate it.
- must not group domains by tier — the domain is the unit, and grouping hides which contract a provider serves.
- must carry the vendor as an optional peer on the provider's subpath alone
  ([swappable modules](../../../swappable-modules.md)).
- must not reach a vendor from the contract entry — importing the contract installs nothing.
- must open a folder only once one provider rule needs writing; a single-provider capability stays recognized.

---

## Built

| Domain | Contract | Providers |
|---|---|---|
| [data](data/state-and-data.md) | the `/api` client, the error body, server-state vs UI-state | `fetch` client · TanStack Query |
| [forms](forms/forms.md) | `useAppForm` — values, schema, submit, field errors | `house/` · `tanstack/` |
| [routing](routing/routing.md) | `RouteConfig` — places, guards, route metadata | `react-router` · `vue-router` |
| [api](api/type-mapping.md) | the .NET ↔ wire ↔ TS scalar contract | none — contract only |

---

## Recognized

Named so a design in progress has somewhere to land; no folder until a rule needs writing.
Each names a capability the SDK already ships behind one contract.

| Domain | Contract | Providers shipped |
|---|---|---|
| `auth` | the session state machine and its sign-in shapes | cookie · bearer · redirect · oauth |
| `storage` | the synchronous client-side persistence seam | local-storage · memory · zustand |
| `analytics` | the product-event sink | console · memory |
| `flags` | flag evaluation, total and never-throwing | static |
| `validation` | the Standard Schema seam every layer may reach | built-in · zod · valibot |
| `observability` | what the app logs, and where a record lands | console · memory |
| `uploads` | admission, scheduling and progress over a transport seam | xhr |
| `config` | a typed, fail-fast read of app configuration | `import.meta.env` · runtime `window` · static |
| `icons` | the icon component contract an app satisfies | any `IconAdapter` |
| `i18n` | the locale a subtree reads and the formatters it drives | `Intl` |
| `feedback` | the notice bus and what renders a notice | toasts · the query-error seam |

---

## Neighbours

- [components](../components/components.md) — the kinds a domain's providers are built from
- [architecture](../architecture/architecture.md) — the layer a domain's contract and providers live in
- [swappable modules](../../../swappable-modules.md) — how a provider's vendor stays an optional peer
