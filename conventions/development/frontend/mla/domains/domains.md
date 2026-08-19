# Domains

*Last updated: 2026-08-19*

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
| [analytics](analytics/analytics.md) | the product-event sink | console · memory |
| [api](api/type-mapping.md) | the .NET ↔ wire ↔ TS scalar contract | none — contract only |
| [auth](auth/auth.md) | the session state machine and its sign-in shapes | cookie · bearer · redirect · oauth |
| [config](config/config.md) | a typed, fail-fast read of app configuration | `import.meta.env` · window · static |
| [data](data/state-and-data.md) | the `/api` client, the error body, server- vs UI-state | fetch · TanStack Query |
| [feedback](feedback/feedback.md) | the notice bus and what renders a notice | toasts · the query-error seam |
| [flags](flags/flags.md) | flag evaluation, total and never-throwing | static |
| [forms](forms/forms.md) | `useAppForm` — values, schema, submit, field errors | house · tanstack |
| [i18n](i18n/i18n.md) | the locale a subtree reads and the formatters it drives | `Intl` |
| [icons](icons/icons.md) | the icon component contract an app satisfies | any `IconAdapter` |
| [observability](observability/observability.md) | what the app logs, and where it lands | console · memory |
| [routing](routing/routing.md) | `RouteConfig` — places, guards, route metadata | react-router · vue-router |
| [storage](storage/storage.md) | the synchronous client-side persistence seam | local-storage · memory · zustand |
| [uploads](uploads/uploads.md) | admission, scheduling and progress over a transport | xhr |
| [validation](validation/validation.md) | the Standard Schema seam every layer may reach | built-in · zod · valibot |

---

## Neighbours

- [constructs](../constructs/constructs.md) — the kinds a domain's providers are built from
- [architecture](../architecture/architecture.md) — the layer a domain's contract and providers live in
- [swappable modules](../../../swappable-modules.md) — how a provider's vendor stays an optional peer
