# Primitive

*Last updated: 2026-08-19*

> Behaviour and accessibility with no look of its own — the layer every visual kind is built on.
> Purpose — focus, portalling, dismissal, and roving navigation are solved once, not once per overlay.
> Use case — building a new overlay, menu, listbox, or anything with keyboard semantics.

## Gate

- must carry **no visual styling** beyond the layout it needs to work.
- must be reusable by two or more unrelated kinds, or it belongs to the one component that needs it.
- must merge into its child through `asChild` rather than force a wrapper element into the DOM.
- must not know a domain — a primitive that names a subject is a [display](display.md) or a [control](control.md).

```txt
✅ Slot · Portal · Presence · FocusScope · DismissableLayer · AnchoredPositioner · RovingFocusGroup
❌ ColorArea               (it edits a colour — a domain control)
```

---

## Location

### Group

- must live in `foundation/primitives/`, the layer nothing may import upward from.
- must be re-exported through that folder's barrel, which is the whole primitive surface.

### Folder

- folder and file shape → [constructs](constructs.md) § *Folder*.

```txt
✅ foundation/primitives/focusScope/{FocusScope.vue, index.ts}
❌ presentation/overlays/focusScope/       (behaviour is not presentation)
```

---

## Declaration

### Component doc

#### [Renders](../../lla/notation/documentation/documentation.md)

- must state the behaviour, not the component that uses it.
- must state the SSR posture when the primitive is inert on the server — a portal is.

### Construct

- must drop to a plain `.ts` module when it only computes, rather than render an empty component.
- must expose `asChild` on any primitive that would otherwise add a wrapper element.
- must implement the APG pattern its behaviour has, and cite the pattern in its spec, not in this convention.

### Component name

- must name the behaviour — `FocusScope`, `DismissableLayer` — never the component that consumes it.
- must take no suffix; the behaviour's own word is the whole name — `Slot` · `Portal` · `Presence`.
- must be a [provider](provider.md) instead when what it supplies is a rendering capability for a subtree.

```vue
<script setup lang="ts">
/** Traps and restores focus within its subtree. */
defineOptions({ name: 'FocusScope' });
defineProps<{ loop?: boolean; trapped?: boolean; asChild?: boolean }>();
</script>
```

---

## Content

### Props

#### [The](../../lla/notation/documentation/documentation.md)

- must default every behaviour flag to **off**, so composing a primitive changes nothing until asked.
- must expose an escape hatch on each automatic behaviour — a cancellable event, not a boolean kill switch.

### Slots

- must expose a single `default` slot, merged into the child when `asChild` is set.

### Emits

#### [Fires when](../../lla/notation/documentation/documentation.md)

- must emit a cancellable `CustomEvent` for a behaviour the consumer may need to pre-empt.

```vue
<script setup lang="ts">
defineProps<{ trapped?: boolean }>();                                     // ✅ default off
defineProps<{ onMountAutoFocus?: (e: CustomEvent) => void }>();           // ✅ preventable
defineProps<{ disableAutoFocus?: boolean }>();                            // ❌ a kill switch, not a hook
</script>
```

---

## Composition

- must be composed by every visual kind, and compose nothing but another primitive.
- must not import from `presentation/`, `auth/`, `query/`, or any capability module — the boundary is linted.
- must not be re-exported from the package root as a styled component; it ships as a building block.

```txt
✅ Modal → Portal → FocusScope → DismissableLayer → Presence
❌ FocusScope → Button        (a primitive reaching into presentation)
```

---

## Neighbours

- [overlay](overlay.md) — the kind that composes the most primitives
- [provider](provider.md) — the primitives that install a rendering capability rather than wrap one
- [architecture](../architecture/architecture.md) — the layer boundary a primitive may not import across
- [component catalog](component-catalog.md) — every other kind, and the composition ladder
