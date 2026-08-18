# Returns

*Last updated: 2026-08-16*

> The `<returns>` block — required on every method that returns a value.

## Scope [REQUIRED]

- must carry `<returns>` on every method whose return type is not `void`, `Task`, or `ValueTask`.
- must exempt exactly those three — `Task` alone is the absence of a value.
- must carry it on `Task<T>` / `ValueTask<T>` — the `T` is the value, the wrapper a visible mechanism.
- **consistency is the reason** ([params](params.md) § *Every parameter, every time*).
  - a per-method judgment leaves a reader unable to tell an omission from a decision.

---

## What it carries

- must name **the value**, not the act of returning it — never `Returns the code.`
- must state the **null / empty case** when one exists — that is the fact a caller most often gets wrong.
- must name the referent, like every other block ([documentation](documentation.md) § *Name the referent*).
- must not restate the `<summary>` — a summary carrying the whole answer makes one of the two redundant.

```csharp
// ✅ the value, and the boundary case
/// <summary>Gets the code addressed by its slug.</summary>
/// <returns>The stored code, or <c>null</c> when the slug is unknown.</returns>

// ❌ restates the act, and hides the null
/// <returns>Returns the code.</returns>
```

---

## Neighbours

- [params](params.md) — the sibling rule for parameters
- [summary](summary.md) — the starter table the summary answers to
