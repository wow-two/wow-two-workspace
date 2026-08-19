# Type mapping

*Last updated: 2026-08-19*

> The one .NET ↔ JSON wire ↔ TS scalar contract every layer obeys — models, forms, API client, enums.
> Purpose — one authority for which TS type represents a .NET type, so dates and enums wire once, globally.

## Scalar contract

| .NET (CLR) | wire (JSON) | TS | Notes |
|---|---|---|---|
| `Guid` | `string` | `string` | ids are plain strings |
| `string` | `string` | `string` | |
| `bool` | `bool` | `boolean` | |
| `int` / `long` / `decimal` | `number` | `number` | no `bigint`, no decimal-as-string |
| `enum` | camelCase `string` | const-type ([enums](../../../lla/components/enums.md)) | wire value **is** the value |
| `DateTimeOffset` / `DateTime` | ISO-8601 `string` | `Temporal.Instant` | see Dates |
| `DateOnly` | `yyyy-MM-dd` | `Temporal.PlainDate` | date-only, no time/zone |
| `TimeOnly` | `HH:mm:ss` | `Temporal.PlainTime` | time-only |
| `TimeSpan` | ISO-8601 duration | `Temporal.Duration` | |
| `IReadOnlyList<T>` | array | `ReadonlyArray<T>` | typed generic, never `T[]` — see Collections |
| `IReadOnlyDictionary<K,V>` | object | `ReadonlyMap<K,V>` | |
| `T?` (nullable) | key omitted when null | `field?: T` | never emit `null`; `?` alone models "absent" |

---

## Dates — Temporal, wired globally

- must map dates with **Temporal** (`@js-temporal/polyfill` until native) — it covers every .NET date type 1:1.

| .NET | Temporal | Why |
|---|---|---|
| `DateTimeOffset` / `DateTime` (a timestamp) | `Temporal.Instant` | the absolute instant is canonical |
| `DateOnly` | `Temporal.PlainDate` | no time, no zone |
| `TimeOnly` | `Temporal.PlainTime` | no date, no zone |
| `TimeSpan` | `Temporal.Duration` | |
| naive `DateTime` (no offset, rare) | `Temporal.PlainDateTime` | only for a zoneless datetime |

- must type date fields as the `Temporal.*` type on **both** the model and any `*Dto` — never a raw `string`.
- must format at the view (`instant.toZonedDateTimeISO(tz)` / `Intl`); never store a formatted string on a model.

---

## Wiring — one reviver, no per-model code

- must convert dates at the **HTTP client boundary** ([state and data](../data/state-and-data.md)), globally,
  never in a per-type mapper.
- **inbound** — the client parses with a reviver: `JSON.parse(text, temporalReviver)`. It matches a **strict**
  ISO pattern per string and returns the right `Temporal.*` — `…T…Z`/offset → `Instant`;
  `^\d{4}-\d{2}-\d{2}$` → `PlainDate`; `^\d{2}:\d{2}(:\d{2})?$` → `PlainTime`; `^P…` → `Duration`.
  A non-matching string passes through unchanged.
- **outbound** — no code: every `Temporal.*` has a `toJSON()` returning its ISO string, so
  `JSON.stringify(body)` serializes dates automatically.
- must keep the pattern strict — require the `T`/`Z` or an exact date/time/duration shape — so a normal string
  is never mis-converted; exclude a known-ISO-but-keep-as-string field by key.
- must house the reviver in `integration/` (the client), or the shared FE package once it exists — it is the
  app's single date seam.
- must not map a date per field or per `*Dto` — a mapper only reshapes ([models](../../constructs/data/models.md)).

---

## Enums

- wire value = the const-object's camelCase value = the TS enum value → **identity**, no mapping.
- must serialize camelCase on the backend (`JsonStringEnumConverter(JsonNamingPolicy.CamelCase)`); full
  pattern: [enums](../../../lla/components/enums.md).

---

## Collections

- must use typed generics — `ReadonlyArray<T>` (read models / DTOs / props), `Array<T>` (mutable local
  builders), `ReadonlySet` / `ReadonlyMap` for unique / keyed.
- must not use bracket `T[]` / `readonly T[]`.

---

## Nullability

- required → `field: T` · optional → `field?: T`.
- must not emit `null` on the wire — the backend omits the key, and `?` alone models absence
  ([typescript](../../../lla/constructs/typescript/typescript.md) § *Absence*).
