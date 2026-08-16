# Members & bodies

*Last updated: 2026-08-15*

> What — the most-abstract class/struct member-body conventions: how a member's body is written, regardless of layer.
> Purpose — keep every body debuggable — intermediates you can save, lines you can breakpoint.
> Use case — reach for it whenever you write a method, accessor, or property body and have to choose block `{ }` vs expression `=>`.

## Bodies

- **must use a block body `{ }` for any member carrying logic** — so you can save intermediates to locals + breakpoint any line (a one-liner has to be rewritten to debug)
- **may use `=>` for a trivial pure getter** — a property/accessor that just returns a field or a constant, with no logic: `public string Name => _name;`
- **may use `=>` for a trivial delegation or a direct return, but only on a primitive component** — see below

### `=>` is decided by the component, not the member

A member that fits on one line today may not tomorrow. Whether that matters depends on **which component owns it**, so the carve-out is granted per component kind, not per member.

| May use `=>` | Why |
|---|---|
| value object · entity · DTO · request / response model | data carriers; a member here delegates or returns, and that does not grow |
| `Extensions` | dependency-free behaviour by definition — no collaborators to accumulate |
| `Mapper` | one transform, in → out; growth means it stopped being a `Mapper` |
| `Constants` · `Registry` | hold values or bindings, not logic |
| `Validator` | a declarative rule chain, not a flow — `public XValidator() => RuleFor(…);` |

| Must use `{ }` always | Why |
|---|---|
| `Service` · `Broker` · `Client` · `Repository` | their logic grows by design — a guard, a retry, a log line all arrive later |
| `Handler` | orchestrates a use case; every one gains steps |
| `Controller` | binds, dispatches, maps a result — three operations minimum |

- the rule is **from the start**, not on the first growth. A `Service` written as a one-liner today gets a block body today, so the diff that adds its second line is one line, not a reshape.

**Five gates, in order. The first `no` blocks the expression body.**

1. **Does this type already have a block-bodied member?** Yes → block body. One file does not mix the two forms; the first block sets the shape for the rest.
   - **adding a block body reverts the file.** The moment one member here needs `{ }`, every `=>` in the type converts with it, in the same change. The mix is what this gate exists to prevent, so the fix travels with its cause rather than waiting for a cleanup pass.
2. **Is this component permitted `=>` at all?** No → block body. The two columns above decide it, before the member is even read.
3. **Is the member a single call forwarding its parameters, or a direct member return?** No → block body. A rule chain, a build, or a construction is a body.
4. **Does it fit on one line with the signature, under 120?** No → block body. Needing a wrap is the tell, and avoiding that wrap is the only thing `=>` buys.
5. **Is it free of branches, chains, `await`, and `match`?** No → block body.

```csharp
// ✅ passes all five — a value object, no block members, one forwarding call, fits
public override string Encode() => this.ToPayload();
```
- **Any logic → block body** — a branch, a call chain, a computation, an `await`, a `match`: write it as `{ … }` even if it currently fits on one line.
- **blank lines separate operations, not closely-related lines** — keep one operation's lines together (no blank within); a blank only *between* operations. e.g. an action body: guard → ⎵ → map-request + send + store-result → ⎵ → return.

```csharp
// ✅ trivial pure getter — expression body fine
public string Slug => _slug;

// ✅ method with logic — block body, intermediates breakpointable
public async Task<IActionResult> Get(CancellationToken ct)
{
    var result = await sender.SendAsync(new GetProductsQuery(), ct);

    return result.Match<IActionResult>(...);
}

// ❌ method as expression body — can't breakpoint or inspect the result
public async Task<IActionResult> Get(CancellationToken ct) =>
    (await sender.SendAsync(new GetProductsQuery(), ct)).Match<IActionResult>(...);
```

## See also

- [code-organization.md](../style/style.md) — one file per type, dividers, parameter + raw-string formatting
- [controllers.md](../../../mla/components/behavior/controller.md) — applies this rule to controller actions (block body, save the dispatch result)
- [models.md](../../constructs/records.md) — record style + property rules
- [request-models.md](../../../mla/components/data/request-model.md) — applies it to the `ToCommand` mapping method
