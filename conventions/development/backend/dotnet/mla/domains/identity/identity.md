# Identity

*Last updated: 2026-08-16*

> Who the caller is, and what the service lets them do.
> Purpose — the claim set is the contract; how it arrives is the provider's business.
> Use case — adding a sign-in method, reading the caller, or gating an endpoint.

## Contract

- must source the caller at the edge and pass it explicitly → [api context building](../api/api-context-building.md).
- must normalize every provider's claims to one claim set before any handler reads them.
- must default to deny — an endpoint opens by declaring what it allows.
- must keep authorization off the wire model; a `Dto` carries no permission.

---

## Configuration

- must key every auth concern under `Identity:` — `Identity:GitHub:ClientId`, never `OAuth:` or `Auth:`.
- must name the namespace and folder `Identity`, nesting a provider under it — `Identity.OAuth.GitHub`.
- the keyword tracks the SDK's own `WoW.Two.Sdk.Backend.Beta.Identity`.

---

## Providers

| Provider | Establishes the caller through | Docs |
|---|---|---|
| JWT bearer | a signed token on the request | [jwt auth](jwt/jwt-auth.md) |
| cookie | a session cookie issued after sign-in | — |
| OAuth / OIDC | an external provider's token, exchanged at the edge | — |
