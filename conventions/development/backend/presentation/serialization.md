# Serialization

*Last updated: 2026-07-03*

> The JSON wire contract every API emits and accepts — property casing, enum + scalar forms, null handling. Configured
> once at the host, never per controller. The frontend mirrors it verbatim: [../../frontend/code-style/type-mapping.md](../../frontend/code-style/type-mapping.md).

## Contract

- must serialize property names + dictionary keys as **camelCase** (`JsonNamingPolicy.CamelCase`).
- must serialize `enum` values as **camelCase strings** — `JsonStringEnumConverter(JsonNamingPolicy.CamelCase)`; never integer ordinals, never PascalCase names.
- must **omit null** on write (`DefaultIgnoreCondition = WhenWritingNull`) — an absent key, never `"field": null`.
- must serialize `Guid` as a string, `decimal` / `int` / `long` as a number, `bool` as a boolean.
- must serialize `DateTimeOffset` / `DateOnly` / `TimeOnly` / `TimeSpan` as ISO-8601 strings.

> Wire vs storage: this is the **API** enum form (camelCase string). DB storage is a separate concern — snake_case text
> ([../persistence/enums.md](../persistence/enums.md)). One enum → `active` on the wire, `active` in the column, `Active` in code.

---

## Wiring

- must apply the contract once, at the host — `AddControllers().AddJsonStringEnums()` over the SDK preset (`JsonOptionsPresets.Default`), never a hand-rolled `JsonSerializerOptions` per controller ([../architecture/host-configuration.md](../architecture/host-configuration.md)).
- must reuse the **same options object** for any manual (de)serialization (e.g. a jsonb `ValueConverter`) so the stored and wire shapes can't drift.
- must not override casing / enum / null policy on an individual endpoint — the contract is uniform across the service.
