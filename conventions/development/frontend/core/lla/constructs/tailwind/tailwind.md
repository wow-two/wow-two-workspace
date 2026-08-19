# Tailwind v4

*Last updated: 2026-08-19*

> Every Tailwind utility group, the verdict on each, and the authoring at-rules that extend the framework.
> Purpose — Tailwind is the only styling layer here, so a group's verdict *is* the styling rule for that property.
> Use case — reach here before writing a class family this codebase has not written before.

## The groups

Counted across the Vue SDK and `smart-qr`.

| Group | In use | Verdict | Doc |
|---|---|---|---|
| color | 1657 | `use` — semantic tokens only | [color](color.md) |
| border | 1318 | `use` | [border](border.md) |
| flexbox | 1205 | `use` — the default layout tool | [flexbox](flexbox.md) |
| sizing | 729 | `use` | [sizing](sizing.md) |
| typography | 721 | `use` | [typography](typography.md) |
| position | 644 | `use` | [position](position.md) |
| spacing | 622 | `use` | [spacing](spacing.md) |
| display | 588 | `use` | [display](display.md) |
| transitions | 266 | `use` — via motion tokens | [transitions](transitions.md) |
| effects | 168 | `use` | [effects](effects.md) |
| transforms | 140 | `use` | [transforms](transforms.md) |
| interactivity | 132 | `use` | [interactivity](interactivity.md) |
| overflow | 79 | `use` | [overflow](overflow.md) |
| grid | 79 | `use` — two-dimensional layout only | [grid](grid.md) |
| z-index | 35 | `use` — semantic tiers only | [z-index](z-index.md) |
| filters | 26 | `use with care` | [filters](filters.md) |
| accessibility | 7 | `use` | [accessibility](accessibility.md) |
| box | 4 | `use` | [box](box.md) |
| tables | 3 | `use` | [tables](tables.md) |
| variants | 1300+ | `use` | [variants](variants.md) |
| authoring | 5 | see the doc | [authoring](authoring.md) |

---

## The rules every group inherits

- must compose classes through `cn()`, never a template literal — `tailwind-merge` resolves a consumer's override
  ([styling](../../../../shapes/app/platform/styling.md)).
- must reach for a scale step before an arbitrary value; an arbitrary value earns itself only where no step exists.
- must write the scale name, never the raw measurement — `gap-2`, not `gap-[0.5rem]`.

---

## Banned

- **the `!` important modifier**, in the v3 prefix (`!px-0`) or the v4 suffix (`px-0!`) spelling — reach for `cn()`
  ordering or a variant. `tailwind-merge` cannot resolve an important class, so it beats every later override; the v3
  prefix form is not a valid v4 utility at all, so it emits nothing.
- **`@apply`** — reach for a `tailwind-variants` recipe or a component. It moves classes out of the markup, where
  `tailwind-merge` can no longer see them, so the box stops being overridable.
- **a template-literal class string carrying a condition** — reach for `cn()`; concatenation appends both sides of a
  conflict and the later one wins by source order rather than by specificity.
- **a raw palette class** (`bg-slate-900`, `text-zinc-500`) — reach for the semantic token ([color](color.md)).

---

## Open

- `SpeedDialTrigger.vue:68` carries `!bottom-auto` and four siblings in the v3 prefix spelling; verify they emit nothing
  under v4.1 and replace them with a positional variant.

---

## Neighbours

- [css](../css/css.md) — the four jobs left to raw CSS
- [styling](../../../../shapes/app/platform/styling.md) — wiring, `cn()`, dark mode
