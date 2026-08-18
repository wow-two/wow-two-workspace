# Results

*Last updated: 2026-08-16*

> The one outcome contract every handler and endpoint returns — a typed success, or an `AppError`.
> Purpose — a failure crosses a boundary as a value, so no layer has to guess whether an exception means "expected".
> Use case — returning from a handler, collapsing at the edge, or bridging a throw into a return.

The carrier's own declaration is a [component](../../constructs/data/result.md); everything below is the service-wide contract.

---

## Carriers

| Carrier | Use | Shape |
|---|---|---|
| `Result` / `Result<T>` | everywhere (domain / service / foundation / infra) | `Success` \| `Failure(AppError)` — lightweight, no context |
| `AppResult<TSuccess>` | mediator handlers ↔ controllers | `Success(TSuccess Data, ctx?)` \| `Failure(AppError Error, ctx?)` |

- both are **closed DUs** (private ctor + sealed nested cases); `where T : notnull` / `where TSuccess : notnull` → non-null, side-owned (no `bool IsSuccess; T?`, no null-checks).
- collapse with `.Match(onSuccess, onFailure)` — the mandated consume path.
- an inner `Result<T>` (service) maps up into an `AppResult<TSuccess>` in the handler.
- may use `=>` for a member that returns or delegates — a carrier holds a success or an error, not logic that grows
  ([style](../../../lla/notation/style/style.md) § *The body*).

---

## `AppError`

`AppError(AppErrorType Type, string Message, IReadOnlyDictionary<string,object?>? Metadata = null) { ErrorOrigin? Origin }` — open `record` (subclassed by `ValidationError`, `AppAggregateError`).

- **must** author errors via a catalog — SDK `AppErrors.{Kind}(...)`, app `OrderErrors.*` — never `new AppError { … }` at a call site.
- **must not** put an HTTP status on the error — `AppErrorType` is transport-agnostic; status maps at the edge ([problem-details.md](problem-details.md)).
- `Type` (name) is the wire `code`; `Origin` is log-only (never serialized); `Metadata` carries message args + reserved header keys.

---

## Rules

| | Rule |
|---|---|
| must | every `IQueryHandler` / `ICommandHandler` returns `AppResult<TSuccess>`; controllers `.Match` it |
| must | failures travel as `AppError` (or a subtype) — never a bare string, exception, or per-op flag across the boundary |
| must not | `Ok(dto)` / `return dto` / `return Unit` from a handler; `DomainError` / `FailureCategory` / `I{App}Failure` / `ISuccessResult` / `IFailureResult` (all removed) |
| may | attach `Success.Context` / `Failure.Context` (`IAppSuccessContext` / `IAppFailureContext`) for cross-cutting metadata |

---

## Throw and return bridge

A failure is expressible either way over the **same** `AppError`: `error.Throw()` · `result.ValueOrThrow()` · `result.ThrowIfFailure()` · `(() => op()).Attempt()` (catch → `Result`). The mediator **never throws** for `AppResult` requests — `ExceptionToResultBehavior` converts a throw to a `Failure` ([problem-details.md](problem-details.md)).

---
