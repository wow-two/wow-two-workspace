# Validation

*Last updated: 2026-07-17*

Input validation runs through the SDK `IValidator<T>` seam, backed by FluentValidation and assembly-scanned at startup.

## Layers

Two distinct mechanisms — do not conflate.

| Concern | Tool | When |
|---|---|---|
| External input (DTOs, requests, commands) | `IValidator<T>` + FluentValidation | At the boundary — before the request reaches domain logic |
| Internal precondition (constructor / method args) | `Guard.Against` (Ardalis) | Inside a type that has already been constructed with trusted-but-checked args |

Validation answers *"is this caller-supplied payload well-formed?"*; guards answer *"did my own code pass a sane argument?"*. See [Guards](#guards-vs-validators).

## Author validators

Validators are FluentValidation `AbstractValidator<T>` — one per validated type, `public sealed`, plain FluentValidation, no SDK base class.

- **Name** `{Type}Validator` — `{Command}Validator` for a command (`ProductCreateCommandValidator`). **Co-locate** with the type it validates (same folder as the command; see [mediator.md](../messaging/mediator.md)).
- **Summaries** — type: `Validates <see cref="{Type}"/>.`; constructor: `Configures the {action} field rules.`
- **Syntax** — one rule per `RuleFor`; each chained call on its own line (`.Must(...)` then `.WithMessage(...)`); a blank line between `RuleFor`s.
- **Messages** — omit `.WithMessage` when FluentValidation's default reads fine (it names the property); add one only where the rule's intent isn't obvious from the property and validator (e.g. a format check).
- **`nameof`** — use `nameof` wherever a rule references another member by name.
- **Shared predicates** — factor a reusable check into a static helper (`ProductValidation.IsValidRepo`) called via `.Must(...)`; don't inline the same lambda across validators.

```csharp
/// <summary>Validates <see cref="ProductCreateCommand"/>.</summary>
public sealed class ProductCreateCommandValidator : AbstractValidator<ProductCreateCommand>
{
    /// <summary>Configures the create-product field rules.</summary>
    public ProductCreateCommandValidator()
    {
        RuleFor(x => x.Slug)
            .NotEmpty();

        RuleFor(x => x.Name)
            .NotEmpty();

        RuleFor(x => x.Repo)
            .Must(ProductValidation.IsValidRepo)
            .WithMessage("Repo must be a 'owner/repo' reference (a single slash, no spaces, no scheme).");
    }
}
```

Multiple validators may target the same `T` — the adapter aggregates all of them.

## Register

Scan assemblies once at composition root via `AddFluentValidatorsFromAssemblies` — **never register `FluentValidation.IValidator<T>` directly** and never hand-bind the SDK `IValidator<T>`:

```csharp
builder.Services.AddFluentValidatorsFromAssemblies();                    // calling assembly
builder.Services.AddFluentValidatorsFromAssemblies(typeof(Program).Assembly);  // explicit
```

What the extension wires (in `ValidationServiceCollectionExtensions`):

- `AddValidatorsFromAssembly(..., includeInternalTypes: true)` — registers each `AbstractValidator<T>` as `FluentValidation.IValidator<T>`.
- `TryAddTransient(typeof(IValidator<>), typeof(FluentValidationAdapter<>))` — binds the **SDK** `IValidator<T>` to `FluentValidationAdapter<T>`, which fans out over the registered `FluentValidation.IValidator<T>[]`.

Consumers depend only on the SDK `IValidator<T>` (`src/Foundation/Validation/`) — the FluentValidation type stays an implementation detail behind the adapter.

## Consume

`IValidator<T>` exposes two entry points; pick by call site.

### Branch on the result (no throw)

`Validate(T)` returns a `ValidationError?` — `null` means valid, non-null is the aggregate failure. Branch on it:

```csharp
var error = validator.Validate(request);
if (error is not null)
    return AppResult<…>.Fail(error);   // error is a ValidationError : AppError
```

`ValidationError : AppError { IReadOnlyList<FieldError> Failures }` (`Type = Validation`); each `FieldError` is `(string Property, string Message, string Code)` — `Property` the member path, `Code` the stable rule code (FluentValidation `ErrorCode`).

### Throw for the pipeline

`ValidateAndThrow(T)` raises a `ValidationException` (a `ValidationException : AppException` whose `.Error` is the `ValidationError`) when any rule fails — used by the mediator `ValidationBehavior`; the terminal `ExceptionToResultBehavior` converts the throw to an `AppResult.Failure` ([problem-details.md](../presentation/problem-details.md)).

## Map to HTTP

A `ValidationError` is an `AppError` (`Type = Validation`) → `400` with an `errors:[{property,code,message}]` extension (from its `Failures`), rendered by the shared `AppErrorProblemDetailsFactory`. The controller just `.Match`es the `AppResult`; nothing hand-maps. See [problem-details.md](../presentation/problem-details.md).

## Guards vs. validators

`Guard.Against` (the Ardalis `IGuardClause` seam, re-exported with `NotSlug` / `NotUlid` wow-two extensions) is **not** a substitute for `IValidator<T>`:

- Guards throw `ArgumentException`-family exceptions for programmer-error preconditions — `Guard.Against.NullOrWhiteSpace(slug, nameof(slug))`.
- Validators produce structured, HTTP-mappable `ValidationError`s for caller-supplied input.

Do not run boundary input through `Guard.Against`, and do not model argument preconditions as `AbstractValidator<T>`.

---

## Open

Unresolved — this convention does not yet rule on either. Do not infer a rule from silence.

- **two-layer validation (presentation + persistence/infra)** — one validation pass at the representation boundary, a second before the write. Closes two gaps a single boundary pass
  leaves open: input validated at presentation then mutated internally and persisted unvalidated; input that never crossed presentation (a job, a consumer, a seeder) reaching infra
  unvalidated. Open: where the second pass binds (entity vs command), how error paths stay wire-shaped, and whether the two share rules.
- **caller-selected validation scope** — `AddMediatorValidationBehavior()` is generic and calls `ValidateAndThrow(T)`; the SDK `IValidator<T>` exposes no
  `Action<ValidationStrategy<T>>` overload, so FluentValidation **RuleSets are unreachable through the pipeline**. Blocks any scenario-scoped validation (`OnCreate` / `OnUpdate`,
  per-discriminator rules). Needs a whole-feature analysis before a rule lands; adopting rulesets requires an SDK change (strategy overload on `IValidator<T>` +
  `FluentValidationAdapter<T>`). Traced in `smart-qr-poc/engineering/planning/validation.md`.

## See also

- [result-pattern.md](result-pattern.md) — `Result`/`AppResult` carrying `AppError` · [problem-details.md](../presentation/problem-details.md) — `errors[]` rendering
- `src/Foundation/Validation/` (SDK) — `IValidator<T>`, `FieldError`, `ValidationError`, `ValidationException`, `FluentValidationAdapter<T>`, `AddFluentValidatorsFromAssemblies`
- `src/Foundation/Guards/` (SDK) — `Guard.Against`, `IGuardClause`, `NotSlug` / `NotUlid`
- [FluentValidation docs](https://docs.fluentvalidation.net/)
