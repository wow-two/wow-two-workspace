# Components

*Last updated: 2026-08-17*

> A role that owns both its shape and its job with no app around it.
> Purpose — keep the app-free roles out of MLA, where every other role needs a renderer to mean anything.
> Use case — `Constants`, `Enums`, `Extensions`; the rest is [MLA components](../../mla/components/components.md).

## The gate [REQUIRED]

- must place a role here only when it is **self-sufficient** — declared, and immediately doing its whole job alone.
- must place it in [`mla/components/`](../../mla/components/components.md) when it is **inert without a collaborator**.
- must not read simplicity as self-sufficiency — a `Dto` fails, because nothing reads it until a client exists.
- must run the test by demonstration: declare the role in a module with nothing else, and use it.

| Role | Self-sufficient because |
|---|---|
| [Constants](constants.md) | the value is readable the moment the module loads |
| [Enums](enums.md) | the member names an option, and naming it is the whole contract |
| [Extensions](extensions.md) | the function runs on its argument, with no collaborator to inject |

A `Component` fails the gate — it needs a renderer. A `Hook` fails — it needs a component tree. A `Screen` fails —
it needs a router. All three are [MLA components](../../mla/components/components.md).

---

## Adding a component [REQUIRED]

- must give each component **one file**, named for the role in the plural — `constants.md`, `enums.md`.
- must carry the three `##` sections below, in order; a component with nothing to say in one omits it, never renames it.
- must state only the folder **name**, never where it sits ([architecture](../../mla/architecture/architecture.md)).
- may override any [`../notation/`](../notation/notation.md) rule, stating the override in its own file.
- must cite `../notation/` rather than restate a default it does not override.

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

#### [Format](../notation/documentation/documentation.md)
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

#### [Format](../notation/documentation/documentation.md)
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

- [constructs](../constructs/constructs.md) — the constructs these roles are built from
- [notation](../notation/notation.md) — the defaults a component may override
- [MLA components](../../mla/components/components.md) — the roles that need an app around them
