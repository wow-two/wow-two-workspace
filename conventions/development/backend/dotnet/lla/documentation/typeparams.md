# Type params

*Last updated: 2026-08-15*

> The `<typeparam>` block — carried when a substitution can be got wrong, skipped when the name already says it.

## Role decides, not presence (REQUIRED)

A `<typeparam>` says what may be substituted and what role it plays here. A conventional name already says that, so documenting it restates the
name — the Redundant comment anti-pattern ([../documentation.md](../documentation.md) § *Comment anti-patterns*).

- must skip a **conventional** parameter — `T` · `TKey` · `TValue` · `TResult` · `TRequest` · `TResponse`. The name is the convention, and the `where` clause carries the rest.
- must document a **domain-meaningful** parameter — `TAggregate`, `TDiscriminator`, `TUserId`: name the role it plays in this type.
- must not restate the `where` clause — `where TId : notnull, IEquatable<TId>` is in the signature, and a copy goes stale the moment the constraint moves.
- must document **every** parameter once any one of them is documented — a partial set leaves a reader unable to tell an omission from a decision, the same argument [params.md](params.md) § *Every parameter, every time* runs for method parameters.

```csharp
// ✅ the role it plays, not the constraint
/// <typeparam name="TId">The key an entity is addressed by.</typeparam>
public interface IKeyedEntity<out TId> : IEntity;

// ❌ restates the name, then the where clause
/// <typeparam name="TKey">The type of the key.</typeparam>
```

## See also

- [params.md](params.md) — the sibling rule for method parameters
- [summary.md](summary.md) — `<typeparamref>` inside a summary
