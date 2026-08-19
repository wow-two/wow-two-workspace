# Border

*Last updated: 2026-08-19*

> Every border, radius, ring and outline utility, and the spellings that break the focus recipe.
> Purpose — the ring is the focus indicator for the whole codebase, so its utilities are an accessibility contract.
> Use case — reach here before drawing an edge, rounding a corner or styling a focus state.

## The utilities

`outline-none`, `border`, `ring-2` and `rounded-md` lead the group; `focus-visible:ring-2 ring-ring` is the recipe.

| Utility | Applies | Verdict |
|---|---|---|
| `border` · `border-2` · `border-0` | edge width on all sides | `use` |
| `border-t` · `border-r` · `border-b` · `border-l` | one edge | `use` |
| `border-x` · `border-y` | one axis | `use` |
| `border-solid` · `border-dashed` · `border-dotted` | edge style | `use` |
| `border-{token}` | edge colour ([color](color.md)) | `use` |
| `rounded` · `rounded-sm` … `rounded-3xl` | the corner scale | `use` |
| `rounded-full` · `rounded-none` | a pill or circle, and square corners | `use` |
| `rounded-t-*` · `rounded-l-*` · `rounded-br-*` | one side or one corner | `use` |
| `rounded-[inherit]` | a child matching whatever its parent rounds to | `use with care` |
| `ring` · `ring-1` · `ring-2` · `ring-0` | the focus ring's width | `use` |
| `ring-offset-*` | the gap between element and ring | `use` |
| `ring-inset` | a ring drawn inside the box | `use` |
| `divide-x` · `divide-y` | rules between children, without a border per child | `use` |
| `outline` · `outline-2` · `outline-offset-*` | the outline, for forced-colors and print | `use with care` |
| `outline-none` paired with a `focus-visible:` ring | the native ring replaced, not removed | `use` |
| `outline-none` with no ring replacing it | focus made invisible | `banned` |
| `focus:` ring instead of `focus-visible:` | a ring a mouse click also raises | `banned` |
| an arbitrary width — `border-[0.5px]` | a hairline the scale does not offer | `use with care` |
| an arbitrary radius — `rounded-[2.5rem]` | a corner outside the radius scale | `use with care` |
| `border-x-0 border-y` style resets to fake a divider | a rule assembled from edge overrides | `use with care` |

- must pair `outline-none` with a `focus-visible:ring-2 focus-visible:ring-ring` on the same element.
- must reach for `focus-visible:`, never `focus:` — the ring is for keyboard users.
- must add `ring-offset-*` with `ring-offset-background` wherever the ring would touch the element's own fill.
- must reach for `divide-*` over a border on every child, so the first or last edge needs no reset.
- must take a radius from the scale, which the theme's `--radius-*` tokens define
  ([custom properties](../css/custom-properties.md)).

---

## Banned

- **`outline-none` with no ring replacing it** — reach for the `focus-visible:ring-2` recipe; the element keeps its
  focus stop but shows nothing, so a keyboard user is navigating a page with no cursor.
- **a `focus:` ring instead of `focus-visible:`** — reach for `focus-visible:`; `:focus` fires on mouse click too, so
  every button flashes a ring on press and designers ask for the ring to be removed altogether.
- **a border colour with no token** — reach for `border-border` or `border-input` ([color](color.md)); a literal edge
  stays put when the theme flips, and a dark surface gets a light hairline.

```vue
<!-- ✅ native outline replaced, not removed; ring offset against the page surface -->
<button class="rounded-md border border-input outline-none
               focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
               focus-visible:ring-offset-background">Save</button>

<!-- ❌ focus made invisible — the element still takes focus, and shows nothing -->
<button class="rounded-md border border-input outline-none">Save</button>
```

---

## Neighbours

- [color](color.md) — the tokens these edges and rings take
- [effects](effects.md) — shadow, which reads as an edge at low elevation
- [interactivity](interactivity.md) — the focus-visible variant's other half
- [variants](variants.md) — `focus-visible:`, `peer-focus-visible:`, `group-focus-within:`
