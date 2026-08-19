# Enum display

*Last updated: 2026-08-19*

> What a member of an enum looks like — a `{Enum}Display` interface bound as a `Record` keyed by the enum.
> Purpose — a new member becomes a compile error in the display map, never a silently unlabelled option.
> Use case — an option needing a label, a description or an icon.

The enum itself is a language form → [enums](../../../lla/components/enums.md).

---

## Declaration

- must extract display data into a `{Enum}Display` interface in `presentation`, documented with `Defines …`.
- may carry `label` · `description` · `icon` or any enum-specific field — the shape is the app's.
- must not document the interface members; the field names carry themselves.
- must bind it as `{Enum}Displays: Record<Enum, {Enum}Display>`, documented with `Maps …`, one entry per member.
- must declare the interface and its `Record` in the same file, the one exception to one type per file.

```tsx
/** Defines the display for a module-shape option. */
interface ModuleShapeDisplay { label: string; icon: ReactNode }

/** Maps each module shape to its display. */
export const ModuleShapeDisplays: Record<ModuleShape, ModuleShapeDisplay> = {
  [ModuleShape.Square]: { label: "Square", icon: <SquareSwatch /> },
  [ModuleShape.Rounded]: { label: "Rounded", icon: <RoundedSwatch /> },
};
```

---

## Neighbours

- [enum payload](enum-payload.md) — what the same member sends
- [enums](../../../lla/components/enums.md) — the value set this is keyed by
