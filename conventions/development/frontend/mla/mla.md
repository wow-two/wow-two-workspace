# MLA — one app

*Last updated: 2026-08-17*

> Mid-level architecture: every rule that needs an app around it to mean anything.
> Purpose — keep app-shaped decisions out of `lla/`, where they would read as language rules.
> Use case — reach here for a kind you declare, a layer it lives in, how the app builds, or a capability it consumes.

## The boundary

- **`mla/` when the rule needs an app** — a `Component`, a layer, a Vite target, a data-fetching contract.
- **`lla/` when TypeScript already supplies the term** — a `type`, a `const` object, a doc block.
- **`hla/` when two of our frontends must agree** — [between our own frontends](../hla/hla.md).

The terms here are **ours**. `Dto`, `Entity`, `Component`, `Screen` are aligned to our architecture, not to anything
TypeScript or a framework defines, which is why they land at this level however familiar they read.

---

## The four buckets

| Bucket | Answers | Lead |
|---|---|---|
| `components/` | what am I building — one file per kind | [components](components/components.md) |
| `architecture/` | where it lives — the layers and the slice tree | [architecture](architecture/architecture.md) |
| `platform/` | how the app builds, styles and serves | [styling](platform/styling.md) |
| `domains/` | a capability, its contract and its providers | [domains](domains/domains.md) |

- **A component has one home layer.** A kind is declared and documented in one layer even when used from others.
- **A third party is a member of the domain that consumes it**, never its own axis.
- **The SDK boundary.** *How to use* and *what to use* from `@wow-two-beta/ui` is a convention and lives here; the
  SDK's own internals live in the SDK's docs. The scope follows the component, not the package.

---

## Neighbours

- [constructs](../lla/constructs/constructs.md) — the language constructs every kind here is built from
- [notation](../lla/notation/notation.md) — the naming and doc defaults a component may override
- [hla](../hla/hla.md) — the scope above, once a second frontend exists
