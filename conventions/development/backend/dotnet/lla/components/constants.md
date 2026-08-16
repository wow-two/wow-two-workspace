# Constants

*Last updated: 2026-08-16*

> A static class holding values the codebase names once.
> Purpose — one home for a value's authority, so a literal never has to be explained twice.
> Use case — reach here when a value is fixed by a spec, a wire format, or a third-party contract.

## Location

### Folder
- must live in a `Constants/` folder beside the code that owns the values.

### File
- must give each constants class its own file, named for the type.

## Declaration

### Type doc
- must open the `<summary>` with **Contains** — `Contains the canonical kebab-case slugs for every channel.`

### Type name
- must declare `public static class {Name}Constants`, or `{Name}` when the noun already reads as a set (`ChannelSlugs`).

## Content

### Member docs
`Holds` — a member-sized verb, matching how properties take `Gets`. **Not `Defines` / `Represents`**: those are type-kind starters, and a `const` is a member. It has no accessor either, so no `Gets`.

- **must not restate the value** — `= "WPA"` is on the line; `Represents the WPA token` says nothing the reader can't see
- **must name the authority that fixes the value** when one exists — a spec, a wire format, a third-party contract. That is the fact the literal alone hides: `"nopass"` is unguessable until you know the WIFI URI scheme mandates it
- **applies at every visibility** — a `private const` carries a summary too; only `<inheritdoc/>`, test methods, and generated code are exempt ([documentation.md](../notation/documentation/documentation.md) § *Required tags per type-kind*)
- **a format-string constant must document its shape, never its slots** — `Holds the payload shape of a WIFI URI.` The `{0}`…`{n}` are visible; what a reader needs is which spec the shape comes from
- **a constant naming a magic number states where the number comes from** — `private const int MaxNameLength = 200;` gets `Holds the column width the schema fixes.`, never `Holds the max name length`

### Members
- must use `const` where the value is compile-time, `static readonly` where it is not.
- must group related values with a blank line between groups, no dividers.

## See also

- [../notation/documentation/summary.md](../notation/documentation/summary.md) — the starter table
- [../notation/style/style.md](../notation/style/style.md) — lifting a structured literal into a named `const`
