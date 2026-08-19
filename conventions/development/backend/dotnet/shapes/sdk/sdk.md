# SDK

*Last updated: 2026-08-19*

> Shell. A package published for every product and for outside consumers. Take [core](../../core/core.md) whole; the shape rules live in [dotnet conventions](../../dotnet-conventions.md) § *Building the SDK itself* until this is written.

---

## Building the SDK

These conventions feed **both** the products and the backend-beta SDK — naming, documentation, constructs and
components hold identically in either repo. What differs is the shape a repo takes, and only that.

| Question | A product answers | The SDK answers |
|---|---|---|
| architecture | Clean layers per service → [architecture](../service/architecture/architecture.md) | a library, no Application / Infrastructure / Persistence split |
| host | one `HostConfiguration` per service → [host configuration](../service/platform/startup/host-configuration.md) | none; it ships `Add*` extensions a host calls |
| what earns a doc | its own business logic | its own surface, plus the seams a product wires |

- must apply every naming, documentation and construct rule in the SDK repo unchanged — the SDK is ours,
  so a convention change reaches it as a row in that repo's sweep file, never as an exemption.
- must keep an SDK type's public surface documented as a product type would be — a consumer reads only the
  XML doc.
- must decide what belongs there through [extract / keep / remove](../../../../sdk-extraction.md), never here.
- must leave the SDK's own package layout and registry to its `docs/` — that is repo shape, not a convention.

> **Queued.** A `use-case/` · `core/` cut of this tree — `core/` for what holds everywhere, `use-case/` for the
> shapes that differ (service, contained library, monolith, microservices, SDK) — is the direction, not yet the
> layout. Today the difference is small enough for the table above.

---

---

---

## Open

- **architecture** — unwritten; a library is not a service and skips the layer split.
- **delivery** — unwritten; packing, versioning and the consumer re-pin.
- **testing** — unwritten.
