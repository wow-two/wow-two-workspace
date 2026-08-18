# Responses

*Last updated: 2026-08-17*

> What a service sends back — the wire format, the error shape, the outcome contract, the fixed endpoints.
> Purpose — a client reads one success shape and one error shape, whichever endpoint it called.
> Use case — changing what an endpoint returns, or how a failure reaches the caller.

## What lives here

- [results](results.md) — the `Result` / `AppResult` outcome contract and the one `AppError`
- [problem details](problem-details.md) — RFC-7807 errors, the status mapper, the global handler
- [serialization](serialization.md) — the JSON wire contract, wired once at the host
- [known endpoints](known-endpoints.md) — the identity and system paths fixed across every app

---

## Boundary

- must keep the success channel and the error channel disjoint — a 2xx body is never a failure shape.
- must map a failure to a status at the edge; the outcome contract stays transport-agnostic.
