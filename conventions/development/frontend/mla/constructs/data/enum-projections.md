# Enum projections

*Last updated: 2026-08-19*

> The two `Record` shapes an enum is projected through — one for what a member looks like, one for what it sends.
> Purpose — the enum stays a bare value set, and everything layered on it is keyed by that set, so a new member
> is a compile error in every projection rather than a silent gap.
> Use case — an option needs a label or an icon, or a wire payload the bare value cannot carry.

The enum itself is a language form → [enums](../../../lla/components/enums.md).

---

## Displays

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

## Payloads

- must model a rich send-object as `{Enum}Payloads: Record<Enum, {Enum}Payload>` in `domain` or `integration`,
  when the wire value alone cannot be sent — picked by the enum, sent as-is.
- must keep the payload out of `presentation`; a display and a payload never share a shape.

---

## Neighbours

- [enums](../../../lla/components/enums.md) — the value set these are keyed by
- [models](models.md) — the shapes a projection carries
