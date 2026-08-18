# Imports

*Last updated: 2026-07-06*

> How to order and write `import` statements in a `.ts` / `.tsx` file — group order, intra-group sort, and `type`-import form.
> Purpose — one deterministic layout so any file's head reads the same and diffs stay minimal. Sits with [naming](../naming/naming.md) / [documentation](../documentation/documentation.md) / [enums](../../components/enums.md) in `code-style/`.

**Order:** `side-effect → third-party → SDK → @/ alias → relative`

---

## 1. Groups

- must order groups by **distance from the runtime**, outermost first, in this fixed sequence:

| # | Group | Matches | Example specifier |
|---|---|---|---|
| 1 | Side-effect | bare `import "…"`, no bindings | `"@fontsource-variable/geist"` · `"./index.css"` |
| 2 | Third-party | any bare specifier not `@wow-two-beta/*` | `react` · `react-router-dom` · `lucide-react` · `@react-oauth/google` |
| 3 | SDK | `@wow-two-beta/ui/*` subpaths | `@wow-two-beta/ui/presentation/actions` |
| 4 | `@/` alias | app-internal absolute (`@/domain` · `@/integration` · `@/presentation`) | `@/domain/codes/core` |
| 5 | Relative | `../` then `./` | `./gradient` |

- must separate every non-empty group with **exactly one blank line**; must not blank-line **within** a group.
- must drop an empty group with **no** leftover blank line — adjacent groups touch.
- in a **multi-package** repo (pnpm workspace, `@{brand}/*` packages), group 4 splits: sibling `@{brand}/*` packages sort **before** the `@/` app alias — same slot order, packages are more distant than app code.

```typescript
// ✅ five groups, one blank line each
import "@fontsource-variable/geist";

import { useEffect, useState } from "react";
import { ArrowRight } from "lucide-react";

import { Button } from "@wow-two-beta/ui/presentation/actions";
import { Stack } from "@wow-two-beta/ui/presentation/layout";

import { UserKind, type Me } from "@/domain/identity";
import { getMe } from "@/integration/identity";

import { AppLayout } from "./AppLayout";
```

---

## 2. Intra-group order

- must sort every group **alphabetically by module specifier** (the string after `from`), case-insensitive.
- side-effect (group 1): must keep global-effect imports (fonts, polyfills) **before** local `./*.css` — load order is semantic, not alphabetical; this is the one group where source order overrides sort.
- third-party (group 2): must place `react` and `react-dom` **first** (framework before ecosystem), then the rest alphabetically.
- `@/` alias (group 4): must sort by **layer** first — `domain` → `integration` → `presentation` (inward-out, mirrors the [layer model](../../../mla/architecture/architecture.md)) — then alphabetically by full path within a layer.
- relative (group 5): must place `../` (parent) **before** `./` (sibling); deeper `../../` before shallower `../`; alphabetical within an equal depth.
- **tie-break** (same specifier prefix): a `type`-only statement sorts **after** a value statement from the same module; otherwise the raw specifier string decides.

---

## 3. Type imports

- must inline the `type` modifier on the **binding** — `import { X, type Y } from "…"` — when a statement pulls **both** values and types from one module; keeps one statement per module, no parallel `import type` twin.
- must use a standalone `import type { … }` **only** when the **entire** statement is type-only (no value binding).
- must not add `import type` for a module already imported for a value — fold the type into the existing statement as `type Y`.

```typescript
import { UserKind, type Me } from "@/domain/identity";   // ✅ mixed → inline `type`
import type { CodeDto } from "@/domain/codes/core";       // ✅ all-type → standalone
import { Gradient } from "@/domain/codes/core";
import type { Gradient } from "@/domain/codes/core";      // ❌ split — fold into the value import
```

---

## 4. Rules

- must import React bindings by **name**, never a default namespace — `import { useState, type ReactNode } from "react"`; no `import React from "react"`, no `React.*` UMD reference ([style](style.md#react-types--import-named-never-the-umd-namespace)).
- must import the SDK through its **published subpath** (`@wow-two-beta/ui/presentation/forms`), never a deep internal path into the package's `src` / `dist`.
- must reach app-internal code through the **`@/` alias**, never a climbing relative (`../../../domain/...`); a relative path is for **same-slice siblings** only (`./gradient`, `./components`).
- must alias a name collision at the **import**, suffixing the SDK side — `import { Section as UiSection } from "@wow-two-beta/ui/presentation/layout"` — so the local symbol keeps the bare name.
- must keep all imports in the **head** of the file — no mid-file `import`; a lazy `import()` for code-splitting is the sole exception.
