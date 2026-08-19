# Components

*Last updated: 2026-08-19*

> Which thing to reach for, and with what values — the application register over the roles `constructs/` defines
> and the surfaces the SDK specs.
> Purpose — the SDK receives a value and applies it; this is where the workspace chooses the value.
> Use case — picking between two shapes that both work, or fixing the value a parameter should carry here.

## The registers [REQUIRED]

| Register | Owns | Lives in |
|---|---|---|
| definition | the role, its declaration, its suffix, its home | [`mla/constructs/`](../constructs/constructs.md) |
| application | which one to reach for, with what values — members, attributes | `mla/components/` — here |
| surface | every prop, slot, emit, option and state one thing exposes | `{Component}.spec.md`, in the SDK repo |

The discriminating pair: the spec says a prop **takes** a timeout; the application register says the preferred
timeout for that operation **is** `N`. The SDK receives and applies; the convention chooses.

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

A kind doc fails the gate — [page](../constructs/visual/page.md) says what a page **is**, so it defines. One
component's prop table fails too — that is its spec's surface. `constants`, `enums` and `extensions` fail on
the third bullet: TypeScript supplies all three, so they are
[lla components](../../lla/components/components.md).

---

## Adding a doc here [REQUIRED]

The three sections, the doc-field rules and the template are [mla](../mla.md) § *Writing a doc in this scope* —
they govern `constructs/` equally, so they are stated once above both.

- must give each role **one file**, named for the role in the plural.
- must name the group folder for its visual group, mirroring `constructs/visual/` one for one.
- must index only the folders in this file's group table, never the components — each group's own lead does that.

---

## The groups

One folder per visual group, mirroring `constructs/visual/`. Each folder's lead indexes its own components; this
table indexes the folders, never the components.

| Group | Components | Construct |
|---|---|---|
| [actions](actions/actions.md) | 15 | [action](../constructs/visual/action.md) |
| [display](display/display.md) | 73 | [display](../constructs/visual/display.md) |
| [feedback](feedback/feedback.md) | 27 | [feedback](../constructs/visual/feedback.md) |
| [forms](forms/forms.md) | 74 | [control](../constructs/visual/control.md) · [field](../constructs/visual/field.md) |
| [layout](layout/layout.md) | 24 | [layout](../constructs/visual/layout.md) |
| [nav](nav/nav.md) | 11 | [nav](../constructs/visual/nav.md) |
| [overlays](overlays/overlays.md) | 8 | [overlay](../constructs/visual/overlay.md) |

---

## Neighbours

- [mla constructs](../constructs/constructs.md) — what each role is, before this register chooses between them
- [lla components](../../lla/components/components.md) — the language forms used end to end, constants onward
- [lla constructs](../../lla/constructs/constructs.md) — the language constructs these kinds are built from
- [notation](../../lla/notation/notation.md) — the defaults a component may override
