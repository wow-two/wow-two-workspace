# Code organization

*Last updated: 2026-07-06*

The TS counterpart of [../backend/code-organization.md](../../backend/code-style/code-organization.md). File-per-type and one-component-per-folder live in [naming.md](naming.md) / [components.md](../presentation/components.md); this file covers in-file layout.

## Language baseline

- **No `var`** — `const` by default, `let` only when reassigning. Applies to `.ts`, `.tsx`, inline `<script>`.
- TypeScript **strict** mode on.

## Section dividers

- **`// ── Section ──`** for field groups inside interfaces or large objects.
- **Plain comments** for logical sections inside JSX — no dashes/decorators.
- **Don't over-divide** — 2-3 fields don't need a divider.

```typescript
// ✅ lightweight label for field groups
export interface Listing {
  // ── Meta ──
  id: string;
  isValid: boolean;

  // ── Property ──
  propertyType: PropertyType | null;
}

// ✅ plain comment sections in JSX
{/* Image carousel */}
<div>...</div>

// ❌ dashed decorators
{/* ---- Image carousel ---- */}
// ---- Helpers ----
```

## Import order

Group order, intra-group sort, and `type`-import form live in [imports.md](imports.md) — `side-effect → third-party → SDK → @/ alias → relative`, blank-line-separated. React-named-imports rule is below.

## React types — import named, never the UMD namespace

- must import React types by name and reference them bare — `import { type ReactNode } from "react"` → `ReactNode`.
- must not reference the `React.*` UMD global (`React.ReactNode`, `React.JSX.Element`, `React.MouseEvent`): with `jsx: "react-jsx"` there is no `React` value in scope, so `React.*` triggers TS `ts(2686)` ("refers to a UMD global").
- `React.JSX.Element` → `ReactElement`; or `JSX.Element` via `import { type JSX } from "react"`.

## File-internal order

Components: imports → types → constants → helpers → component → sub-components (see [components.md](../presentation/components.md)). Non-component modules: imports → types → constants → exported members.

## See also

- [naming.md](naming.md) · [components.md](../presentation/components.md)
- [../backend/code-organization.md](../../backend/code-style/code-organization.md) — the C# sibling
