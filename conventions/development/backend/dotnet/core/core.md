# Core

*Last updated: 2026-08-19*

> What holds in every .NET deliverable we build — the language, the roles we define, the things complete on
> their own, and the capabilities a codebase reaches for.
> Purpose — a rule that does not change when the deliverable changes belongs here, once.
> Use case — naming a type, writing a doc comment, picking a role, or reaching for a capability.

## The three scopes

| Scope | Answers | Lead |
|---|---|---|
| [lla](lla/lla.md) | one symbol | the C# form, and how that form is written end to end |
| [mla](mla/mla.md) | one service | the roles we define, the things complete alone, the capabilities |
| [hla](hla/) | between our own services | empty by design until a second service exists |

- must place a rule here when it holds whatever is being built — a service, a library, the SDK, a CLI.
- must place it under [shapes](../shapes/shapes.md) when it changes with the deliverable.
- must not let a shape's vocabulary leak in — `core/` never names a project, a layer, or a host.

---

## Routing a rule

**Routing.** A kind of type you declare → `mla/constructs/{kind}.md`. A thing complete on its own →
`mla/components/`. How any symbol is written → `lla/`. A concrete technology or capability →
`mla/domains/{domain}/`. A rule spanning services we both own → `hla/`.
Where a folder is **created in the project tree**, how a service builds, starts and answers →
[shapes](../shapes/shapes.md), never `core/`.

**The test between `mla/` and `hla/`:** do we own both ends? A third party is adapted in `mla/`, never contracted in `hla/`.
**The three levels, and where each lands.** A C# construct is [constructs](lla/constructs/constructs.md). Everything we
define lands in `mla/`: a **role** that needs something else present → `mla/constructs/` (`Entity`, `Controller`, `Broker`);
a **thing complete alone** → `mla/components/` (`Constants`, `Enums`, `Settings`). A ban follows its rule — construct bans
in `lla/`, role bans with the role.

**The test between baseline and a domain:** would the rule survive if the feature were deleted? Yes → baseline. No → the domain that owns it.

---

## What each scope owns

### `lla/` — one symbol
Every rule that holds for **any** symbol, whatever kind it is: its name, its doc blocks, its member bodies, its file layout,
and the language constructs banned outright. A rule naming a *kind* of type is not `lla/`; a rule naming a technology is not `lla/`.

### `mla/` — one service
Five buckets. `constructs/` = the roles we define, one file per suffix. `components/` = the things complete on their own.
`architecture/` = where it lives, one folder per pattern, testing among the layers. `platform/` = how the service builds,
starts and answers. `domains/` = a concrete technology or use case, one folder each.

- **A component has one home layer.** A kind is declared, stored and documented in one layer even when used from others.
  A `Validator` reading `Options` composes with another component that has its own home; it does not straddle. `Service` is
  the one exception — as the fallback suffix it lands in Application or Infrastructure per instance.
- **A third party is a member of the domain that consumes it**, never its own axis. If the app cannot run without it, it is
  infrastructure, whoever wrote it.
- **The SDK boundary.** *How to use* and *what to use* from our own SDK is a convention and lives here; the SDK's internals
  live in the SDK's own docs.

### `hla/` — between our own services
Named ahead of its contents on purpose: without it, the first gateway or gRPC rule lands in `shapes/service/platform/` and becomes a
single-service default every later service inherits by accident.

---
