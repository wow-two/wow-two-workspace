# Extensions

*Last updated: 2026-08-16*

> The static-logic tier over a domain's types.
> Purpose — keep dependency-free behaviour off the type it extends, without inventing a service for it.
> Use case — reach here for encoding, projection or registration logic that needs no collaborators.

## Location

### Folder
- must live in an `Extensions/` folder beside the domain it extends.

### File
- must give each extensions class its own file, named for the type.

## Declaration

### Type doc
`Extends`, not `Provides`. An extension class hosts methods bolted onto a type it does not own — it supplies no behaviour of its own, so the service starter overstates it.

`Extends <see cref="X"/> for {purpose}.` — the target, then the **purpose category**.

- `Extends <see cref="WifiContentValueObject"/> for payload encoding.`
- **name the purpose, not the additions** — what a class adds changes every time a method lands; why it exists does not
- **cref the target when there are one or two** — the reader clicks through
- **use an abstract name when the targets are many or open** — `Extends the host builder for observability wiring.` A list of crefs stops being readable past two, and an open target set has nothing to cref
- individual extension methods keep a verb start (`Adds`, `Maps`, `Builds`)

### Type name
- must declare `public static class {Domain}Extensions` — named for the vector, never for a single target.
- must not be reached through `using static` ([../notation/naming/naming.md](../notation/naming/naming.md) § *Banned*).

## Content

### Member docs
- must document every method per [../notation/documentation/](../notation/documentation/documentation.md); an extension method starts with its verb.

### Members
- must take no injected collaborators and hold no state.
- may take the receiver as a `this` parameter or as a plain argument.

## See also

- [../notation/documentation/summary.md](../notation/documentation/summary.md) — the starter table
- [../../mla/components/components.md](../../mla/components/components.md) — the suffix keep-list
