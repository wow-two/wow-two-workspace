# Models

*Last updated: 2026-07-03*

> How to declare a model, in the order you build one. Scalars + dates → [type-mapping.md](type-mapping.md); enums →
> [enums.md](enums.md); the API envelope + errors are integration, not models → [state-and-data.md](../architecture/state-and-data.md).

**Flow:** `kind → file + name → shape + doc → members (doc → type) → mapper (only if a DTO)`

---

## 1. Kind

Default to a **bare domain model**; reach for a `*Dto` only to reshape a wire payload.

| Kind | Name | When |
|---|---|---|
| domain model | **bare** — `Invoice` | always — the app-facing entity |
| wire DTO | `*Dto` — `InvoiceDto` | only when the wire shape ≠ app shape (flat / denormalized / renamed) |
| content variant | `*Content` — `ImageContent` | a discriminated-union member on a `type` field |
| form values | `*Values` — `AddressValues` | the flat, all-editable shape a control set binds to |
| transient row | `*Draft` — `LineItemDraft` | a client-only builder row (adds a client `id`) |

- must use the bare model directly (no DTO, no mapper) when the wire shape already equals the app shape.
- must add a `*Dto` for a **shape** mismatch only — dates + enums are wired globally ([type-mapping.md](type-mapping.md)), never a reason for a DTO.
- no `*Request` / `*Response` — a write sends the bare model (or its `*Dto`); a failure returns `ProblemDetails`.

---

## 2. File + name

- must create one type per file, `PascalCase.ts` named after the export — `Invoice.ts`, `InvoiceDto.ts`.
- must co-locate it in the slice that **owns** it — a domain model in `domain/`, a view-model in `application/`, a wire DTO with its client in `integration/` ([architecture.md](../architecture/architecture.md)). Not fixed to one layer.
- must name the model **bare + singular**; a suffix marks each variant (§1). No `Model` / `Entity` suffix.
- slice's only public surface is its lowercase `index.ts` barrel.

---

## 3. Shape + doc

- must use `interface` for an object shape; `type` only for a union / alias / enum value-set.
- must open the type doc with **`Defines`** — one line.

```typescript
/** Defines an issued invoice and its lifecycle status. */
export interface Invoice {
```

---

## 4. Members

Per member, in order: **doc → type**.

- must open each member doc with **`Gets or sets`** — one line.
- must leave **one blank line between members** (member = its doc + the field), as in a C# model.
- must mark required as `field: T`, optional as `field?: T` — no `T | null`, no emitted null.
- must type each member per [type-mapping.md](type-mapping.md); enum fields per [enums.md](enums.md).
- must group a large model with `// ── Section ──` bands; no `@example`, no mechanism notes.

```typescript
  /** Gets or sets the invoice's unique id. */
  id: string;

  /** Gets or sets the current lifecycle status. */
  status: InvoiceStatus;

  /** Gets or sets the total amount due. */
  total: number;

  /** Gets or sets when the invoice was issued. */
  issuedAt: Temporal.Instant;

  /** Gets or sets the optional customer note. */
  note?: string;
}
```

---

## 5. Mapper — only if a `*Dto` exists

- must reshape `*Dto` ↔ model in one `mapInvoice(dto)` at the integration boundary ([state-and-data.md](../architecture/state-and-data.md)); a single `*Dto` serves both directions.
- must not leak a `*Dto` past `integration/`; the mapper only **reshapes** — dates + enums are already wired globally.
