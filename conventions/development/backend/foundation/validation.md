# Validation

*Last updated: 2026-07-25*

Input validation runs through the SDK `IValidator<T>` seam, backed by FluentValidation and assembly-scanned at startup.

## Layers

Two distinct mechanisms — do not conflate.

| Concern | Tool | When |
|---|---|---|
| External input (DTOs, requests, commands) | `IValidator<T>` + FluentValidation | At the boundary — before the request reaches domain logic |
| Internal precondition (constructor / method args) | `Guard.Against` (Ardalis) | Inside a type that has already been constructed with trusted-but-checked args |

Validation answers *"is this caller-supplied payload well-formed?"*; guards answer *"did my own code pass a sane argument?"*. See [Guards](#guards-vs-validators).

## Phases — existence first, then state reach

A command's checks run in a fixed order. Phase 1 is a gate; phases 2–3 are split by how far each must reach for its answer. Pattern names: `smart-qr-poc/engineering/planning/validation-patterns.md`. Ordering evidence + citations: `smart-qr-poc/engineering/research/error-ordering/error-ordering.md`.

> **Framing is not one of these phases.** Authentication (401), content-type negotiation (415), an unreadable body and an unparseable route id (400) are all resolved by the host before a handler exists — model binding and middleware own them. They precede everything below, we author none of them, and they are why the cheap-checks-first objection is already satisfied without splitting authored validation in two.

1. **Existence + ownership** — resolve the target entity; missing → `NotFound` (404), not-owned → `Forbidden` (403). Runs **before any field rule**. A **precondition** of phases 2–3, not a validation rule: it names no field the client sent, so it is an `AppError`, never a `ValidationError`.
2. **Static constraints** — decidable from the payload alone (shape, format, cross-field-within-payload). Pure, no I/O, via `IValidator<T>`. This is the bulk of validation.
3. **Transition constraints** — compare the candidate against the resolved prior state (immutable-once-set, legal state transition, monotonic field). Needs both states, so it runs only after phase 1. Enforced on the **entity** (the only object holding both states); the handler maps the outcome to a wire-shaped `ValidationError` (400).

- must resolve before running field rules for any command that targets an existing entity — a 404 that was true on the first request must not surface only after the client fixes a field.
- must not let the generic pipeline `ValidationBehavior` set that order — it runs ahead of the handler, so phase 2 would win. **Resolve in the command handler**, then call `validator.Validate(command)` and branch ([Consume](#branch-on-the-result-no-throw)). The pipeline behavior keeps commands that target nothing (create, query).
- a pre-validation mediator behavior would enforce the order without per-handler discipline; **deferred**, not rejected — it lands with the async-validation seam in one sweep, not piecemeal. Design already worked out: `smart-qr-poc/engineering/planning/validation.md` § *Phase-1 placement*.
- must return 404 for a well-formed id that matches no row — the client sent a syntactically valid value, so there is no field to name.
- must not read persisted state inside an `IValidator<T>` — phases 1 and 3 own that. A validator is pure.
- must emit a `ValidationError` (400) only for a field the **request carried**; a stateful failure with no such field is an `AppError` (404/403/409). The *layer* never decides this — the failure's nature does. A cross-aggregate uniqueness clash names a field the caller can fix, so it stays a `ValidationError` even though a lower layer decided it.
- a **transition constraint** (restricts *before→after* pairs) is not an **invariant** (holds at *every* state) — don't conflate them.
- must keep 400 for field failures, not 422 — the axis is genuinely unsettled (422 is core HTTP in RFC 9110 §15.5.21; DRF hard-codes 400, Zalando bans 422), so this is a consistency call, not a correctness one. Don't "fix" it.
- **422 does not cover a missing entity.** §15.5.21 scopes it to content the server understood but could not process — a semantic fault *in the payload*. A target that does not exist is 404's definition (§15.5.5). The 400-vs-422 question is only ever about field failures.

**Why this order.** No RFC mandates it — anyone citing one is overreading:

- the strongest normative statement is Google's AIP-211: check authorization **before** validating any request; AIP-193 puts permission before existence.
- RFC 9110 §13.2.1 implies the phase model — preconditions evaluate after normal request checks and *just before* the content is processed, so body processing is last and resolution precedes it.
- the security argument is **existence** masking, not field-shape secrecy: RFC 9110 §15.5.4 permits 404 in place of 403, and CWE-203/204 make any observable response difference the weakness. A field-level 400 emitted before the authz decision is such a difference — and existence you never resolved cannot be masked. That a 400 also leaks the resource's *field shape* is an inference (CWE-209 / OWASP BOPLA), not a cited rule.
- the counter-argument is real but narrow: OWASP's DoS guidance says run resource-cheap checks first. That is what phase 1 already does; it does not justify moving field-level rules ahead of the authz decision.
- the cost is one PK read spent on a well-framed but invalid payload. Accepted.

**ASP.NET Core defaults to the opposite order.** `[ApiController]`'s `ModelStateInvalidFilter` short-circuits with a 400 in the filter pipeline, before the action body where the 404 lives — and attribute-based authorization has the same inversion (it evaluates before model binding, so object-level 403s land after the 400 too). Inverting it means `SuppressModelStateInvalidFilter` or resolving in a resource filter. Our mediator pipeline is the same trap in different clothing, which is why the rule above names it.

## Layer independence

Validation repeats down the stack; layers do not delegate to each other.

- must have every layer validate as if no other validation layer exists — never assume an outer layer already checked.
- must keep each layer to **its own scope** — a presentation layer does not absorb cross-aggregate checks (sibling counts, uniqueness scans) to spare a service a query; those stay where they can reach the data, as an `AppError`.
- must not let a service skip existence + ownership because the caller already resolved the entity — the redundant read is what makes the layer independently correct.
- the duplicate read is fixed by **caching the resolution**, not by skipping the check. Caching is not wired yet; until then the extra query is accepted.

## Author validators

Validators are FluentValidation `AbstractValidator<T>` — one per validated type, `public sealed`, plain FluentValidation, no SDK base class.

- **Name** `{Concept}Validator` — `WifiContentValidator`, `ProductCreateCommandValidator`. **Co-locate** with the type it validates (same folder as the command; see [mediator.md](../messaging/mediator.md)).
- **Track the type name only when the concept has more than one model.** A validator names the *concept*, not the class. `WifiContentValueObject` gets `WifiContentValidator` — there is one wifi-content model, so nothing is ambiguous, and dragging a role suffix into the validator name buys a longer identifier and no information.
- **When a concept does have several models across layers** (`ProductEntity` + `ProductDto` + `ProductCreateRequest`), each validator carries the full type name so the target is unambiguous. That is the case the `{Type}Validator` shape exists for.
- a role suffix on the model (`Entity` / `Dto` / `ValueObject`) is a **statement about the model**, not about what validates it — renaming the model must not force a validator rename.
- **Summaries** — type: `Validates <see cref="{Type}"/>.`; constructor: `Configures the {action} field rules.`
- **Syntax** — one rule per `RuleFor`; each chained call on its own line (`.Must(...)` then `.WithMessage(...)`); a blank line between `RuleFor`s.
- **Messages** — omit `.WithMessage` when FluentValidation's default reads fine (it names the property); add one only where the rule's intent isn't obvious from the property and validator (e.g. a format check).
- **`nameof`** — use `nameof` wherever a rule references another member by name.
- **Shared predicates** — factor a reusable check into a static helper (`ProductValidation.IsValidRepo`) called via `.Must(...)`; don't inline the same lambda across validators.
- **Cross-reference a composed validator** — a validator that nests another via `SetValidator` / `SetInheritanceValidator` / `RuleForEach` must name it in a type-level `<seealso cref="..."/>`, with a one-line note that a member added to the nested type needs a rule added there. **Outer → inner only**: an inner validator never references its callers, so the link stays one-way and adds no dependency. Doc comments, not code — the no-mutual-knowledge rule is about references, not documentation. *Exception:* a validator dispatching over a closed union already lists every branch in its constructor, so a `<remarks>` pointing at that table replaces the per-subtype `<seealso>`.

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

`ValidationError : AppError { IReadOnlyList<FieldError> Failures }` (`Type = Validation`); each `FieldError` is `(string Property, string Message, string Code, IReadOnlyDictionary<string, object>? Params)` — `Property` the member path, `Code` the stable rule code (FluentValidation `ErrorCode`), `Params` the rule's operands ([Rule codes and operands](#rule-codes-and-operands)).

### Throw for the pipeline

`ValidateAndThrow(T)` raises a `ValidationException` (a `ValidationException : AppException` whose `.Error` is the `ValidationError`) when any rule fails — used by the mediator `ValidationBehavior`; the terminal `ExceptionToResultBehavior` converts the throw to an `AppResult.Failure` ([problem-details.md](../presentation/problem-details.md)).

## Map to HTTP

A `ValidationError` is an `AppError` (`Type = Validation`) → `400` with an `errors:[{property,code,message}]` extension (from its `Failures`), rendered by the shared `AppErrorProblemDetailsFactory`. The controller just `.Match`es the `AppResult`; nothing hand-maps. See [problem-details.md](../presentation/problem-details.md).

**Carry the field path at every layer.** A machine-readable location is the cross-ecosystem norm — JSON:API `source.pointer`, AIP-193 `FieldViolation.field`, ASP.NET `ValidationProblemDetails.errors`, Laravel dot keys, Zod `path`. Dropping it is the outlier.

- must emit a **domain member path** in `FieldError.Property`, never a wire path — a service knows `Code.Slug`, not `rules[0].content.url`. The factory camelCases; the client maps.
- a client maps the path onto its own model, attaches the message to that field, and renders anything unmapped at form level. A lower layer's model may be wider than the client's, so unmapped paths are expected.
- this stays cheap only while the wire and domain models are kept symmetric. Diverge them and the API layer needs a translation table.
- watch the silent-drop trap: a path the client's form recognises but no component renders falls into neither bucket and vanishes. Collapse such a path onto the bound one before filing it (worked example: `smart-qr-poc/.../createCodeForm.ts` `mapCodeFieldPath`).

## Rule codes and operands

A failure carries a machine tag and its operands so a **consumer can re-render it** — in its own wording or its own language — rather than
display `Message` verbatim. That is what lets a client-caught and a server-caught failure of one rule read identically instead of speaking with
two voices. The frontend SDK renders from these (`@wow-two-beta/ui` `foundation/validation` `createMessageResolver`).

- must let `FluentValidationAdapter<T>` populate `Code` and `Params` — never hand-build a `FieldError` where a validator ran.
- must declare a secret-bearing member on the **validator** via `ISensitiveMembers`, not by a global name rule — sensitivity is a property of the
  operation. Sign-up must state the required password length; sign-in must not; both validate `Password`.
- a declared member reports no operands at all — key redaction leaves `TotalLength`, which discloses the secret's length.
- `PropertyValue` / `PropertyPath` never reach `Params`, whatever a validator declares.
- `Params` keys stay FluentValidation's placeholder names (`MaxLength`, `From`, `To`); the client maps them on read. Server-side normalization via
  `ValidatorOptions.Global.ErrorCodeResolver` is **deferred** — adopt only when a consumer needs the wire itself normalized.
- `PropertyName` in `Params` is the **display** name — `.WithName()` makes it diverge from `Property`.
- a rule comparing against nothing (`NotEmpty`) contributes no operands.

## Advisory rules

A rule that should guide without blocking is `.WithSeverity(Severity.Warning)` — not a second rule set, not a second validator.

- must keep an advisory rule in the same validator as the blocking ones — one rule set, two verdicts.
- `Validate` / `ValidateAndThrow` see `Error` only; `Inspect` returns every severity and makes no verdict.
- must expose an advisory read as a **sub-resource** (`POST /codes/validate`), never a bespoke HTTP verb — none of the registered verbs means "check this".
- must not let a warning influence a write path — if it should block, it is an `Error`.

## Localize field messages

`IErrorMessageResolver` resolves the top-level `detail`. `errors[].message` bypasses it, so a response would otherwise be localized in one and
English in the other.

- must resolve a field message through `IFieldErrorMessageResolver` (`src/Foundation/Validation/`) — the SDK registers a passthrough default, so
  the seam is wired and the translation is opt-in.
- must register a custom resolver **before** `AddErrorHttpStatusMapping` — the SDK default is `TryAdd`.
- reach for a per-rule `IStringLocalizer` inside `.WithMessage("…")` when the code-keyed table isn't enough — the only authored string in a validator.
- the request culture is already on `CultureInfo.CurrentUICulture` under `UseRequestLocalizationConventions`.
- a frontend on the SDK message catalogue renders from `Code` and needs none of this.
- this serves every other consumer — another service, a mobile client, a direct API caller.

## Guards vs. validators

`Guard.Against` (the Ardalis `IGuardClause` seam, re-exported with `NotSlug` / `NotUlid` wow-two extensions) is **not** a substitute for `IValidator<T>`:

- Guards throw `ArgumentException`-family exceptions for programmer-error preconditions — `Guard.Against.NullOrWhiteSpace(slug, nameof(slug))`.
- Validators produce structured, HTTP-mappable `ValidationError`s for caller-supplied input.

Do not run boundary input through `Guard.Against`, and do not model argument preconditions as `AbstractValidator<T>`.

---

## Open

Unresolved — this convention does not yet rule on either. Do not infer a rule from silence.

- **two-layer validation — rule sharing.** § *Layer independence* settles the principle; the lower pass binds at **service level** (analysed in `smart-qr-poc/engineering/planning/validation.md` § *Lower-pass placement* — an EF interceptor sees only the tracked graph and fires too late; a repository guard would have to cross-inject repositories). Pending owner sign-off, then it moves into § *Layer independence* as a rule. What stays open: whether the service pass shares rule definitions with phase 2 — sharing risks pulling I/O-free rules into a layer that has database reach. Also unsettled: a check-then-write probe is racy, so a DB constraint must back anything that must hold.
- **Dapper-read entity attached to EF for a write** — measured in `smart-qr-poc/engineering/research/data-seam/` (POC). `Attach` snapshots `OriginalValues` from the **current instance**, so the order is **load → attach → mutate**; mutate-then-attach reads `Unchanged` and **silently drops the write**. `AsNoTracking` keeps no snapshot at all. `EntityEntry.OriginalValues` is therefore not a "compare against previous" source pre-handler; `GetDatabaseValues()` recovers the stored row at the cost of a second query. A Dapper-materialized entity also needs EF's value converters (jsonb) applied by hand. The read-seam design is a backend-SDK task.
- **caller-selected validation scope** — `AddMediatorValidationBehavior()` is generic and calls `ValidateAndThrow(T)`; the SDK `IValidator<T>` exposes no
  `Action<ValidationStrategy<T>>` overload, so FluentValidation **RuleSets are unreachable through the pipeline**. Blocks any scenario-scoped validation (`OnCreate` / `OnUpdate`,
  per-discriminator rules). Needs a whole-feature analysis before a rule lands; adopting rulesets requires an SDK change (strategy overload on `IValidator<T>` +
  `FluentValidationAdapter<T>`). Traced in `smart-qr-poc/engineering/planning/validation.md`.

## See also

- [result-pattern.md](result-pattern.md) — `Result`/`AppResult` carrying `AppError` · [problem-details.md](../presentation/problem-details.md) — `errors[]` rendering
- `src/Foundation/Validation/` (SDK) — `IValidator<T>`, `FieldError`, `ValidationError`, `ValidationException`, `FluentValidationAdapter<T>`, `AddFluentValidatorsFromAssemblies`
- `src/Foundation/Guards/` (SDK) — `Guard.Against`, `IGuardClause`, `NotSlug` / `NotUlid`
- [FluentValidation docs](https://docs.fluentvalidation.net/)
