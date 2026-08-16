# Returns

*Last updated: 2026-08-16*

> The `<returns>` block — required on every method that returns a value.

## Required, unless there is nothing to return [REQUIRED]

- must carry `<returns>` on every method whose return type is not `void`, `Task`, or `ValueTask`.
- must exempt exactly those three — a method returning nothing has nothing to describe, and `Task` alone is the absence of a value.
- must carry it on `Task<T>` / `ValueTask<T>` — the `T` is the value, and the wrapper is a mechanism the caller already sees.
- **consistency is the reason**, the same one [params.md](params.md) § *Every parameter, every time* runs: a per-method judgment leaves a reader unable to tell an omission from a decision.

## What it says

- must name **the value**, not the act of returning it — `The stored code, or null when the slug is unknown.`, never `Returns the code.`
- must state the **null / empty case** when one exists — that is the fact a caller most often gets wrong.
- must name the referent, like every other block ([documentation.md](documentation.md) § *Name the referent*).
- must not restate the `<summary>` — if the summary already carries the whole answer, the summary is doing the returns block's job and one of them is redundant.

```csharp
// ✅ the value, and the boundary case
/// <summary>Gets the code addressed by its slug.</summary>
/// <returns>The stored code, or <c>null</c> when the slug is unknown.</returns>

// ❌ restates the act, and hides the null
/// <returns>Returns the code.</returns>
```

## See also

- [params.md](params.md) — the sibling rule for parameters
- [summary.md](summary.md) — the starter table the summary answers to
