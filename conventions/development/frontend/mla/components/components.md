# Components

*Last updated: 2026-08-19*

> Which thing to reach for, and with what values — the judgement register over the roles `constructs/` defines
> and the surfaces the SDK specs.
> Purpose — the SDK receives a value and applies it; this is where the workspace chooses the value.
> Use case — picking between two shapes that both work, or fixing the value a parameter should carry here.

## The three registers [REQUIRED]

| Register | Owns | Lives in |
|---|---|---|
| definition | what the role is, its suffix, its contract shape | [`mla/constructs/`](../constructs/constructs.md) |
| judgement | which one to reach for, and with what values | `mla/components/` — here |
| surface | every prop, slot, emit and state one component exposes | `{Component}.spec.md`, in the SDK repo |

The discriminating pair: the spec says a prop **takes** a timeout; this register says the preferred timeout for
that operation **is** `N`. The SDK receives and applies; the convention chooses.

`lla` / `mla` / `hla` name the **layers** — how far a rule reaches. A register is a different cut: which half of
one role a doc owns.

---

## The gate [REQUIRED]

- must place a doc here only when it says **which thing to reach for, and with what values**.
- must place it in [`mla/constructs/`](../constructs/constructs.md) when it says **what the thing is** — the role,
  the suffix it takes, the shape of its contract.
- must place it in [`lla/components/`](../../lla/components/components.md) when the thing is a **language form**
  used end to end — a `const` binding, a `const` object value set, a static-helper object.
- must leave one component's props, slots, emits and states to its `{Component}.spec.md` in the SDK repo.
- must not enumerate a parameter here, and must not fix a preferred value in a spec — one half each.
- must not read self-sufficiency or simplicity as the test — every component has a caller, and that sorts nothing.

A kind doc fails the gate — [page](../constructs/page.md) says what a page **is**, so it defines. One component's
prop table fails too — that is its spec's surface. `constants`, `enums` and `extensions` fail on the third bullet:
TypeScript supplies all three, so they are [lla components](../../lla/components/components.md).

---

## Adding a component [REQUIRED]

- must give each component **one file**, named for the role in the plural — the shape
  [`lla/components/`](../../lla/components/components.md) uses for `constants.md` and `enums.md`.
- must carry the three `##` sections below, in order; a component with nothing to say in one omits it, never renames it.
- must state only the folder **name**, never where it sits ([architecture](../architecture/architecture.md)).
- may override any [`lla/notation/`](../../lla/notation/notation.md) rule, stating the override in its own file.

| Section | Sub-headings | States |
|---|---|---|
| Location | Folder · File | the folder name that wraps it, and the file's name |
| Declaration | Type doc · Type name | the type's doc fields, and the type's own name |
| Content | Member docs · Members | each member's doc fields, and the members themselves |

- must give each doc field its own `####` sub-heading, linked to the doc that owns that field.
- must not sub-head a field the component does not declare.
- must write each rule as what the code **must have** — a banned shape goes in the ❌ example, not a rule.
- must close every doc sub-heading and `Members` with one ✅ / ❌ pair; the ❌ must fail a rule stated above.
- must state a constraint as its own rule only when no positive rule already excludes it.
- must state a member **order** rule in `Members` — a reader cannot predict an order the doc never fixes.

````markdown
# {Components}

*Last updated: {YYYY-MM-DD}*

> {One line saying what the role is.}
> Purpose — {what having it buys}.
> Use case — {when to reach for it}.

## Location

### Folder
- {rule}

### File
- {rule}

## Declaration

### Type doc

#### [Format](../../lla/notation/documentation/documentation.md)
- must {rule}

```typescript
// ✅
{good}
// ❌ {why it fails}
{bad}
```

### Type name
- must {rule}

## Content

### Member docs

#### [Format](../../lla/notation/documentation/documentation.md)
- must {rule}

### Members
- must {rule}

```typescript
// ✅
{good}
// ❌ {why it fails}
{bad}
```

## Neighbours

- {link} — {what it owns}
````

---

## Neighbours

- [mla constructs](../constructs/constructs.md) — what each role is, before this register chooses between them
- [lla components](../../lla/components/components.md) — the language forms used end to end, constants onward
- [lla constructs](../../lla/constructs/constructs.md) — the language constructs these kinds are built from
- [notation](../../lla/notation/notation.md) — the defaults a component may override
