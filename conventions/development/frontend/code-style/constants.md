# Constants

*Last updated: 2026-07-05*

A single fixed value, or an unrelated group of them. Distinct from an [enum](enums.md) — a closed value **set** a field ranges over.

## Const vs enum

- a single scalar, or unrelated values → a **`const`** (this file).
- a fixed **set** of related string values (a closed vocabulary) → an **enum** ([enums](enums.md)).

## Declaration

- must name a module-level constant **PascalCase** — `PresetIconSize`, `DefaultGradientEnd` — the same casing as enums / value-sets; a data/scalar const is that same category, not a separate `UPPER_SNAKE` one. Existing `UPPER_SNAKE` migrates gradually; new code is PascalCase.
- must freeze an object / array / tuple constant with `as const`.
- must co-locate constants with the module that owns them (`design/gradient.ts`); use a dedicated `Constants.ts` file only for a slice-wide set.
- prefer a named factory over an inlined literal for a repeated shape — `makeDefaultGradient(fg)`, not a hand-built object at each call site.

```typescript
/** Preset-icon glyph size (px). */
export const PresetIconSize = 16;

/** Linear-gradient direction presets — angle (deg) + arrow. */
export const Angles = [/* … */] as const;
```

## Comments

- must JSDoc every exported constant with a one-liner `/** … */` ([documentation](documentation.md)); include units / range when not obvious — `(px)`, `(0..1 extent)`.
- an internal (unexported) constant uses `/** @internal … */`.

## See also

- [enums](enums.md) — the value-**set** sibling · [extensions](extensions.md) — `{Noun}Extensions` helper objects · [naming](naming.md)
