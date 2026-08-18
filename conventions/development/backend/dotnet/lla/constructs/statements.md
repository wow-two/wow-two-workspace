# Statements

*Last updated: 2026-08-16*

> Every C# expression and statement form, and which of them we may write.
> Purpose — settle the body-level vocabulary once, so no component doc has to rule on `stackalloc` or `unsafe`.
> Use case — reach here when a language feature inside a method body is unfamiliar in this codebase.

## What lives here

A **construct** declares a type. A **statement** or **expression** runs inside one. Both are layer 1, so both sit in
this folder; the split is only whether the form produces a declaration or an effect.

---

## The forms

Exhaustive through C# 13 / .NET 10. A form we have never written is still listed, with a verdict.

- must read `use` as the default form for its job, and `use with care` as allowed but argued in review.
- must treat `banned` as never written — `What it does` carries the replacement.
- a declaration form (`operator checked`, `partial`, a local function) is ruled on in [constructs](constructs.md).

| Form | What it does | Verdict |
|---|---|---|
| `if` · `else` | branches on a boolean condition | `use` |
| `switch` statement | branches into one of many sections | `use` |
| `switch` expression | yields a value from the arm that matches | `use` |
| `when` guard | adds a condition to a `switch` arm or `case` | `use` |
| ternary `?:` | yields one of two values from a condition | `use` |
| `foreach` | walks a sequence without an index | `use` |
| `for` | loops with an index the body reads | `use` |
| `while` | loops while a condition holds | `use` |
| `do` · `while` | loops with the test after the body | `use with care` |
| `await foreach` | walks an `IAsyncEnumerable<T>` | `use` |
| `return` | ends the member, with a value or without | `use` |
| `break` | ends the enclosing loop or `switch` section | `use` |
| `continue` | starts the next iteration | `use` |
| `yield return` | emits one element of an iterator | `use with care` |
| `yield break` | ends an iterator | `use with care` |
| `goto` · `goto case` · `goto default` | jumps to a label; the target is invisible scanning down | `banned` |
| label `name:` | names a jump target, reachable only by `goto` | `banned` |
| `try` · `catch` · `finally` | handles a failure the caller cannot prevent | `use` |
| `catch` filter `when` | selects a `catch` without unwinding the stack | `use` |
| `throw` statement | raises an exception | `use` |
| `throw` expression | raises inline, inside `??` or a `switch` arm | `use` |
| rethrow `throw;` | re-raises the caught exception, stack intact | `use` |
| `using` statement | disposes at the end of a nested block | `use with care` |
| `using` declaration | disposes at the end of the enclosing scope | `use` |
| `await using` | disposes an `IAsyncDisposable` | `use` |
| `lock` on a private gate | serializes a region on a `private readonly` object | `use with care` |
| `lock` on `this` or a public field | takes a lock a caller can also take, so a caller can deadlock | `banned` |
| `lock` on a `System.Threading.Lock` | the .NET 9 lock object, checked by the compiler | `use with care` |
| `unsafe` block · pointer types | drops verification for raw memory; use `Span<T>` / `Memory<T>` | `banned` |
| `fixed` | pins storage so a pointer stays valid; needs `unsafe`, itself banned | `banned` |
| `stackalloc` | allocates on the stack; the budget is invisible at the call site | `banned` |
| `checked` · `unchecked`, block or expression | toggles overflow checking; hides the arithmetic decision | `banned` |
| `await` | suspends until the awaited operation completes | `use` |
| `async` lambda | an inline asynchronous callback | `use with care` |
| `is` operator | tests a value against a pattern | `use` |
| declaration pattern `is T t` | tests the type and binds the narrowed value | `use` |
| type pattern `is T` | tests the type without binding | `use` |
| constant pattern | tests equality against a literal or a `const` | `use` |
| null pattern `is null` · `is not null` | tests for null, bypassing an `==` overload | `use` |
| relational pattern `<` `>` `<=` `>=` | tests against a constant bound | `use` |
| logical pattern `and` · `or` · `not` | combines patterns in one expression | `use` |
| property pattern `{ Prop: … }` | tests members of the matched value | `use` |
| positional pattern `(a, b)` | tests through `Deconstruct` or tuple elements | `use with care` |
| `var` pattern | binds without testing, for a `when` guard | `use with care` |
| discard pattern `_` | matches anything and binds nothing | `use` |
| list pattern `[a, b]` | tests a collection's elements and its length | `use with care` |
| slice pattern `..` | matches the remainder inside a list pattern | `use with care` |
| parenthesized pattern | groups patterns against precedence | `use` |
| `as` operator | converts, yielding `null` when it cannot | `use with care` |
| cast `(T)x` | converts, throwing when it cannot | `use with care` |
| LINQ method syntax | composes a query as chained calls | `use` |
| LINQ query syntax `from … select` | the same query as clauses, with `let` · `join` · `group` | `use with care` |
| lambda `=>` | an inline function value | `use` |
| `static` lambda | a lambda the compiler forbids from capturing | `use with care` |
| lambda with explicit return type or defaults | pins the signature inference would pick | `use with care` |
| anonymous method `delegate { }` | the pre-lambda inline function form | `use with care` |
| method group conversion | passes a method by name instead of a lambda | `use` |
| `new` expression | creates an instance of a named type | `use` |
| target-typed `new()` | creates the instance the target type already names | `use` |
| object initializer `{ P = v }` | sets members right after construction | `use` |
| collection initializer `{ a, b }` | fills a collection right after construction | `use with care` |
| collection expression `[a, b]` | builds a collection literal, typed by its target | `use` |
| spread `..e` | inlines a sequence into a collection expression | `use` |
| `with` expression | copies a record, overriding the named members | `use` |
| index `^n` · range `a..b` | addresses from the end, or slices a span or list | `use` |
| `+` `-` `*` `/` `%` | arithmetic; each overloadable as a binary operator | `use with care` |
| unary `+` `-` `!` `~` | sign, logical negation, bitwise complement; overloadable | `use with care` |
| `++` `--` | increment and decrement; overloadable | `use with care` |
| `true` · `false` operators | let a value stand as a condition on its own | `use with care` |
| `&` `\|` `^` | bitwise and logical combination; overloadable | `use with care` |
| `<<` `>>` `>>>` | shifts, unsigned right shift included; overloadable | `use with care` |
| `==` · `!=` | equality; overloadable only as a pair | `use with care` |
| `<` `>` `<=` `>=` | comparison; overloadable only in pairs | `use with care` |
| `&&` · `\|\|` | short-circuits; not overloadable, derived from `&` `\|` `true` `false` | `use` |
| `=` assignment | stores a value; never overloadable | `use` |
| compound assignment `+=` `-=` … | applies the operator, then assigns the result | `use` |
| `??` | yields the right side when the left is null | `use` |
| `??=` | assigns only when the target is null | `use` |
| `?.` · `?[]` | member or element access that stops at null | `use` |
| `!` null-forgiving | asserts non-null to the compiler, unchecked at runtime | `use with care` |
| tuple literal `(a, b)` | groups values without declaring a type | `use with care` |
| deconstruction `var (a, b) = x` | splits one value into named locals | `use` |
| discard `_` | drops a value the code does not need | `use` |
| `nameof` | yields a symbol's name, checked by the compiler | `use` |
| `typeof` | yields the `Type` of a named type | `use` |
| `sizeof` | yields a value type's size in bytes | `use with care` |
| `default` · `default(T)` | yields the type's zero value | `use` |
| `dynamic` | defers binding to runtime; use generics or an interface | `banned` |
| interpolated string `$"…"` | composes text from embedded expressions | `use` |
| raw string literal `"""` | holds text verbatim, quotes and backslashes included | `use` |
| interpolated raw string `$$"""` | raw text with `{{…}}` holes | `use` |
| verbatim string `@"…"` | escapes nothing except a doubled `""` | `use with care` |
| UTF-8 literal `"…"u8` | a `ReadOnlySpan<byte>` of UTF-8 bytes | `use with care` |
| `ref` local · `ref` assignment | aliases existing storage instead of copying it | `use with care` |
| `out` argument · `out var` | returns a second value through a parameter | `use with care` |
| `in` argument | passes a value type by readonly reference | `use with care` |
| `ref readonly` parameter | the same, with the modifier required at the call | `use with care` |
| `scoped` | bounds a reference's lifetime to the current method | `use with care` |
| `params` argument | passes a variable number of arguments | `use` |
| local variable declaration | names a value inside a body | `use` |
| `var` | infers the local's type; spell the type when it is unobvious | `use` |
| local `const` | a compile-time value scoped to the body | `use` |
| block `{ }` | groups statements and scopes their locals | `use` |
| expression statement | evaluates an expression for its effect | `use` |
| empty statement `;` | does nothing | `use with care` |
| `this` · `base` access | reaches the current instance or the base one | `use` |

- must `await` every asynchronous call, without exception ([style](../notation/style/style.md) § *Banned*).
- must use `var` when the initializer names the type, and write the type when it does not
  ([style](../notation/style/style.md) § *`var` — preferred, with one exception*).
- must promote a structural interpolated string to a `const` — interpolation is for a message.
- must gate `lock` behind a `private readonly` object, never `this` and never a public field.

---

## Neighbours

- [constructs](constructs.md) — the forms that declare a type
- [style](../notation/style/style.md) — how the text around these is laid out
