# Icons

*Last updated: 2026-08-19*

> The icon component contract an app satisfies, and the wrapper that gives every glyph its accessibility posture.
> Purpose — one wrapper decides decorative versus semantic, so no call site hand-wires the hidden state.
> Use case — passing an icon into a component, shipping a bespoke glyph, or sizing one.

## The contract

- must accept any component whose props satisfy the adapter shape — a numeric size plus SVG attributes.
- must type the size as a number alone; props are contravariant, and a wider type rejects every real icon.
- must express a CSS-unit size on the class, never on the size prop.
- must render decorative by default — with no label the glyph is hidden from assistive technology.
- must flip to an image role exactly when a label is passed.
- must let a caller-supplied attribute win over the wrapper's own binding.
- must take an icon as a component, never as a name the seam resolves from a registry.
- must leave the icon set to the app — the contract names none.
- must keep a built-in set module-private where one exists; it is not part of the surface.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| `lucide-vue-next` | icon components already typed with a numeric size | the shipped default set |
| a custom component | the adapter shape, hand-written over an SVG | a brand mark, or a glyph the set lacks |
| the spinner | a fixed spinning glyph sized by class | a busy indicator, which is not an app-chosen icon |

---

```txt
✅ <Icon :icon="Check" :size="16" />             decorative, hidden from assistive tech
✅ <Icon :icon="Check" aria-label="Done" />      semantic, given the image role
❌ <Icon :icon="Check" size="1em" />             a CSS unit belongs on the class
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [display](../../constructs/display.md) — the kind a glyph belongs to
- [component catalog](../../constructs/component-catalog.md) — the controls that take an icon prop
- [styling](../../platform/styling.md) — where a class-driven size is decided
