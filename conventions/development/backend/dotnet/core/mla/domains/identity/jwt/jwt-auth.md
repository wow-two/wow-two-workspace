# JWT auth

*Last updated: 2026-08-15*

> JWT bearer authentication — issuing a token, validating one, and wiring both into the host.
> Purpose — one token shape and one validation path per service, so a claim means the same thing everywhere.
> Use case — adding sign-in, or changing what a token carries.

How a product wires JWT **validation** and **issuance** from the backend-beta SDK: two independent registrations
on **one shared signing key**. The SDK carries **no user model** — the app maps its own user into `Claim`s and
passes them in.

## Two halves, one key

- **Validate inbound bearer tokens** — `AddJwtBearerAuthentication`, configured through `Action<JwtOptions>`.
  - wires the ASP.NET `JwtBearer` scheme + `TokenValidationParameters`.
- **Issue signed tokens** — `AddJwtTokenIssuance`, configured through `Action<JwtTokenIssuerOptions>`.
  - wires `ITokenIssuer` → `JwtTokenIssuer` (singleton) + `TimeProvider.System`.

- validation lives under `src/Identity/Jwt/`, issuance under `src/Identity/Jwt/Issuance/`.
- the two do **not** know about each other at runtime; the **same symmetric key on both sides** is the contract.
- a token from `JwtTokenIssuerOptions.SigningKey` validates only if `JwtOptions.SymmetricKey` is byte-identical (HMAC).
- issued `iss`/`aud` (`JwtTokenIssuerOptions.Issuer` / `.Audience`) must equal `JwtOptions.Issuer` / `.Audience`.

> An API that only **accepts** tokens (Auth0 / Entra ID / Supabase issued them)
> registers `AddJwtBearerAuthentication` **only**. An auth service that mints tokens for its own API registers
> **both**, same key. Don't add issuance to a pure resource server.

---

## Validation — `AddJwtBearerAuthentication`

`JwtServiceCollectionExtensions.AddJwtBearerAuthentication(this IServiceCollection, Action<JwtOptions>)`.
Throws at registration if mis-configured — fail-fast, not fail-open:

- `JwtOptions.Issuer` — **required** (`InvalidOperationException` if blank).
- `JwtOptions.Audience` — **required** (same).
- exactly one key source — **required**: `JwtOptions.SymmetricKey` (HMAC dev / shared secret) **or**
  `JwtOptions.JwksUri` (asymmetric / managed keys via OIDC discovery). Supplying neither throws.

Hardened defaults baked into the scheme — do not re-set them in the product:

- `ValidateIssuer` / `ValidateAudience` / `ValidateIssuerSigningKey` all on.
- `RequireHttpsMetadata = true`, `SaveToken = true`.
- `MapInboundClaims = false` — raw claim types, no legacy SOAP remapping.
- tunable: `JwtOptions.ValidateLifetime` (default `true`), `JwtOptions.ClockSkew` (default 30s).

```csharp
builder.Services.AddJwtBearerAuthentication(o =>
{
    o.Issuer   = "https://my-issuer";
    o.Audience = "my-api";
    o.SymmetricKey = builder.Configuration["Jwt:Key"]!;   // OR o.JwksUri for managed keys
});

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();
```

`AddJwtBearerAuthentication` registers the scheme only — the product still calls
`UseAuthentication()` / `UseAuthorization()` in the pipeline.

---

## Issuance — `AddJwtTokenIssuance` + `ITokenIssuer`

`JwtIssuanceServiceCollectionExtensions.AddJwtTokenIssuance(this IServiceCollection, Action<JwtTokenIssuerOptions>)`
registers `ITokenIssuer` as a singleton (`JwtTokenIssuer`). It is a **pure library** — usable from a worker or a
console app, with no ASP.NET middleware.

`JwtTokenIssuerOptions`:

- `JwtTokenIssuerOptions.Issuer` — the `iss` claim; default `""`.
- `JwtTokenIssuerOptions.Audience` — the default `aud`, overridable per call; default `""`.
- `JwtTokenIssuerOptions.Lifetime` — the default token lifetime; default 1h.
- `JwtTokenIssuerOptions.SigningKey` — symmetric HMAC key, **required**; default `""`.
  - throws on first resolve if blank; ≥ 32 bytes for HS256.
  - source it from a secret store, never hard-code it.
- `JwtTokenIssuerOptions.Algorithm` — `HS256` (default) / `HS384` / `HS512`; any other value throws.

### `ITokenIssuer.Issue` — the only method, app supplies the claims

```csharp
string Issue(IEnumerable<Claim> claims, TokenIssuanceContext? context = null);
```

The SDK **never constructs claims**. The product maps its own user model into `Claim`s and passes them in:

```csharp
var token = _tokens.Issue(
    new[]
    {
        new Claim(JwtRegisteredClaimNames.Sub, user.Id),
        new Claim("user_role", user.Role),
    },
    new TokenIssuanceContext(Lifetime: TimeSpan.FromHours(24)));
```

`TokenIssuanceContext(TimeSpan? Lifetime = null, string? Audience = null, IReadOnlyDictionary<string,object>? AdditionalHeaders = null)`
— per-call overrides; an unset member falls back to `JwtTokenIssuerOptions`.
`JwtTokenIssuer` stamps `iat` / `nbf` / `exp` from the injected `TimeProvider` (fake-clock-testable),
not the wall clock.

---

## Registering both — shared key

```csharp
var jwtKey = builder.Configuration["Auth:JwtKey"]!;   // one secret, both halves

builder.Services.AddJwtTokenIssuance(o =>
{
    o.Issuer     = "my-auth";
    o.Audience   = "my-api";
    o.SigningKey = jwtKey;
});
builder.Services.AddJwtBearerAuthentication(o =>
{
    o.Issuer       = "my-auth";    // == issuer above
    o.Audience     = "my-api";     // == audience above
    o.SymmetricKey = jwtKey;       // == signing key above
});
```

Same key + matching `iss`/`aud` ⇒ tokens this service mints validate on this service, and on any sibling
sharing the secret. Diverge the key and every token 401s.

---

## Not in scope (v1)

- refresh tokens, revocation, asymmetric issuance (RS*/ES*) and key rotation are **not** implemented for issuance.
- issuance is symmetric HMAC only; validation already accepts asymmetric / managed keys via `JwtOptions.JwksUri`.
- key rotation is the v2 seam — an `IKeyProvider`-shaped extension.
- do not assume it exists; there is no such symbol in source today.

---

## Neighbours

- [settings.md](../../../components/settings.md) — bind `Issuer`/`Audience`/key from config + secret store,
  not literals
- [result-pattern.md](../../../constructs/data/result.md) — in app code, surface auth failures as `AppError`,
  never a thrown exception
- [conventions](../../../../../../../../conventions.md) § *Authoring a convention* — the cite-the-symbol rule
- SDK `wow-two-sdk.backend.beta` → `src/Identity/Jwt/jwt.md` (validation) +
  `src/Identity/Jwt/Issuance/issuance.md` (issuance) — quickstarts + JWKS examples
