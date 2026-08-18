# Validation

*Last updated: 2026-08-18*

> Deciding whether caller-supplied input is well-formed, and where each check is allowed to reach.
> Purpose — a layer that skips a check because another layer ran it stops being independently correct.
> Use case — authoring a validator, wiring the pipeline, or mapping a failure to HTTP.

The validator's declaration is a [component](../../constructs/behavior/validator.md); the rest below is this domain's.

---

## Layers

Two distinct mechanisms — do not conflate.

- **External input** (DTOs, requests, commands) → `IValidator<T>` + FluentValidation.
  - at the boundary, before the request reaches domain logic.
- **Internal precondition** (constructor / method args) → `Guard.Against` (Ardalis).
  - inside a type already constructed with trusted-but-checked args.

Validation asks *is this caller-supplied payload well-formed?*;
a [guard](#guards-vs-validators) asks *did my own code pass a sane argument?*

---

## Phases — existence first, then state reach

A command's checks run in a fixed order — phase 1 gates, phases 2–3 split by how far each must reach.

- pattern names: `smart-qr-poc/engineering/planning/validation-patterns.md`
- ordering evidence and citations: `smart-qr-poc/engineering/research/error-ordering/error-ordering.md`

> **Framing is not one of these phases.** Authentication (401), content-type negotiation (415), an unreadable
> body and an unparseable route id (400) all resolve in model binding and middleware, before a handler exists.
> They precede everything below, we author none of them, and they satisfy the cheap-checks-first
> objection without splitting authored validation in two.

1. **Existence + ownership** — resolve the target entity; missing → `NotFound` (404), not-owned → `Forbidden`
   (403). Runs **before any field rule**. A **precondition** of phases 2–3, not a validation rule: it names no
   field the client sent — an `AppError`, never a `ValidationError`.
2. **Static constraints** — decidable from the payload alone: shape, format, cross-field within the payload.
   Pure, no I/O, via `IValidator<T>` — the bulk of validation.
3. **Transition constraints** — compare the candidate against the resolved prior state: immutable-once-set,
   legal state transition, monotonic field. Needs both states, so it runs only after phase 1. Enforced on the
   **entity**, the only object holding both; the handler maps the outcome to a `ValidationError` (400).

- must resolve before any field rule when a command targets an existing entity.
- a 404 true on the first request must not surface only after the client fixes a field.
- must not let the generic pipeline `ValidationBehavior` set that order — it runs ahead of the handler, so
  phase 2 would win.
- must resolve in the command handler, then call `validator.Validate(command)` and
  [branch](#branch-on-the-result-no-throw).
- must leave commands that target nothing — create, query — to the pipeline behavior.
- a pre-validation mediator behavior would enforce the order without per-handler discipline.
- **deferred**, not rejected — it lands with the async-validation seam in one sweep, not piecemeal.
- designed in `smart-qr-poc/engineering/planning/validation.md` § *Phase-1 placement*.
- must return 404 for a well-formed id that matches no row.
- the value is syntactically valid, so there is no field to name.
- must not read persisted state inside an `IValidator<T>` — a validator is pure; phases 1 and 3 own that.
- must emit a `ValidationError` (400) only for a field the **request carried**.
- a stateful failure naming no such field is an `AppError` (404/403/409).
- must let the failure's nature decide that, never the layer.
- a cross-aggregate uniqueness clash names a fixable field — a `ValidationError`, even if a lower layer decided it.
- a **transition constraint** restricts *before→after* pairs; an **invariant** holds at *every* state.
- don't conflate them.
- must keep 400 for field failures, not 422 — a consistency call, not a correctness one.
- the axis is unsettled: RFC 9110 §15.5.21 makes 422 core HTTP, DRF hard-codes 400, Zalando bans 422.
- must not "fix" that 400 to a 422.
- **422 does not cover a missing entity**.
- §15.5.21 scopes it to content the server understood but could not process — a semantic fault *in the payload*.
- a target that does not exist is 404 (§15.5.5).
- the 400-vs-422 question is only ever about field failures.

**Why this order.** No RFC mandates it — anyone citing one is overreading:

- Google's AIP-211 is the strongest normative statement: authorize **before** validating any request.
- AIP-193 puts permission before existence.
- RFC 9110 §13.2.1 implies the phase model — preconditions evaluate after normal request checks.
- they evaluate *just before* the content is processed, so body processing is last and resolution precedes it.
- the security argument is **existence** masking, not field-shape secrecy.
- §15.5.4 permits 404 in place of 403, and CWE-203/204 make any observable response difference the weakness.
- a field-level 400 emitted before the authz decision is such a difference.
- existence you never resolved cannot be masked.
- that a 400 also leaks the resource's *field shape* is an inference (CWE-209 / OWASP BOPLA), not a cited rule.
- the counter-argument is real but narrow: OWASP's DoS guidance runs resource-cheap checks first.
- phase 1 already does that.
- it justifies moving no field rule ahead of the authz decision.
- the cost is one PK read spent on a well-framed but invalid payload. Accepted.

**ASP.NET Core defaults to the opposite order.**

- `[ApiController]`'s `ModelStateInvalidFilter` short-circuits with a 400 in the filter pipeline.
- that is before the action body where the 404 lives.
- attribute-based authorization inverts the same way — it evaluates before model binding.
- object-level 403s land after the 400 too.
- inverting it means `SuppressModelStateInvalidFilter`, or resolving in a resource filter.
- our mediator pipeline is the same trap in different clothing — the rule above names it.

---

## Layer independence

Validation repeats down the stack; layers do not delegate to each other.

- must have every layer validate as if no other did — never assume an outer layer checked.
- must keep each layer to **its own scope**.
- a presentation layer absorbs no cross-aggregate check (sibling counts, uniqueness scans) to spare a query.
- those stay where they reach the data, as an `AppError`.
- must not let a service skip existence + ownership because the caller already resolved the entity.
- the redundant read is what makes the layer independently correct.
- the duplicate read is fixed by **caching the resolution**, never by skipping the check.
- caching is not wired yet, so the extra query is accepted until then.

---

## Author validators

One per validated type, plain FluentValidation, no SDK base class — declaration rules in
[validator](../../constructs/behavior/validator.md).

- must name it `{Concept}Validator` — `WifiContentValidator`, `ProductCreateCommandValidator`.
- must co-locate it with the type it validates, in the command's own folder
  ([mediator](../messaging/mediator/mediator.md)).
- must track the type name only when the concept has more than one model.
- a validator names the *concept*, not the class — `WifiContentValueObject` gets `WifiContentValidator`.
- a role suffix there buys a longer identifier and no information.
- must give each validator the full type name when a concept spans several models across layers.
- `ProductEntity` + `ProductDto` + `ProductCreateRequest` — that is what the `{Type}Validator` shape exists for.
- a role suffix on the model (`Entity` / `Dto` / `ValueObject`) describes the model, not its validator.
- renaming the model must force no validator rename.
- must summarize the type `Validates <see cref="{Type}"/>.`
- must summarize the constructor `Configures the {action} field rules.`
- must write one rule per `RuleFor`, each chained call on its own line — `.Must(...)` then `.WithMessage(...)`.
- must leave a blank line between `RuleFor`s.
- may use `=>` for a member that returns or delegates ([style](../../../lla/notation/style/style.md) § *The body*).
- must give the constructor a block body — the syntax rule above puts each chained call on its own line.
- must omit `.WithMessage` while FluentValidation's default reads fine — it names the property.
- must add one only where the rule's intent is not obvious from the property and validator, as in a format check.
- must use `nameof` wherever a rule references another member by name.
- must factor a reusable check into a static helper called via `.Must(...)` — `ProductValidation.IsValidRepo`.
- must not inline the same lambda across validators.
- must name a nested validator in a type-level `<seealso cref="..."/>`.
- nested = `SetValidator` · `SetInheritanceValidator` · `RuleForEach`.
- must add a one-line note that a member added to the nested type needs a rule added there.
- must keep the link **outer → inner only** — an inner validator references no caller, so it adds no dependency.
- the no-mutual-knowledge rule is about references, not documentation, so doc comments carry this, never code.
- may replace the per-subtype `<seealso>` with a `<remarks>` pointing at the constructor's branch table.
- only when the validator dispatches over a closed union already listing every branch.

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

Multiple validators may target the same `T` — the adapter aggregates them.

---

## Register

- must scan assemblies once at the composition root via `AddFluentValidatorsFromAssemblies`.
- must not register `FluentValidation.IValidator<T>` directly, and must not hand-bind the SDK `IValidator<T>`.
- must depend only on the SDK `IValidator<T>` (`src/Foundation/Validation/`).
- FluentValidation stays an implementation detail behind the adapter.

```csharp
builder.Services.AddFluentValidatorsFromAssemblies();                    // calling assembly
builder.Services.AddFluentValidatorsFromAssemblies(typeof(Program).Assembly);  // explicit
```

What `ValidationServiceCollectionExtensions` wires:

- `AddValidatorsFromAssembly(..., includeInternalTypes: true)` — registers each `AbstractValidator<T>` as
  `FluentValidation.IValidator<T>`.
- `TryAddTransient(typeof(IValidator<>), typeof(FluentValidationAdapter<>))` — binds the **SDK** `IValidator<T>`
  to `FluentValidationAdapter<T>`, which fans out over the registered `FluentValidation.IValidator<T>[]`.

---

## Consume

`IValidator<T>` exposes two entry points; pick by call site.

### Branch on the result (no throw)

`Validate(T)` returns a `ValidationError?` — `null` means valid, non-null is the aggregate failure. Branch on it:

```csharp
var error = validator.Validate(request);
if (error is not null)
    return AppResult<…>.Fail(error);   // error is a ValidationError : AppError
```

`ValidationError : AppError { IReadOnlyList<FieldError> Failures }`, `Type = Validation`. A `FieldError` is
`(string Property, string Message, string Code, IReadOnlyDictionary<string, object>? Params)`:

- `Property` — the member path.
- `Code` — the stable rule code, FluentValidation's `ErrorCode`.
- `Params` — the rule's operands ([rule codes and operands](#rule-codes-and-operands)).

### Throw for the pipeline

`ValidateAndThrow(T)` raises a `ValidationException : AppException` whose `.Error` is the `ValidationError`,
when any rule fails. The mediator `ValidationBehavior` uses it; the terminal `ExceptionToResultBehavior`
converts the throw to an `AppResult.Failure` ([problem details](../../platform/responses/problem-details.md)).

---

## Map to HTTP

A `ValidationError` is an `AppError` (`Type = Validation`) → `400` with an `errors:[{property,code,message}]`
extension built from its `Failures`, rendered by the shared `AppErrorProblemDetailsFactory`
([problem details](../../platform/responses/problem-details.md)).

- must `.Match` the `AppResult` in the controller, and hand-map nothing.

**Carry the field path at every layer.** A machine-readable location is the cross-ecosystem norm — JSON:API
`source.pointer`, AIP-193 `FieldViolation.field`, ASP.NET `ValidationProblemDetails.errors`, Laravel dot keys,
Zod `path`. Dropping it is the outlier.

- must emit a **domain member path** in `FieldError.Property`, never a wire path.
- a service knows `Code.Slug`, not `rules[0].content.url`; the factory camelCases, and the client maps.
- a client maps the path onto its own model and attaches the message to that field.
- anything unmapped renders at form level.
- a lower layer's model may be wider than the client's, so unmapped paths are expected.
- this stays cheap only while the wire and domain models are kept symmetric.
- diverge them and the API layer needs a translation table.
- must collapse a path the client's form recognises but no component renders onto the bound one, before filing it.
- otherwise it falls into neither bucket and vanishes.
- worked example — `smart-qr-poc/.../createCodeForm.ts` `mapCodeFieldPath`.

---

## Rule codes and operands

A failure carries a machine tag and its operands so a **consumer can re-render it** — in its own wording or
language — rather than display `Message` verbatim. That is what lets a client-caught and a server-caught failure
of one rule read identically instead of in two voices. The frontend SDK renders from these
(`@wow-two-beta/ui` `foundation/validation` `createMessageResolver`).

- must let `FluentValidationAdapter<T>` populate `Code` and `Params`.
- must not hand-build a `FieldError` where a validator ran.
- must declare a secret-bearing member on the **validator** via `ISensitiveMembers`, never by a global name rule.
- sensitivity is a property of the operation — sign-up must state the required password length.
- sign-in must not, and both validate `Password`.
- a declared member reports no operands at all.
- key redaction leaves `TotalLength`, which discloses the secret's length.
- `PropertyValue` / `PropertyPath` never reach `Params`, whatever a validator declares.
- `Params` keys stay FluentValidation's placeholder names (`MaxLength`, `From`, `To`).
- the client maps them on read.
- server-side normalization via `ValidatorOptions.Global.ErrorCodeResolver` is **deferred**.
- adopt it only when a consumer needs the wire itself normalized.
- `PropertyName` in `Params` is the **display** name — `.WithName()` makes it diverge from `Property`.
- a rule comparing against nothing (`NotEmpty`) contributes no operands.

---

## Advisory rules

A rule that should guide without blocking is `.WithSeverity(Severity.Warning)` — not a second rule set, and not
a second validator.

- must keep an advisory rule in the same validator as the blocking ones — one rule set, two verdicts.
- `Validate` / `ValidateAndThrow` see `Error` only; `Inspect` returns every severity and makes no verdict.
- must expose an advisory read as a **sub-resource** (`POST /codes/validate`), never a bespoke HTTP verb.
- none of the registered verbs means "check this".
- must not let a warning influence a write path — if it should block, it is an `Error`.

---

## Localize field messages

`IErrorMessageMapper` maps the top-level `detail`; `errors[].message` bypasses it, so a response would
otherwise be localized in one and English in the other.

> **Ships as `IErrorMessageResolver` / `IFieldErrorMessageResolver`** until the SDK sweep lands the
> `Resolver → Mapper` fold ([components](../../constructs/constructs.md) § *Folds*). The canonical name is
> written here; the shipped name is what compiles today.

- must map a field message through `IFieldErrorMessageMapper` (`src/Foundation/Validation/`).
- the SDK's passthrough default wires the seam, so the translation is opt-in.
- must register a custom mapper **before** `AddErrorHttpStatusMapping` — the SDK default is `TryAdd`.
- may reach for a per-rule `IStringLocalizer` inside `.WithMessage("…")` when the code-keyed table falls short.
- that is the only authored string in a validator.
- the request culture is already on `CultureInfo.CurrentUICulture` under `UseRequestLocalizationConventions`.
- a frontend on the SDK message catalogue renders from `Code` and needs none of this.
- this serves every other consumer — another service, a mobile client, a direct API caller.

---

## Guards vs. validators

`Guard.Against` — the Ardalis `IGuardClause` seam, re-exported with `NotSlug` / `NotUlid` wow-two extensions —
is **not** a substitute for `IValidator<T>`.

- a guard throws an `ArgumentException`-family exception for a programmer-error precondition.
- `Guard.Against.NullOrWhiteSpace(slug, nameof(slug))`.
- a validator produces a structured, HTTP-mappable `ValidationError` for caller-supplied input.
- must not run boundary input through `Guard.Against`.
- must not model an argument precondition as an `AbstractValidator<T>`.

---

## Open

Unresolved — this convention does not yet rule on either. Do not infer a rule from silence.

- **two-layer validation — rule sharing.** § *Layer independence* settles the principle; the lower pass binds
  at **service level**.
  - an EF interceptor sees only the tracked graph and fires too late.
  - a repository guard would have to cross-inject repositories.
  - pending owner sign-off, it moves into § *Layer independence* as a rule.
  - open: whether the service pass shares rule definitions with phase 2 — sharing risks pulling I/O-free rules
    into a layer that has database reach.
  - also unsettled: a check-then-write probe is racy, so a DB constraint must back anything that must hold.
  - analysed in `smart-qr-poc/engineering/planning/validation.md` § *Lower-pass placement*.
- **Dapper-read entity attached to EF for a write** — measured in
  `smart-qr-poc/engineering/research/data-seam/` (POC).
  - `Attach` snapshots `OriginalValues` from the **current instance**, so the order is load → attach → mutate.
  - mutate-then-attach reads `Unchanged` and **silently drops the write**; `AsNoTracking` keeps no snapshot.
  - `EntityEntry.OriginalValues` is therefore no "compare against previous" source pre-handler.
  - `GetDatabaseValues()` recovers the stored row, at the cost of a second query.
  - a Dapper-materialized entity also needs EF's value converters (jsonb) applied by hand.
  - the read-seam design is a backend-SDK task.
- **caller-selected validation scope** — `AddMediatorValidationBehavior()` is generic and calls
  `ValidateAndThrow(T)`, and the SDK `IValidator<T>` exposes no `Action<ValidationStrategy<T>>` overload.
  - FluentValidation **RuleSets are therefore unreachable through the pipeline**.
  - blocks any scenario-scoped validation — `OnCreate` / `OnUpdate`, per-discriminator rules.
  - adopting rulesets requires an SDK change: a strategy overload on `IValidator<T>` plus
    `FluentValidationAdapter<T>`.
  - needs a whole-feature analysis before a rule lands. Traced in
    `smart-qr-poc/engineering/planning/validation.md`.
