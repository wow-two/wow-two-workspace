# Styling

*Last updated: 2026-08-19*

**Tailwind v4 (CSS-first)** utility classes only. No CSS modules, no styled-components, no per-component `.css`.

## Tailwind v4 wiring (`index.css`)

A consuming app's `src/index.css` imports Tailwind, imports the beta-UI design tokens, and `@source`s the beta-UI
compiled output so the utility classes its components emit are generated (Tailwind v4 ignores `node_modules` by
default):

```css
@import 'tailwindcss';

/* Design tokens (@theme) shipped by the library — gives bg-primary, text-foreground,
   bg-card, border-border, etc. */
@import '@wow-two-beta/ui/styles.css';

/* Tailwind v4 ignores node_modules; point it at the beta UI's dist so its utility
   classes are generated. Path is relative to THIS file. */
@source '../../node_modules/@wow-two-beta/ui/dist';
```

The Vite plugin is `@tailwindcss/vite` (in `plugins: [react(), tailwindcss()]`). No `tailwind.config.js` content
array — `@source` declarations live in CSS.

- **`@source` is relative to `index.css`.** `index.css` lives in `bootstrap/`
  ([architecture](../architecture/architecture.md)), so the lib path is `../../node_modules/...` — two up,
  `bootstrap/` → `src/` → repo root. A wrong depth **silently drops** the lib's utility classes: the app renders
  half-styled with no build error.

---

## Design tokens

- Consume the **semantic token classes** the beta UI ships via `@theme` — `bg-background`, `text-foreground`,
  `bg-card`, `border-border`, `bg-primary`, etc. — instead of raw palette values (`bg-slate-900`).
- A repo that needs its own brand tokens extends them in its `@theme` block. **Default theme works out of the box** —
  override only the keys you must.

---

## Conditional classes — `cn()`

- Merge/conditional classes via **`cn()`** (clsx + tailwind-merge). Cross-app it lives in `@{brand}/common/lib`;
  the beta UI exposes its own.
- Never build class strings with template-literal concatenation when conditions are involved.

---

## Variants — `tailwind-variants`

Components with multiple visual states define their class map with **`tailwind-variants`** in a co-located
`*.variants.ts` / `*Styles.ts` file ([naming](../../lla/notation/naming/naming.md)) — keep large variant maps out of
the JSX.

---

## Dark mode

- Class-based dark mode via the `dark:` variant, toggled on `document.documentElement`.
- Drive it through the shared theme hook (`useTheme`), not ad-hoc `localStorage` reads in components.

---

## Neighbours

- [constructs](../constructs/constructs.md) — variants, props
- [architecture](../architecture/architecture.md) — where `index.css` lives (the `bootstrap/` layer)
