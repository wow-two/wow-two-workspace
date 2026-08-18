# Data components

*Last updated: 2026-08-16*

> The component kinds whose identity is the values they carry.
> Purpose — a data component is inert until something reads it, which is why it is MLA rather than LLA.
> Use case — naming or declaring a type that holds rather than does.

## The kinds

| Kind | Carries |
|---|---|
| [entity](entity.md) | a table-mapped row, owning its identity |
| [value object](value-object.md) | values stored inside a row, owning no identity |
| [dto](dto.md) | a projection onto the wire |
| [api request](api-request.md) | the body one controller action binds |
| [application request](application-request.md) | the message a caller dispatches in-process |
| [result](result.md) | an operation's outcome — a success or an `AppError` |
| [entity configuration](../../domains/persistence/ef/entity-configuration.md) | an EF mapping for one entity |

---

## Shared rules

- must declare a `sealed record` with `init`-only properties → [constructs](../../../lla/constructs/constructs.md).
- must start the type summary with **Represents**, and each member with **Gets**.
- must state role, location and declaration only; shape and flow belong to the domain that uses the type.
