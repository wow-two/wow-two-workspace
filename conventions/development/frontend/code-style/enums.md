# Enums

*Last updated: 2026-07-03*

> How a fixed value-set is declared in TS so it reads **PascalCase in code** and travels **camelCase on the wire**.
> Purpose — one enum shape that maps to the backend `enum` with zero runtime translation (the wire value *is* the value).
> Supersedes the former TS-`enum` + label-`Record` prescription; every product already uses (or is moving to) the const-object form.

## Pattern — const object `as const`

- must declare a const object with **PascalCase keys** (code-facing) and **camelCase string values** (the wire form), then derive the type.
- must not use the TS `enum` keyword — the const object is tree-shakeable, has no nominal-typing / `const enum` pitfalls, and the value *is* the wire string.
- must name it singular, no `Enum` suffix — `BarcodeFormat`, not `BarcodeFormats` / `BarcodeFormatEnum`.

```typescript
/** Defines the rendering symbology of a code. */
export const BarcodeFormat = {
  QrCode: "qrCode",
  DataMatrix: "dataMatrix",
  Code128: "code128",
} as const;
export type BarcodeFormat = (typeof BarcodeFormat)[keyof typeof BarcodeFormat];
```

- **PascalCase for usage** — code references the key: `BarcodeFormat.QrCode`.
- **camelCase for mapping** — the value *is* the wire string (`"qrCode"`); the field type is the union of those values. Assigning `BarcodeFormat.QrCode` yields `"qrCode"` — no mapper, no lookup.

---

## Wire contract — camelCase both sides

- backend **must** serialize / deserialize enums as camelCase — `JsonStringEnumConverter(JsonNamingPolicy.CamelCase)` (see [../backend/persistence/enums.md](../../backend/persistence/enums.md)). This is a **required backend change** for products still emitting PascalCase enum names.
- because the wire value equals the const value, a DTO enum field is typed as the enum directly (`barcodeFormat: BarcodeFormat`) — the mapper passes it through unchanged (enums are identity; only dates transform — see [models.md](models.md)).

---

## Labels — the display bridge

- domain enums **must** ship a `{Enum}Labels: Record<Enum, string>` — a compile error forces a label for every member (later swapped for backend-served translations).
- must key labels by the enum member, not the raw string.

```typescript
/** Human-readable labels for BarcodeFormat. */
export const BarcodeFormatLabels: Record<BarcodeFormat, string> = {
  [BarcodeFormat.QrCode]: "QR code",
  [BarcodeFormat.DataMatrix]: "Data Matrix",
  [BarcodeFormat.Code128]: "Code 128",
};
```

---

## Unresolved fallback

- a domain enum **must** include `Unresolved: "unresolved"` as its **first** member — the fallback when a value can't be resolved (bad / future wire data must not crash the UI).
- must default to `Unresolved` when mapping an unknown wire value; log it.

---

## Usage

```typescript
if (code.barcodeFormat === BarcodeFormat.QrCode) { }   // ✅ compare via the key
const label = BarcodeFormatLabels[code.barcodeFormat];  // ✅ display via labels
const options = enumOptions(BarcodeFormatLabels);        // ✅ dropdowns from labels
if (code.barcodeFormat === "qrCode") { }                 // ❌ magic-string compare
```

---

## Domain enum vs UI value-set

Both use the const-object shape; they differ in whether they cross the API + need labels.

| | Domain enum | UI value-set |
|---|---|---|
| Crosses the API? | **yes** — camelCase values match the backend | no — internal plumbing |
| Label record? | **required** (`{Enum}Labels`) | none |
| `Unresolved` member? | **yes**, first | no |
| Examples | `BarcodeFormat`, `Plan`, `RuleConditionType` | `ButtonType`, `HtmlElement`, `Key`, `ModuleShape` (style token) |

- must pick by what the set *is* — user-facing + API-mapped → domain enum; pure UI/runtime token → value-set (see [extensions.md](extensions.md) for the same shape).

---

## Location

- must live in the domain layer: `domain/{domain}/{sub}/enums/{EnumName}.ts` (single app) — one file per enum + its labels, exposed via the slice barrel.

---

## Enums in models vs forms

- **domain models + DTOs** — enum field typed as the enum ([models.md](models.md)); the wire value satisfies it directly.
- **form values** (`*Values`) — enum fields are `string` (HTML `<select>` binds strings); the `*Values` → request bridge narrows back to the enum ([forms.md](../presentation/forms.md)).
