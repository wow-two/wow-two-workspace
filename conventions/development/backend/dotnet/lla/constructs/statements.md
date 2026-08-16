# Statements

*Last updated: 2026-08-16*

> Every C# expression and statement form, and which of them we may write.
> Purpose — settle the body-level vocabulary once, so no component doc has to rule on `stackalloc` or `unsafe`.
> Use case — reach here when a language feature inside a method body is unfamiliar in this codebase.

## What lives here

A **construct** declares a type. A **statement** or **expression** runs inside one. Both are layer 1, so both sit in
this folder; the split is only whether the form produces a declaration or an effect.

## Allowed

| Form | Use it for |
|---|---|
| `if` · `switch` expression / statement | branching; the expression when every arm yields a value |
| `foreach` · `for` · `while` | iteration; `foreach` unless the index is used |
| `using` declaration | scoping a disposable without nesting a block |
| pattern matching · `is` · property patterns | narrowing a type or shape in one expression |
| `try` / `catch` / `finally` | a failure the caller cannot prevent |
| `throw` expression | guarding a null or an invalid argument inline |
| collection expressions `[..]` | building a collection literal |
| range · index `^` `..` | slicing a span or a list |
| `await` · `await foreach` | every asynchronous call, without exception |
| `nameof` | naming a symbol the compiler checks |
| interpolated strings | composing a message; a structural literal becomes a `const` |

## Banned

| Banned | Reach for instead | Why |
|---|---|---|
| `unsafe` · `fixed` · pointers | `Span<T>` · `Memory<T>` | the safety traded away is never repaid |
| `stackalloc` | `Span<T>` over a pooled buffer | the stack budget is invisible at the call site |
| `checked` · `unchecked` | a type that cannot overflow, or a guard | the block hides the arithmetic decision |
| `goto` | a loop, a method, or an early `return` | the target is invisible when scanning downward |
| `dynamic` | generics or polymorphism | the compiler stops checking, and the failure moves to runtime |
| `lock` on `this` or a public field | a `private readonly object` gate | a caller can take the lock and deadlock |
| a non-generic `delegate` | `Func<>` · `Action<>` · `Predicate<>`, or a generic one | the signature cannot be reused |

## See also

- [constructs.md](constructs.md) — the forms that declare a type
- [../notation/style/style.md](../notation/style/style.md) — how the text around these is laid out
