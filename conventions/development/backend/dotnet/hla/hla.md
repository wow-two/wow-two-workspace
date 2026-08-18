# HLA — between our own services

*Last updated: 2026-08-16*

> High-level architecture: rules that only exist once there is more than one of our services.
> Purpose — keep fleet-shaped decisions out of `mla/`, where a single service would silently adopt them as defaults.
> Use case — reach here when a rule needs both ends to obey it, and we own both ends.

## The boundary

- **`hla/` when we own both ends** — a gRPC contract, a cross-service event schema, a shared quota, the gateway's routing rules.
- **`mla/` when we own one end** — a third party is *adapted*, never contracted. Its client, broker and observed limits live in `mla/domains/`.

---

## Empty by design

Nothing here yet, and the folder is named ahead of its contents on purpose: without it, the first gateway or gRPC rule lands in
`mla/platform/` and becomes a single-service default that every later service inherits by accident.

Candidates, as they arrive: API gateway routing · gRPC contract and versioning · cross-service event schema and delivery
guarantees · rate limiting and quota allocation across services · distributed tracing correlation.
