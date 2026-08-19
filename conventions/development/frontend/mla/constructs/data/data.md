# Data constructs

*Last updated: 2026-08-19*

> The constructs whose identity is the values they carry — the shapes a slice declares, and the carrier they
> travel in.
> Purpose — a data construct does nothing until something reads it, which is why it is MLA rather than LLA.
> Use case — declaring a wire or app shape, or returning from an operation that can fail.

## The kinds

| Kind | Carries |
|---|---|
| [models](models.md) | the `*Dto` · `*ApiRequest` · `*Model` · `*Content` family, and how one maps to the next |
| [result](result.md) | the `Result<TSuccess, TFailure>` carrier, `AppError`, and `ResultExtensions` |
| [enum projections](enum-projections.md) | `{Enum}Display` · `{Enum}Payload` — how an enum is read |

---

## Neighbours

- [constructs](../constructs.md) — the authoring pass and the coining gate every construct runs
- [enums](../../../lla/components/enums.md) — the value set a model field is typed as
- [type mapping](../../domains/api/type-mapping.md) — the .NET ↔ wire ↔ TS scalar contract these shapes obey
