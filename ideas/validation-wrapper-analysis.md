# Custom validation wrapper over FluentValidation — is it needed?

*Last updated: 2026-07-27*

> **Status:** analysis, nothing built. Spun out of the shared-validation vector after its frontend half
> shipped (`shared-validation-spec.md`). Answers one question: do error codes, translated messages, and
> config-sourced rule operands need a wrapper type over FluentValidation, or do FV's own hooks carry them?
>
> **Every signature below was reflected off `FluentValidation 11.11.0`** — the version pinned in
> `Directory.Packages.props:129`. Not recalled from docs.

## Verdict

**No wrapper type. Three global hooks plus one extension-method surface.**

- codes, translations, and operands are all served by `ValidatorOptions.Global` — FV already exposes exactly
  the seams the vector needs, and none of them require touching how a validator is authored.
- config-sourced operands are the one genuinely unserved ask, and the thing that serves them is a handful of
  rule-builder extensions, not a base class.
- a base class is also **ruled out by convention** — `conventions/development/backend/foundation/validation.md`
  § *Author validators* says validators are "plain FluentValidation `AbstractValidator<T>`, **no SDK base
  class**". Global config and extension methods leave that rule intact; a `WowTwoValidator<T>` breaks it.

---

## The hooks that already exist

Reflected off `FluentValidation.ValidatorConfiguration` (11.11.0):

| Hook | Type | Serves |
|---|---|---|
| `OnFailureCreated` | `Func<ValidationFailure, IValidationContext, object, IValidationRule, IRuleComponent, ValidationFailure>` | **everything post-hoc** — rewrite code, stamp params, replace message, per failure |
| `ErrorCodeResolver` | `Func<IPropertyValidator, string>` | the default `ErrorCode` per built-in validator |
| `LanguageManager` | `ILanguageManager` | translated default messages |
| `MessageFormatterFactory` | `Func<MessageFormatter>` | how placeholders render into a message |
| `DisplayNameResolver` | `Func<Type, MemberInfo, LambdaExpression, string>` | the property name a message says |

`ILanguageManager` is 3 members — `Enabled`, `Culture`, `GetString(key, culture)`. Its concrete
`LanguageManager` also carries `AddTranslation(language, key, message)` and `Clear()`; both exist in the
assembly but are absent from the shipped XML docs, so treat them as unsupported surface and implement the
interface instead.

`ValidationFailure.FormattedMessagePlaceholderValues` is a public dictionary on every failure — the operands
(`MaxLength`, `ComparisonValue`, `From`/`To`, …) FV already computed and that the SDK adapter currently drops.

---

## Ask 1 · Error codes

**Served. `ErrorCodeResolver`, one line at composition root.**

- FV's default code is the validator type name (`NotEmptyValidator`). The shared vocabulary wants `required`.
- `ErrorCodeResolver` maps `IPropertyValidator` → code globally, so every rule reports the shared vocabulary
  without a single `.WithErrorCode` at any call site.
- an explicit `.WithErrorCode("slugTaken")` still wins per-rule — the resolver only supplies the *default*.
- the frontend already normalizes on read (`FLUENT_VALIDATION_CODES`), so this is not urgent. Doing it makes
  the wire honest and turns the client alias table into a passthrough rather than a translation.

**Watch:** the resolver receives the validator instance only — no member, no type. A code that must vary by
member cannot come from here; that is `.WithErrorCode` territory.

---

## Ask 2 · Translated error messages

**Served, and the request-culture plumbing is already shipped.**

Two layers, and they answer different questions:

- **default messages** — `ILanguageManager` implementation set on `ValidatorOptions.Global.LanguageManager`.
  `GetString(key, culture)` is called per failure; FV ships translations for ~15 languages already. Culture
  falls through to `CultureInfo.CurrentUICulture`, which `UseRequestLocalizationConventions`
  (`src/Localization/`) already sets per request. So this is *wiring*, not building.
- **authored messages** — a `.WithMessage("URL is required.")` literal is invisible to the language manager.
  Localizing those needs `.WithMessage(x => localizer["Code.Url.Required"])` with an injected
  `IStringLocalizer<T>`, i.e. per-validator work, or the catalogue on the client renders them instead.

**The real gap is downstream of FV, not inside it.** `AppErrorProblemDetailsFactory` runs
`IErrorMessageResolver` over `problem.Detail` and passes `validationError.Failures` through untouched — so
`errors[].message` never reaches resx even once the language manager is wired. That is the fix worth doing
regardless of which layer authors the string.

**Ordering note.** With the client catalogue shipped, server-side translation is now optional for
form-rendered failures — the client renders from a code. It stays mandatory for every non-form consumer
(mobile, another service, a direct API caller), which is the argument for doing it anyway.

---

## Ask 3 · Operands (params)

**Served by `OnFailureCreated`, and it is the precondition for Ask 4.**

- FV computes the operands and hangs them on `FormattedMessagePlaceholderValues`; the SDK's
  `FluentValidationAdapter` builds `FieldError` from `PropertyName` / `ErrorMessage` / `ErrorCode` only.
- so the cheapest fix is **not** a hook at all — it is reading the dictionary the adapter already has in hand.
  `OnFailureCreated` matters only for stamping operands a custom rule computed itself.
- without operands the catalogue can render presence rules but not size or comparison rules, which is most of
  what a form shows.

---

## Ask 4 · Config-based validation (baked vs config)

**The only genuinely unserved ask.** FV has no notion of a rule operand sourced from configuration.

`RuleFor(x => x.Name).MaximumLength(50)` bakes `50` into the assembly. Wanting it per-tenant, per-plan, or
per-environment is a real requirement (`Free` plan caps at 5 rules, `Pro` at 500) and nothing in FV addresses it.

Three shapes, in ascending cost:

- **read config inside the predicate.** `.Must((v) => v.Length <= monitor.CurrentValue.MaxName)` — live values,
  works today, zero new surface. **Costs the built-in validator**, so the failure reports
  `PredicateValidator` with no operands, and its message is a baked literal that will disagree with the
  configured bound. Usable only with `.WithErrorCode("max")` + a hand-stamped placeholder, at every call site.
- **config-aware rule builders (recommended).** An extension surface —
  `RuleFor(x => x.Name).MaximumLengthFrom(o => o.MaxNameLength)` — that reads `IOptionsMonitor<T>` inside the
  predicate *and* emits the right code and operands automatically. Small (one extension per constrained rule
  kind), keeps validators plain `AbstractValidator<T>`, and is the only shape where a config-driven bound and
  its rendered message cannot disagree.
- **rules defined entirely in config.** A declarative rule table loaded at startup and compiled to FV rules.
  Real single-source, real cost, and it re-opens the neutral-format question that
  `shared-validation-spec.md` already ruled incompatible with § *Layer independence*. Not recommended.

**The dependency worth naming:** config-sourced operands are only correct once Ask 3 lands. A rule whose bound
comes from config but whose message is baked will state the wrong number the first time an operator changes it.
Params are a precondition, not a companion.

**The client half.** If the server's bound is configurable, the client's must not be hard-coded, or the two
drift in the direction that costs — client stricter than server locks a user out of something the server would
accept. Two safe answers: drop the bound client-side and let the server own it (lax drift is free), or serve
the bounds to the client. The FE SDK already has the carrier for the second —
`foundation/config` `defineConfig` reads runtime `window.__APP_CONFIG__` ahead of build-time env.

---

## What a wrapper would and would not buy

| Concern | Wrapper needed? | Why |
|---|---|---|
| shared error codes | no | `ErrorCodeResolver`, global, one line — deferred, nothing needs it |
| translated default messages | no | `ILanguageManager`, global; culture already per-request |
| translated authored messages | no | `IFieldErrorMessageResolver` (shipped), or per-rule `IStringLocalizer` |
| operands on the wire | no | read `FormattedMessagePlaceholderValues` in the existing adapter — shipped |
| config-sourced operands | **extensions, not a type** | needs its own rule builders to keep code + operands right |
| rules from a declarative table | yes, and don't | re-opens the neutral-format conflict |

A wrapper *type* buys discoverability and nothing else, at the cost of a convention rule and a layer between
every validator and the library it is written in.

---

## Build order — status

1. **DONE** — `FluentValidationAdapter` carries `FormattedMessagePlaceholderValues` onto `FieldError.Params`,
   stripping `PropertyValue` / `PropertyPath`.
2. **DEFERRED** (owner, 2026-07-27) — `ErrorCodeResolver`. No product needs a normalized wire; the client alias
   table covers it. Revisit when a non-JS consumer reads the codes.
3. **DONE (the plug, not the translation)** — `IFieldErrorMessageResolver` + passthrough default, wired through
   all four handlers. `.WithMessage` is confirmed as the localization point; the resx implementation waits
   until an app needs a non-English validator message.
4. **BLOCKED on a real bound** — config-aware rule builders (`MaximumLengthFrom(…)`). Shape settled below.
5. **BLOCKED on (4)** — the client half: drop the bound, or publish it through `foundation/config`.

---

## Config-sourced operands — the settled shape (owner, 2026-07-27)

**Per-tenant, via a dictionary of configs keyed by tenant id; the validator switches on it at predicate time.**

```csharp
public sealed class CodeCreateCommandValidator : AbstractValidator<CodeCreateCommand>
{
    public CodeCreateCommandValidator(IOptionsMonitor<ValidationBoundsOptions> bounds, ITenantContext tenant)
    {
        RuleFor(x => x.Rules)
            .MaximumCountFrom(() => bounds.CurrentValue.For(tenant.Id).MaxRules);
    }
}
```

- the dictionary is `Dictionary<TenantId, Bounds>` with a default entry — a tenant with no row gets the
  default rather than a missing-key throw.
- the lookup happens **inside the predicate**, not at rule-build time. A validator is built once; the tenant
  changes per request, so a bound read in the constructor would freeze the first request's tenant into every
  later one. This is the one detail that makes the whole shape correct or silently wrong.
- `ITenantContext` must therefore be resolvable at validate time. Validators are registered by assembly scan
  with a scoped lifetime; confirm that before building, since a singleton validator capturing a scoped tenant
  context is the same freeze in different clothing.
- the extension (`MaximumCountFrom`) exists so the failure still reports `Code = "max"` and
  `Params = { MaxLength = n }`. A raw `.Must(…)` reports `PredicateValidator` with no operands, and its baked
  message states the wrong number the moment an operator changes the config. **That is why step 1 had to land
  first** — params are the precondition, not a companion.

---

## Advisory validation — shipped as hooks, endpoint deferred

The ask: type-as-you-go feedback that suggests without blocking (a password-strength meter, "this description
looks thin"), running the **same rules** the write path runs.

**FluentValidation already models it.** `.WithSeverity(Severity.Warning)` per rule; `ValidationFailure.Severity`
carries it out. Nothing to invent — only to carry through the SDK's own types, which is what shipped:

- `ValidationSeverity` (`Error` / `Warning` / `Info`) — the SDK's own enum, keeping FV behind the adapter
- `FieldError.Severity`, defaulting to `Error`
- `Validate` / `ValidateAndThrow` filter to `Error`; a warning-only instance is **valid**
- `IValidator<T>.Inspect(T)` returns every failure at every severity and makes no verdict

**Not shipped, deliberately:** the endpoint, the debounce, the model-inference rules. Those are product shape,
and `Inspect` is the whole seam they need.

**On "a different HTTP verb for the same path":** there isn't one. No registered method means "validate this
without doing it", and inventing one breaks caches, proxies, and OpenAPI tooling. The nearest correct thing is a
**sub-resource** — `POST /codes/validate` alongside `POST /codes` — which is a distinct path, cacheable, and
describable. A `?dryRun=true` flag on the write path is the alternative and is worse: it makes one endpoint mean
two things, and a dropped query param performs the write.

**The inference idea fits without changing any of this.** A rule whose predicate calls a small model is still a
rule; mark it `Warning` and it reaches `Inspect` and never blocks a write. The one caveat: the SDK's
`IValidator<T>` is synchronous, so an inference-backed rule needs the async-validation seam that
`conventions/.../validation.md` § *Open* already tracks as deferred. Until then, an advisory endpoint runs the
sync rules and does its inference in the handler beside them.

---

## Open for brainstorm

- what is the tenant source at validate time — `src/Tenancy/` resolver, a claim, or a header? Decides whether
  a validator can stay constructor-injected at all.
- does a bound change need to invalidate anything (cached responses, a client-published config blob), or is
  next-request pickup enough?
- when (4) lands, does the client drop the bound entirely or read it from `foundation/config`? Dropping is free
  (lax drift self-heals); publishing is better UX and one more thing to keep in sync.
