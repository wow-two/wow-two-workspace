# Params

*Last updated: 2026-08-15*

> The `<param>` block — one per parameter, always, describing its role in this method's process.

## Every parameter, every time [REQUIRED]

- must document **every** parameter of a documented method. No judgment call, no exceptions — a method's `<param>` set is complete or the doc is wrong.
- **consistency is the reason.** A per-parameter test ("does the name say it?") produces a class where one method documents three parameters and its neighbour documents none, and a reader can no longer tell an omission from a decision.
- **exempt: a constructor whose parameters are all injected collaborators** — a DI primary constructor documents none of them, and carries no `<summary>` either ([documentation](documentation.md) § *Required tags per type-kind*). A constructor taking values documents every parameter, and so does a mixed one — the completeness argument above is exactly what a partial set breaks.
- **`<param>` is exempt from the mandated-comment anti-pattern** ([documentation](documentation.md) § *Comment anti-patterns*), which targets a doc added because a rule demands one. Here the rule demands one, deliberately.

## What each one says

A method is one process. A `<param>` says what the parameter **is to that process**.

- must write a compact noun phrase — no filler, no leading type restatement.
- must not restate the type — the signature carries it.
- must name the referent ([documentation](documentation.md) § *Name the referent*) — `the display name of the code`, never `the display name`.
- must describe the role in **this** method, never in a method this one calls. A downstream flow is the callee's contract, and repeating it here rots when the callee changes.
- should name the constraint the type cannot express — a 1-based index, a required non-empty, which of several meanings applies.

```csharp
// ✅ every parameter, each saying its role here
/// <param name="lines">The document built so far.</param>
/// <param name="prefix">The vCard property prefix to write.</param>
/// <param name="value">The value to escape and append.</param>
private static void AppendProperty(List<string> lines, string prefix, string? value)

// ✅ short names still get their line
/// <param name="id">The code to load.</param>
/// <param name="ct">The cancellation token.</param>
public Task<CodeEntity?> GetByIdAsync(Guid id, CancellationToken ct);

// ❌ restates the type, adds nothing
/// <param name="appliedBy">A string that is the value used for the appliedBy column.</param>

// ✅ says its role in the process
/// <param name="appliedBy">The host stamp recorded on each applied row.</param>
```
