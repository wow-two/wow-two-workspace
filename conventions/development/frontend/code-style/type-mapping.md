# Type mapping

*Last updated: 2026-07-03*

> The one .NET ↔ JSON wire ↔ TS scalar contract every layer obeys — models, forms, API client, enums.
> Purpose — a single authority for "what TS type represents this .NET type", so a field reads the same on both sides of
> the wire and dates/enums are wired **once**, globally, not per model.

## Scalar contract

| .NET (CLR) | wire (JSON) | TS | Notes |
|---|---|---|---|
| `Guid` | `string` | `string` | ids are plain strings |
| `string` | `string` | `string` | |
| `bool` | `bool` | `boolean` | |
| `int` / `long` / `decimal` | `number` | `number` | no `bigint`, no decimal-as-string |
| `enum` | camelCase `string` | enum const-type ([enums.md](enums.md)) | wire value **is** the enum value — no mapping |
| `DateTimeOffset` / `DateTime` | ISO-8601 `string` | `Temporal.Instant` | see Dates |
| `DateOnly` | `yyyy-MM-dd` | `Temporal.PlainDate` | date-only, no time/zone |
| `TimeOnly` | `HH:mm:ss` | `Temporal.PlainTime` | time-only |
| `TimeSpan` | ISO-8601 duration | `Temporal.Duration` | |
| `IReadOnlyList<T>` | array | `ReadonlyArray<T>` | typed generic, never `T[]` — see Collections |
| `IReadOnlyDictionary<K,V>` | object | `ReadonlyMap<K,V>` | |
| `T?` (nullable) | key omitted when null | `field?: T` | never emit `null`; `?` alone models "absent" |

---

## Dates — Temporal, wired globally

Dates are the one non-trivial mapping. Use **Temporal** (`@js-temporal/polyfill` until native) — it maps every .NET date type 1:1.

| .NET | Temporal | Why |
|---|---|---|
| `DateTimeOffset` / `DateTime` (a timestamp) | `Temporal.Instant` | the absolute instant is canonical; Temporal has no `OffsetDateTime`, and the wire offset is presentational — format in the viewer's zone at render |
| `DateOnly` | `Temporal.PlainDate` | no time, no zone |
| `TimeOnly` | `Temporal.PlainTime` | no date, no zone |
| `TimeSpan` | `Temporal.Duration` | |
| naive `DateTime` (no offset, rare) | `Temporal.PlainDateTime` | only if the backend ever sends a zoneless datetime |

- must type date fields as the `Temporal.*` type on **both** the model and any `*Dto` — never a raw `string`.
- must format for display at the view (`instant.toZonedDateTimeISO(tz)` / `Intl`), never store a formatted string on the model.

---

## Wiring — one reviver, no per-model code

Dates convert at the **HTTP client boundary** ([state-and-data.md](../architecture/state-and-data.md)), globally — never in a per-type mapper.

- **inbound** — the client parses with a reviver: `JSON.parse(text, temporalReviver)`. The reviver matches a **strict** ISO pattern per string and returns the right `Temporal.*` (`…T…Z`/offset → `Instant`; `^\d{4}-\d{2}-\d{2}$` → `PlainDate`; `^\d{2}:\d{2}(:\d{2})?$` → `PlainTime`; `^P…` → `Duration`). A non-matching string passes through unchanged.
- **outbound** — no code: every `Temporal.*` has a `toJSON()` returning its ISO string, so `JSON.stringify(body)` serializes dates automatically.
- must keep the pattern strict (require the `T`/`Z` or an exact date/time/duration shape) so a normal string is never mis-converted; exclude a known-ISO-but-keep-as-string field by key if one ever appears.
- must house the reviver in `integration/` (the client), or the shared FE package once it exists — it is the single date seam for the whole app.

> This is why there is **no per-field date mapping** and dates never force a `*Dto`: the reviver already handed the model a
> `Temporal.*`. A mapper exists only to reshape (flat ↔ rich), never to parse a date ([models.md](models.md)).

---

## Enums

- wire value = the const-object's camelCase value = the TS enum value → **identity**, no mapping. Backend must serialize camelCase (`JsonStringEnumConverter(JsonNamingPolicy.CamelCase)`). Full pattern: [enums.md](enums.md).

---

## Collections

- must use typed generics — `ReadonlyArray<T>` (read models / DTOs / props), `Array<T>` (mutable local builders), `ReadonlySet` / `ReadonlyMap` for unique / keyed. Never bracket `T[]` / `readonly T[]`. Mirrors `IReadOnlyList<T>` / `List<T>`.

---

## Nullability

- required → `field: T` · optional → `field?: T`. Never `T | null` and never emit `null` on the wire — the backend omits null keys ([models.md](models.md)).
