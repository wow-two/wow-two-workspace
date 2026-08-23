# Language constructs

*Last updated: 2026-08-16*

> Every C# construct we may declare, what each one is for, and the constructs banned outright.
> Purpose — settle the *form* once, so no role doc has to re-argue `record` vs `class`.
> Use case — reach here before declaring a type, and whenever a construct is unfamiliar in this codebase.

## The constructs

Exhaustive through C# 13 / .NET 10. A form we have never written is still listed, with a verdict.

- must read `use` as the default form for its job, and `use with care` as allowed but argued in review.
- must treat `banned` as never declared — the replacement sits in § *Banned constructs*.
- `Data or behavior` names the role the form is fit to carry; `—` means it carries neither.

| Construct | Declares | Data or behavior | Verdict |
|---|---|---|---|
| `class` | a reference type open to inheritance | either | `use with care` |
| `sealed class` | a reference type closed to inheritance | behavior | `use` |
| `abstract class` | a base that cannot be instantiated | either | `use with care` |
| `static class` | a type carrying only static members | either | `use with care` |
| `partial class` | one type split across several files | either | `use with care` |
| `record` | a reference type with value equality | data | `use with care` |
| `record class` | the explicit spelling of `record` | data | `use with care` |
| `sealed record` | a data carrier closed to inheritance | data | `use` |
| `abstract record` | a record base, usually a union root | data | `use with care` |
| `record struct` | a value type with value equality | data | `use with care` |
| `readonly record struct` | a `record struct` no member may mutate | data | `use with care` |
| `struct` | a value type, copied on assignment | data | `use with care` |
| `readonly struct` | a `struct` no member may mutate | data | `use with care` |
| `ref struct` | a `struct` confined to the stack | data | `use with care` |
| `readonly ref struct` | an immutable stack-only `struct` | data | `use with care` |
| `interface` | a contract carrying no state | either | `use` |
| `enum` | a closed set of named integral options | data | `use` |
| generic `delegate` | a named, reusable callback shape | behavior | `use with care` |
| non-generic `delegate` | a callback shape fixed to one signature | behavior | `banned` |
| nested type | a type scoped inside its owner | either | `use with care` |
| anonymous type `new { }` | an unnamed compiler-generated carrier | data | `use with care` |
| type parameter `<T>` | a type the caller supplies | — | `use` |
| `where` constraint | the bound a type argument must satisfy | — | `use` |
| `allows ref struct` | lifts the anti-constraint on a type parameter | — | `use with care` |
| variance `in` · `out` | a type parameter's assignment direction | — | `use with care` |
| file-scoped `namespace` | the namespace of the whole file | — | `use` |
| block `namespace` | a namespace scoped by braces | — | `banned` |
| `file` modifier | a type visible only inside its own file | either | `use with care` |
| top-level statements | an implicit `Program` type and entry point | behavior | `use` |
| field | a value slot on an instance or on the type | data | `use with care` |
| `const` field | a compile-time value inlined at every use | data | `use` |
| `readonly` field | a field assignable only during construction | data | `use` |
| `static readonly` field | a shared field fixed after type init | data | `use` |
| `volatile` field | a field read and written without reordering | data | `use with care` |
| `ref` field | a field holding a reference, `ref struct` only | data | `use with care` |
| `fixed` buffer | an inline array inside an `unsafe` struct | data | `banned` |
| property | a named accessor pair over a value | data | `use` |
| auto-property | a property whose backing field is generated | data | `use` |
| `init` accessor | a setter callable only while constructing | data | `use` |
| `required` member | a member the object initializer must set | data | `use` |
| `field` keyword | the generated backing field, inside an accessor | data | `use with care` |
| indexer `this[…]` | element access on the type itself | data | `use with care` |
| `event` | a multicast subscription point | behavior | `banned` |
| method | a named operation | behavior | `use` |
| local function | a method scoped to one body | behavior | `use with care` |
| `static` local function | a local function that cannot capture | behavior | `use with care` |
| constructor | instance initialization | behavior | `use` |
| initializer `: base` · `: this` | which constructor runs before this one | behavior | `use` |
| primary constructor (class · struct) | constructor parameters in the type header | behavior | `use` |
| primary constructor (record) | positional parameters and their members | data | `banned` |
| static constructor | one-time type initialization | behavior | `use with care` |
| finalizer `~T()` | cleanup the GC runs | behavior | `use with care` |
| operator overload | what an operator means for the type | behavior | `use with care` |
| conversion operator | an `implicit` or `explicit` cast to another type | behavior | `use with care` |
| `operator checked` | the overflow-checking variant of an operator | behavior | `use with care` |
| explicit interface implementation | a member reachable only through the interface | behavior | `use with care` |
| extension method (`this` parameter) | a static method called as an instance one | behavior | `use` |
| `extension` block | extension members grouped by one receiver | behavior | `use with care` |
| partial method | a signature whose body may live in another file | behavior | `use with care` |
| partial property · indexer | a property split the same way | data | `use with care` |
| `abstract` member | a member a derived type must implement | either | `use with care` |
| `virtual` · `override` member | a member a derived type may replace | either | `use with care` |
| `sealed override` | an override no further type may replace | either | `use with care` |
| `new` member | a member hiding the base's same-named one | either | `use with care` |
| default interface member | a body on an interface member | behavior | `use with care` |
| `static abstract` interface member | a static contract a generic can call | either | `use with care` |
| `ref` · `ref readonly` return | a reference to storage instead of a copy | data | `use with care` |
| expression-bodied member `=>` | a member whose body is one expression | either | `use with care` |
| access modifiers | who may reach the declaration | — | `use` |
| `unsafe` member · pointer type | a member permitted to use pointers | — | `banned` |

- must declare a data carrier as a `sealed record` with body properties, never positional (§ *Data components*).
- must declare behavior as a `sealed class` — value equality would be wrong on a type whose identity is what it does.
- must give a `static class` a role that carries no instance state; which roles those are is MLA's to name.
- must have a measured allocation reason before any `struct` form — the default is a reference type.
- must prefer `Func<>` / `Action<>` over a named `delegate` unless the name earns itself.
- must put one `enum` per file; the role and its mapping rules are MLA.
- must let the role pick an `interface` doc starter ([summary](../notation/documentation/summary.md)).
- must clear the six gates in [style](../notation/style/style.md) § *The body* before an expression-bodied member.

---

## Banned constructs

A ban here is about the **construct**, whatever role holds it. A ban that depends on the role lives with that role in
[`mla/constructs/`](../../mla/constructs/constructs.md).

- **`event`** — reach for an `IEvent` on the mediator bus. Four failures, and a service host hits every one:
  - the handler cannot be awaited — it returns `void`, so its exceptions surface unobserved.
  - the lapsed listener — the publisher holds a strong reference, so a subscriber that stays is never collected.
  - the null-invocation race — the last subscriber detaches between check and call, and the call throws.
  - one throwing handler aborts the rest — the first exception stops every later subscriber.
  - an `IEnumerable<IObserver>` set injected by hand is the same shape and folds the same way.
- **positional records for data carriers** — reach for body properties; the accessor pair is the component's.
- **`dynamic`** — reach for generics or polymorphism; the compiler stops checking and the failure moves to runtime.
- **`using static`** — reach for the type name at the call site ([naming](../notation/naming/naming.md) § *Banned*).

---

## Data components

A construct carrying **data** answers what a value *is*. The role fixes the starter, and the shape follows from it.

### Location

#### Folder
- must sit in the folder its component doc names.
  - [components](../../mla/components/components.md) states the folder.
  - [domain structuring](../../../shapes/service/architecture/clean/domain-structuring.md) states which layer it may appear in.

#### File
- must give the type its own file, named for the type: `Channel.cs`, `IEntity.cs`, `ChannelGetAllQuery.cs`.
- must name a generic-only type by its base name — `Repository.cs` for `Repository<T>`.
- may share one file with its non-generic sibling when both sit at the same abstraction level and read as one concept
  with a default-type overload. The non-generic name wins: `IEntity.cs`.
- must keep a `Result`'s nested `Success` / `Failure` in its file — they are inner types.
- must split two unrelated traits, or two siblings whose shapes differ.
- must give a nested type its own file unless the rule above places it.

### Type doc

#### [Summary](../notation/documentation/summary.md)
- must start with **Represents** for a concrete carrier — `record` · `record struct` · `struct`.
- must start with **Defines** for the interface over one.

#### [Typeparams](../notation/documentation/typeparams.md)
- must document a domain-meaningful parameter, and skip a conventional one.

### Type name
- must name the thing carried, never the carrier — `Channel`, not `ChannelData`.

### Member docs

#### [Summary](../notation/documentation/summary.md)
- must start a property with **Gets**, **Gets or sets** or **Sets**, matching its accessors.
- must start a field holding a fixed value with **Holds** — `const`, `static readonly`, `readonly`.
- must start a field keeping changing state with **Keeps** — the verb says the value moves.
- must name the referent unless the value is the type's own ([referents](../notation/documentation/documentation.md)).

```csharp
// ✅ accessor and mutability visible from the first word
/// <summary>Gets the kebab-case slug.</summary>
/// <summary>Holds the compiled pattern an e-mail address must match.</summary>
/// <summary>Keeps the live executions keyed by run id.</summary>

// ❌ Holds on a field whose value moves, so the doc goes stale on the first write
/// <summary>Holds the live executions keyed by run id.</summary>
```

### Members
- must be body properties, never positional parameters.
- must be `required` when the value must come from outside the constructor.
- must be non-nullable unless the absence is a fact the caller reads.
- must leave the accessor pair to the component's own doc — `init` and `set` answer to what writes the value.
- may use `=>` where the component doc grants it ([style](../notation/style/style.md) § *The body*).

### Constructs
- must use `sealed record` for anything whose identity is its values.
- must use `record struct` or `readonly record struct` only for a measured allocation reason.
- may carry behaviour that reads its own values; a flow means it stopped being data.

---

## Behavior components

A construct carrying **behavior** answers what a type *does*. It has no value identity.

### Location

#### Folder
- must sit in the folder its component doc names.
  - [components](../../mla/components/components.md) states the folder.
  - [domain structuring](../../../shapes/service/architecture/clean/domain-structuring.md) states which layer it may appear in.

#### File
- must give the type its own file, named for the type: `CodesController.cs`, `StripeBillingBroker.cs`.
- must name a generic-only type by its base name — `Repository.cs` for `Repository<T>`.
- may share one file with its non-generic sibling when both sit at the same abstraction level and read as one concept
  with a default-type overload. The non-generic name wins: `IEntity.cs`.
- must split two unrelated traits, or two siblings whose shapes differ.
- must give a nested type its own file unless the rule above places it.

### Type doc

#### [Summary](../notation/documentation/summary.md)
- must start with the role's own verb — `Provides` · `Maps` · `Binds` · `Validates`.
- must start with **Defines** for the interface over one.

#### [Remarks](../notation/documentation/remarks.md)
- must carry a directive, a spec reference, or a constraint the signature hides.

### Type name
- must carry the role suffix from the keep-list ([constructs](../../mla/constructs/constructs.md)).

### Member docs

#### [Summary](../notation/documentation/summary.md)
- must start each method with its own verb — `Adds` · `Gets` · `Creates` · `Sends` · `Maps` · `Builds`.
- must start a property with **Gets**, **Gets or sets** or **Sets**, matching its accessors.
- must start a collaborator field with nothing — an injected field carries no doc.
- must start a `Lazy<T>` field with **Holds** — the value is written once, so it does not move.
- must name the deferral on a `Lazy<T>` field — the first read pays a cost the signature hides.

#### [Params](../notation/documentation/params.md)
- must carry a `<param>` for every parameter of a documented method.

#### [Returns](../notation/documentation/returns.md)

```csharp
// ✅ the verb, every parameter, the boundary case
/// <summary>Sends the OTP to the resolved Telegram chat.</summary>
/// <param name="chatId">The chat the code is delivered to.</param>
/// <returns>The delivery outcome, or a failure when the chat is unreachable.</returns>

// ❌ a partial parameter set, which is the failure params.md names
/// <summary>Sends the OTP to the resolved Telegram chat.</summary>

// ✅ Holds, plus the deferral the type signature hides
/// <summary>Holds the compiled route table, built on first read.</summary>
private readonly Lazy<RouteTable> routes;
// ❌ Keeps claims the value moves, and the deferral goes unnamed
/// <summary>Keeps the compiled route table.</summary>
```

### Members
- must take collaborators through the constructor, never a service locator.
- must hold no mutable state unless the role is a `Tracker`.
- must reach for `Lazy<T>` only when the value is expensive and some paths never read it —
  a scoped or singleton lifetime already defers construction to the first resolve.
- must separate member groups with `#region` / `#endregion` once the type passes 60 lines — an IDE folds a
  region and a comment banner is invisible to it.
- may use `=>` where the component doc grants it ([style](../notation/style/style.md) § *The body*).

### Constructs
- must use `sealed class` — a `record` would claim value equality the type does not have.
- must use `static class` only for a `Constants` or `Extensions` role.
- must not use `struct` — a behaviour type copied by value is a bug waiting for a caller.

---

## Neighbours

- [constructs](../../mla/constructs/constructs.md) — the roles these constructs carry
- [statements](statements.md) — the forms that run inside a declaration
