# MLA — one app

*Last updated: 2026-08-19*

> Mid-level architecture: every rule that needs an app around it to mean anything.
> Purpose — keep app-shaped decisions out of `lla/`, where they would read as language rules.
> Use case — reach here for a kind you declare, a layer it lives in, how the app builds, or a capability it consumes.

## The boundary

- **`mla/` when the rule reaches one app** — a role you declare, a layer, a Vite target, a data-fetching
  contract.
- **`lla/` when TypeScript, a framework or the browser already supplies the term** — a `type`, a `const` object,
  a doc block, and that form carried end to end in [`lla/components/`](../lla/components/components.md).
- **`hla/` when two of our frontends must agree** — [between our own frontends](../hla/hla.md).

The terms here are **ours**. `Dto`, `Entity`, `Component`, `Page` are aligned to our architecture, not to anything
TypeScript or a framework defines, which is why they land at this level however familiar they read.

---

## The six buckets

| Bucket | Answers | Lead |
|---|---|---|
| `constructs/` | what is this role — one file per role | [constructs](constructs/constructs.md) |
| `components/` | which one to reach for, and with what values | [components](components/components.md) |
| `architecture/` | where it lives — the layers and the slice tree | [architecture](architecture/architecture.md) |
| `platform/` | how the app builds, styles and serves | [styling](platform/styling.md) |
| `domains/` | a capability, its contract and its providers | [domains](domains/domains.md) |
| `frameworks/` | the delta one framework adds | [react](frameworks/react/react.md) · [vue](frameworks/vue/vue.md) |

- **Three registers, one owner each.** `constructs/` defines the role, `components/` chooses between roles and
  fixes values, and one component's own props and slots live in its `{Component}.spec.md` in the SDK repo.
  Registers cut a role in half; `lla` / `mla` / `hla` are the **layers**, and cut by reach.
- **A third party is a member of the domain that consumes it**, never its own axis.
- **The SDK boundary.** *How to use* and *what to use* from `@wow-two-beta/ui` is a convention and lives here; the
  SDK's own internals live in the SDK's docs. The scope follows the component, not the package.

---

## Neighbours

- [lla constructs](../lla/constructs/constructs.md) — the language constructs every kind here is built from
- [lla components](../lla/components/components.md) — those forms used end to end: constants, enums, extensions
- [notation](../lla/notation/notation.md) — the naming and doc defaults a component may override
- [hla](../hla/hla.md) — the scope above, once a second frontend exists
