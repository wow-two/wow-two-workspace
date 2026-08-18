# Models

*Last updated: 2026-07-03*

> How to declare a model, in the order you build one. Scalars + dates → [type-mapping.md](../../domains/api/type-mapping.md); enums →
> [enums](../../../lla/components/enums.md); the API envelope + errors are integration, not models → [state-and-data.md](../../domains/data/state-and-data.md).

**Flow:** `kind → file + name → shape + doc → members (doc → type) → mapper (only if a DTO)`

---

## 1. Kind

Every client-side data model carries a **`*Dto`** suffix — it marks "a data shape" and disambiguates from a same-noun enum (`BuilderStyle` reads like an enum; `BuilderStyleDto` doesn't). The **prefix** names the role. Only a wire **write** payload breaks the pattern — it's a `*Request`.

- **read model / entity** — `{Noun}Dto` (`CodeDto`) · `domain` — the app-facing thing = the wire read shape, used directly; a read returns the `*Dto` (the frontend entity *is* what the backend sends — no separate `*Response`)
- **form model** — *none separate by default* — the create/update form binds the write **`{Noun}CreateUpdateApiRequest`** (`CodeCreateUpdateApiRequest`) directly (there is no `Create`/`Update` *Dto*). UI-only concerns (a rule-row key) belong to the form lib, not a modeled field; add a thin form type only if editing needs props the wire doesn't carry
- **nested sub-model** — **lives in its parent's layer** — a read sub-model `*Dto` in `domain` (`RuleDto` · `CodeStyleDto` on `CodeDto`); a write sub-model `*ApiRequest` in `integration` (`RuleApiRequest` · `StyleApiRequest` on the request)
- **write contract** — `{Noun}{Verb}ApiRequest` · `integration` — the wire payload a write sends (mirrors the backend `*ApiRequest`), **noun-first** (the entity, or the domain/subdomain for a multi-entity action) so a concern's requests group together. Verb = the CRUD action (`Create` · `Update` · `SetActive` · `Preview`); a shared create+update **body** is `{Noun}CreateUpdateApiRequest` (`CodeCreateUpdateApiRequest`) — the id rides the URL, so split into `{Noun}Create`/`{Noun}Update` only once the bodies diverge. **Nested** models take `*Dto` (`CodeRuleDto` · `CodeStyleDto`), never `*ApiRequest` — only the top-level endpoint body is `*ApiRequest`; a request references the shared domain `*Dto` (or a request-specific `*Dto` in `integration` if it differs)
- **list row** — `{Noun}RowDto` (`CodeRowDto`) · when a list projects a lighter shape than the full entity
- **list query** — `{Noun}QueryDto` (`CodesQueryDto`) · the search + paging params a list read takes
- **content variant** — `{Noun}Content` (`WifiContent`; union `CodeContent`) · `domain` — a discriminated-union member on a `type` field; **no `Dto`** (mirrors the backend; content names don't clash with enums)
- **descriptor + catalog** — a declared variant-set's lookup / dispatch table · `domain`; not a wire shape → **no `*Dto`**:
  - `{Noun}Descriptor` — **one entry**: a variant's identity + display + behavior (`ContentTypeDescriptor` = `{ id, label, mode }`)
  - `{noun}Catalog` — the **exhaustive static list** of descriptors + a `{noun}(id)` lookup; lets the UI *enumerate* the set and *resolve a per-type fact without a switch*
  - `Descriptor` not `Spec` (`.spec` / behavior-test collision); `Catalog` not `Registry` (implies runtime registration). File named after the descriptor, in the slice's `models/`

- a **write** sends its `*Request`, never a form / entity Dto — the entity carries server-owned fields (id · slug · scanCount) a write must not.
- a **read** returns its `*Dto` directly; `*Response` is reserved for a genuine wrapper (paging), never a plain entity read.
- a wire ≠ app **shape** mismatch → map it at the `integration` boundary; the app still sees one `*Dto`. Dates + enums are wired globally ([type-mapping.md](../../domains/api/type-mapping.md)), never a reason for a mapper.
- enums stay **bare** — the `*Dto` on the model is what separates a `BuilderStyleDto` model from a `BuilderStyle`-style enum name.

---

## 2. File + name

- must name the model **bare + singular**; a suffix marks each variant (§1). No `Model` / `Entity` suffix.
- **file granularity — split independent, group tight:** a model referenced on its own or that grows → its own `PascalCase.ts`; a cohesive family used together (a `*Request` set · an aggregate + its inline sub-shapes) → one file. Don't force one-type-per-file (a C# / assembly rule with no TS analog); don't dump unrelated models together.
- must place model files in a **`models/` role-group** within their slice — symmetric with `components/` / `hooks/` (e.g. `domain/codes/style/models/` · `integration/codes/models/`).
- must co-locate a model in the slice that **owns** it — entity in `domain/`, form `*Input` in `application/`, `*Request` / `*Dto` with its client in `integration/` ([architecture.md](../../architecture/architecture.md)).
- slice's only public surface is its lowercase `index.ts` barrel.

---

## 3. Shape + doc

- must use `interface` for an object shape; `type` only for a union / alias / enum value-set.
- must open the type doc with **`Represents`** for a data model (an interface that holds data) — one line; **`Defines`** only for an abstraction / contract / enum. (We have no classes; a data interface *represents* its data — mirrors [documentation](../../../../backend/dotnet/lla/notation/documentation/documentation.md) + the frontend [documentation](../../../lla/notation/documentation/documentation.md) verb table.)

```typescript
/** Represents an issued invoice and its lifecycle status. */
export interface Invoice {
```

---

## 4. Members

Per member, in order: **doc → type**.

- must open each member doc with **`The …`** — a value noun phrase, one line. TS has no get/set, so a model field reads like a prop's `value` ([components](../components.md) § Members) — never `Gets or sets` (a C# get/set idiom).
- must leave **exactly one blank line between every documented member** of an interface / type (member = its doc + the field), as in a C# model — a general model-formatting rule, mirroring the blank-line-before-derived-type in [enums](../../../lla/components/enums.md).
- must mark required as `field: T`, optional as `field?: T` — no `T | null`, no emitted null.
- must type each member per [type-mapping.md](../../domains/api/type-mapping.md); enum fields per [enums](../../../lla/components/enums.md).
- must group a large model with `// ── Section ──` bands; no `@example`, no mechanism notes.

```typescript
  /** The invoice's unique id. */
  id: string;

  /** The current lifecycle status. */
  status: InvoiceStatus;

  /** The total amount due. */
  total: number;

  /** When the invoice was issued. */
  issuedAt: Temporal.Instant;

  /** The optional customer note. */
  note?: string;
}
```

---

## 5. Mapper — only if a `*Dto` exists

- must reshape `*Dto` ↔ model in one `mapInvoice(dto)` at the integration boundary ([state-and-data.md](../../domains/data/state-and-data.md)); a single `*Dto` serves both directions.
- must not leak a `*Dto` past `integration/`; the mapper only **reshapes** — dates + enums are already wired globally.
