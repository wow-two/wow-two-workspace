# HLA — between our own frontends

*Last updated: 2026-08-19*

> High-level architecture: rules that only exist once one frontend has to agree with another at runtime.
> Purpose — keep fleet-shaped decisions out of `mla/`, where a single app would silently adopt them as defaults.
> Use case — reach here when a rule needs both apps to obey it, and we own both apps.

## The boundary

- **`hla/` when we own both ends** — a micro-frontend host/remote contract, a shared runtime, cross-app route
  ownership.
- **`mla/` when we own one end** — a third-party widget is *adapted*, never contracted. Its client and its limits
  live in `mla/domains/`.

A monorepo `@{brand}/*` package is **not** `hla/`: it is compiled into one app, so its rules are
[boundaries](../../shapes/app/architecture/boundaries.md).

**The SDK targets every scope, and the scope follows the component, not the package.** `@wow-two-beta/ui`'s primitives
and layers are `mla/`; a module-federation host, a shared session across separately deployed apps, or a cross-app
routing contract would be `hla/` the day the SDK ships one. Consuming a package is never itself the test.

---

## Named ahead of its contents

Nothing shipped here yet — not because the scope is idle, but because the SDK has built nothing into it. The folder is
named first on purpose: without it, the first module-federation or shared-runtime rule lands in the
[app shape](../../shapes/app/app.md) and becomes a single-app default every later app inherits by accident.

Candidates, as they arrive: micro-frontend host / remote contract and version skew · a shared runtime (single Vue or
React instance across remotes) · cross-app route ownership and deep-link handover · a shared auth session across
separately deployed apps · design-token distribution when two apps must render identically.
