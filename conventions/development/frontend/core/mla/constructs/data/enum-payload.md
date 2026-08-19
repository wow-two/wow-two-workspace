# Enum payload

*Last updated: 2026-08-19*

> What a member of an enum sends when the bare wire value cannot carry it — a `{Enum}Payload` bound as a
> `Record` keyed by the enum.
> Purpose — the payload is picked by the enum and sent as-is, so the value set stays the single source.
> Use case — a write whose shape varies by the option chosen.

---

## Declaration

- must model a rich send-object as `{Enum}Payloads: Record<Enum, {Enum}Payload>` in `domain` or `integration`,
  when the wire value alone cannot be sent — picked by the enum, sent as-is.
- must keep the payload out of `presentation`; a display and a payload never share a shape.

---

## Neighbours

- [enum display](enum-display.md) — what the same member looks like
- [enums](../../../lla/components/enums.md) — the value set this is keyed by
