# Components

*Last updated: 2026-08-18*

> The things that are complete on their own — declared, and immediately doing their whole job.
> Purpose — a component needs no service, no domain and no collaborator present to mean something.
> Use case — a constants holder, an enum, a settings record, a clock seam.

## The gate [REQUIRED]

- must be **self-sufficient** — declared, and doing its whole job with nothing else present.
- must run the test by demonstration: declare it in a program with nothing else, and use it.
- must fail the gate when it stays inert until a collaborator exists — an `Entity` needs a store, a `Handler` a dispatcher.
- must not read simplicity as self-sufficiency; the test is whether it delivers its contract alone.
- must move to [constructs](../constructs/constructs.md) when it names a role rather than a whole thing.

| Component | Self-sufficient because |
|---|---|
| [constants](constants.md) | the value is readable the moment the class exists |
| [enums](enums.md) | the member names an option, and naming it is the whole contract |
| [extensions](extensions.md) | the method runs on the receiver, with no collaborator to inject |
| [indexers](indexers.md) | the lookup answers from the type's own state |
| [json](json.md) | the seam holds its options and serializes with nothing else present |
| [settings](settings.md) | the record binds and validates without another type existing |
| [time](time.md) | the seam answers the clock question on its own |

---

## Adding a component [REQUIRED]

- must give each component one file, named for the role — `constants.md`, `enums.md`.
- must carry the three `##` sections in order: `Location` · `Declaration` · `Content`.
- must give `Declaration` the sub-heads `### Type doc` · `### Construct` · `### Type name`, skipping any it has no rule for.
- must state the folder **name** only, never its layer ([domain structuring](../architecture/clean/domain-structuring.md)).
- must cite [notation](../../lla/notation/notation.md) rather than restate a default it does not override.
- may close with `## Neighbours` — links out, one line each, carrying no rules.

A component keeps `## Content` because its members **are** its contract; a [construct](../constructs/constructs.md) drops
it, since the shape of a role belongs to the domain that uses it.
