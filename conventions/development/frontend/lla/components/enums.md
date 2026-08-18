# Enums

*Last updated: 2026-07-05*

> How to declare an enum and layer its display + send-object data. The enum is a `const` object — PascalCase key → camelCase wire value — and the **only** enum constant; display + payloads attach as `Record<Enum, …>` keyed by it. No TS `enum` keyword.

**Flow:** `kind → location → doc + shape → members → export → displays → payloads → use`

---

## 1. Kind

The fork that drives location.

|                           | Domain enum                                 | Non-domain enum                      |
|---------------------------|---------------------------------------------|--------------------------------------|
| Tied to a product domain? | **yes** — even if it never hits the backend | no                                   |
| Examples                  | `BarcodeFormat` · `ModuleShape` · `Plan`    | `ButtonType` · `Key` (SDK UI tokens) |

- must classify by **domain tie** (`identity` · `codes` · `billing` …), not by whether it crosses the API — a product-domain concept → domain enum; a UI / app / integration token → non-domain.

---

## 2. Location

- must create a **domain enum** in the [`domain` layer](../../mla/architecture/architecture.md), at `domain/{sub-domain}/enums/{EnumName}.ts`.
- must place a **non-domain enum** in the layer that owns it — `application` / `integration` / `presentation`; no fixed home.
- must name it singular, no `Enum` suffix — `BarcodeFormat`, not `BarcodeFormats`.

---

## 3. Shape and documentation

- must JSDoc the type with a one-liner starting **`Defines …`** ([documentation](../notation/documentation/documentation.md)).
- must declare a `const` object `as const`, then derive the type.
- must not use the TS `enum` keyword — nominal-typing + `const enum` pitfalls; the const object is tree-shakeable and the value *is* the wire string.

```typescript
/** Defines the QR data-module body shape. */
export const ModuleShape = { … } as const;
```

---

## 4. Members and documentation

- must document each member with a JSDoc one-liner starting **`Refers to …`** — what the value stands for.
- must use a **PascalCase key** + a **camelCase value** — the value *is* the wire string ([serialization casing](../../../backend/dotnet/mla/platform/responses/serialization.md#contract)).
- must **not** add an `Unresolved` / `Unknown` sentinel member — keep three concerns separate:
  - **nothing selected** → `null` / optional field (form state); omit on send, never emit null.
  - **"any / all"** → a real member present on **both** sides, or modeled as absence.
  - **unmappable inbound value** (deploy skew / corrupt data) → handled at the **read boundary** (the api mapper coerces to a safe default or drops + logs) — it never enters the typed union, so pickers and exhaustive switches stay clean.

```typescript
export const ModuleShape = {
  /** Refers to a plain square module. */
  Square: "square",
  /** Refers to a module with rounded corners. */
  Rounded: "rounded",
} as const;
```

---

## 5. Export

- must derive the type from the const on its own line, with a **blank line before it**.

```typescript
export const ModuleShape = {
  …
} as const;

export type ModuleShape = (typeof ModuleShape)[keyof typeof ModuleShape];
```

---

## 6. Displays — presentation extension

- must extract display data out of the enum into a **`{Enum}Display` interface** in the presentation layer, JSDoc'd with `Defines …`.
- the interface **may** carry `label` · `description` · `icon` (a `ReactNode`) · any enum-specific field — the shape is the app's.
- must **not** doc the interface members — the field names carry themselves.
- must bind it as **`{Enum}Displays: Record<Enum, {Enum}Display>`**, JSDoc'd with **`Maps …`** — one entry per member, looked up by value, no mapper.
- must declare the interface + its `Record` in the **same file** — one unit, the exception to one-type-per-file.

```typescript
// presentation/codes/core/shape/ShapeDisplays.ts
/** Defines the display for a module-shape option. */
interface ModuleShapeDisplay {
  label: string;
  icon: ReactNode;
}

/** Maps each module shape to its display. */
export const ModuleShapeDisplays: Record<ModuleShape, ModuleShapeDisplay> = {
  [ModuleShape.Square]: { label: "Square", icon: <SquareSwatch /> },
  [ModuleShape.Rounded]: { label: "Rounded", icon: <RoundedSwatch /> },
};
```

---

## 7. Payloads — backend extension

- must model a rich send-object as **`{Enum}Payloads: Record<Enum, {Enum}Payload>`** (`domain` / `integration`) when the wire value alone can't be sent — picked by the enum, sent as-is.

---

## 8. Use

**No bare-union types**
- must **not** declare a domain or UI value-set as a bare string-union `type` (`type X = "a" | "b"`) — a union is a type with **no value source**, so every use site falls back to a magic string literal.
- must declare the const-object enum (§3) and derive the type from it, then compare by member (`X.A`) — never the literal.

```typescript
type Nav = "strip" | "pills";                     // ❌ no value source — magic strings everywhere

export const Nav = {                               // ✅ const object → value source + derived type
  /** Refers to the segmented strip layout. */
  Strip: "strip",
  /** Refers to the pill-group layout. */
  Pills: "pills",
} as const;

export type Nav = (typeof Nav)[keyof typeof Nav];
```

**The enum**
- must compare by key, never a magic string.

```typescript
if (code.barcodeFormat === BarcodeFormat.QrCode) { }   // ✅
if (code.barcodeFormat === "qrCode") { }                // ❌
```

**No parallel `isMember` flags**
- must model a value that is one of an enum's members as the **enum**, then compare `x === Enum.Member` at the use site — never fan it into a family of derived booleans (`isSolid` + `isGradient`, `isLinear` + `isRadial`).
- a boolean-per-member family doesn't scale (new member ⇒ new flag at every branch) and a fall-through `if/else` silently mishandles it — a `switch (x)` or an enum-keyed `Record` (§6) stays exhaustive.
- deriving the enum from a nullable / binary field is fine — do it **once** (`const fill = gradient ? FillType.Gradient : FillType.Solid`), then compare `fill`.
- a standalone predicate with no underlying enum (`const isEdit = Boolean(id)`) may stay a boolean.

```typescript
const fill = gradient ? FillType.Gradient : FillType.Solid;
{fill === FillType.Gradient ? <GradientRow/> : <SolidRow/>}   // ✅ compare the enum
const isGradient = gradient !== null; …{isGradient && …}       // ❌ boolean stand-in
```

**With a `Displays` extension**
- must read display from the record by value.

```typescript
const { label, icon } = BarcodeFormatDisplays[code.barcodeFormat];
```

**As a field**
- a model / DTO field is the enum type (`barcodeFormat: BarcodeFormat`); the wire string already fits — nothing converts it ([models.md](../../mla/components/data/models.md)).
- a form-values field is `string` (a `<select>` emits strings), narrowed back to the enum on submit ([forms.md](../../mla/domains/forms/forms.md)).
</content>
