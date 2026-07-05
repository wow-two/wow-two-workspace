# Forms

*Last updated: 2026-07-03*

> Editable form state for a model — a flat, forgiving `*Values` shape, resolved back to the model on submit.
> The type contract + enums: [../code-style/type-mapping.md](../code-style/type-mapping.md) · [../code-style/enums.md](../code-style/enums.md).

## `*Values` — the editable shape

A form binds a `{Model}Values` type ([../code-style/models.md](../code-style/models.md)), not the domain model — HTML inputs need a forgiving, all-editable shape.

- must name it `{Model}Values` — `InvoiceValues` for `Invoice`.
- must type enum fields as `string` (a `<select>` binds strings), scalars as-is, and a date field as the SDK control's value type (`Date` / `TimeValue`).
- must keep fields forgiving while editing (`?` / `""` / `null`) — validation runs on submit, not per keystroke.

```typescript
/** Defines the editable fields of the invoice form. */
export interface InvoiceValues {
  /** Gets or sets the status, as the raw select value. */
  status: string;

  /** Gets or sets the total, as entered. */
  total: number | null;

  /** Gets or sets the issue date from the picker. */
  issuedAt: Date | null;
}
```

---

## Flow

```
domain model            → *Values (strings / control types)   ← seed the form from the model
user edits              → resolve + validate on submit         ← strings → enums, Date/TimeValue → Temporal.*
                        → domain model (or its *Dto)           ← send to the API
```

- must resolve on submit — narrow enum strings to the enum ([../code-style/enums.md](../code-style/enums.md)) and bridge `Date` / `TimeValue` → `Temporal.*` ([../code-style/type-mapping.md](../code-style/type-mapping.md)); surface validation errors, never silently coerce.

---

## Inputs

- must prefer `@wow-two-beta/ui` controls (`TextInput`, `Select`, `DatePicker`, `TimeField`, …) over hand-rolled ones — [components.md](components.md).
- must keep form state local (`useState`); lift to a hook only when it must be shared.
- must derive dropdown options from the enum label record — `enumOptions({Enum}Labels)` ([../code-style/enums.md](../code-style/enums.md)).
