# Provider

*Last updated: 2026-08-19*

> A component that installs one capability for its subtree and renders nothing but its slot.
> Purpose — a capability crosses the tree without prop drilling, and the wiring lives in one named file.
> Use case — auth, query client, feature flags, locale, colour mode, direction, scroll lock.

## Gate

- must render **only `<slot />`** — a wrapper that adds markup is a [layout](layout.md).
- must supply exactly one capability; two capabilities are two providers, composed by the caller.
- must be installable at any depth, so a subtree can override what an ancestor provided.
- must not be the capability — the seam it installs is a `.ts` contract
  ([headless suffixes](../behavior/headless-suffixes.md)).

```txt
✅ AuthProvider · QueryProvider · FlagsProvider · LocaleProvider · ColorModeProvider · DirectionProvider
❌ AppShell               (it renders the frame as well as providing it — a layout)
```

---

## Location

### Group

- must live in its capability module — `auth/`, `query/`, `flags/`, `router/` — not in `presentation/`.
- must live in `foundation/primitives/` when the capability is a rendering concern, not a domain one.

### Folder

- must sit beside the context and the seam it installs, so one folder holds the whole capability.

```txt
✅ src/auth/{AuthProvider.vue, AuthContext.ts, AuthStrategy.ts, index.ts}
❌ src/presentation/layout/authProvider/     (a capability is not presentation)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name what the subtree gains, not how the value is computed.

### Construct

- must `provide()` one key, and expose a `use{Capability}()` composable as the only way to read it.
- must make that composable fail loudly when no provider is above it.
- must read a swappable seam live on each call, so replacing it takes effect without a remount.

### Component name

- must end `*Provider`, and name the context it supplies `*Context` — one capability, one pair.
- must name the capability, never the implementation — `AuthProvider`, not `CookieAuthProvider`.

```vue
<script setup lang="ts">
/** Renders its children with an auth session available to the subtree. */
defineOptions({ name: 'AuthProvider' });
</script>

<template><slot /></template>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take the seam it installs as a prop — the strategy, the client, the flag source.
- must take the initial value as a separate prop, so a test or an SSR pass can seed it.

### Slots

- must declare a single `default` slot and render it unwrapped.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit only capability lifecycle events a host must react to — a session expiring, a client reconnecting.

```vue
<script setup lang="ts">
defineProps<{ strategy: AuthStrategy; bridge?: AuthBridge }>();   // ✅ the seam comes in
defineSlots<{ default(): unknown }>();                            // ✅
defineProps<{ class?: string }>();                                // ❌ nothing is rendered to style
</script>
```

---

## Composition

- must be mounted in `bootstrap/` for an app-wide capability, and inline for a scoped override.
- must compose nothing — it wraps, it does not build.
- must nest rather than merge: two capabilities are two providers, not one with two seams.

```txt
✅ App → QueryProvider → AuthProvider → RouterView
❌ AppProvider(auth + query + flags)      (one component, three capabilities)
```

---

## Neighbours

- [headless suffixes](../behavior/headless-suffixes.md) — the `.ts` seam vocabulary a provider installs
- [primitive](primitive.md) — the rendering-level providers that ship in `foundation/primitives/`
- [hooks](../behavior/hooks.md) — the `use{Capability}()` composable a provider is read through
- [visual kinds](visual.md) — every other kind, and the composition ladder
