# Components

*Last updated: 2026-08-16*

> A role that owns both its shape and its role with no service around it.
> Purpose — keep the service-free roles out of MLA, where every other role needs a layer to mean anything.
> Use case — reach here for `Constants`, `Extensions` and `Enums`; anything else is [`mla/components/`](../../mla/components/components.md).

## The gate [REQUIRED]

- must place a role here only when it is **self-sufficient** — declared, and immediately doing its whole job alone.
- must place it in [`mla/components/`](../../mla/components/components.md) when it is **inert without a collaborator**.
- must not read simplicity as self-sufficiency — an `Entity` is a plain record and still fails, because it cannot be read or written until a store exists.
- must run the test by demonstration: declare the role in a program with nothing else, and use it.

| Role | Self-sufficient because |
|---|---|
| [Constants](constants.md) | the value is readable the moment the class exists |
| [Extensions](extensions.md) | the method runs on the receiver, with no collaborator to inject |
| [Enums](enums.md) | the member names an option, and naming it is the whole contract |

## Adding a component [REQUIRED]

- must give the component **one file**, named for the role in the plural — `constants.md`, `extensions.md`, `enums.md`.
- must carry the three `##` sections below, in order; a component with nothing to say in one omits it, never renames it.
- must state only the folder **name** it wraps itself in; which layer or domain that folder sits in is [`mla/layers/`](../../mla/layers/domain-structuring.md).
- may override any [`../notation/`](../notation/notation.md) rule, stating the override in its own file.
- must cite `../notation/` rather than restate a default it does not override.

| Section | Sub-headings | States |
|---|---|---|
| Location | Folder · File | the folder name that wraps it, and the file's name |
| Declaration | Type doc · Type name | the type's `<summary>`, and the type's own name |
| Content | Member docs · Members | each member's `<summary>`, and the members themselves |

```markdown
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
- {rule}

### Type name
- {rule}

## Content

### Member docs
- {rule}

### Members
- {rule}

## See also

- {link} — {what it owns}
```

## See also

- [../constructs/constructs.md](../constructs/constructs.md) — the constructs these roles are built from
- [../notation/notation.md](../notation/notation.md) — the defaults a component may override
