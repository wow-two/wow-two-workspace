# UZ Geocoder — national address normalisation & geocoding API

*Last updated: 2026-08-09*

> **Status:** spec only, nothing built. Pick #1 from [cadastre-agency-analysis.md](cadastre-agency-analysis.md).
> One sentence: **Uzbekistan has no working geocoder, and the state is about to build the address register
> that makes one possible.** Sell the primitive, not the map.
> Play: **B2B, no procurement required.** Ports: API `8250` https / `8251` http · Vite `8252`.
>
> **Re-ranked 2026-08-10** by [uz-govtech-demand-map.md](uz-govtech-demand-map.md): `P1` drops from #1 to #3.
> It stays load-bearing under ~16 government bodies, but it sells as the **engine inside a registry-crosswalk
> product**, not as a standalone register. Two facts moved it: the World Bank already has ~$1.8M of address
> packages under procurement, and the funded target for a national address register is **June 2030**, not
> end-2026. Build the matcher; do not pitch a rival register.

---

## 1 · The problem

- Uzbek addresses are written five ways for one place — Cyrillic, Latin, Russian, old street name, mahalla name
- `Toshkent sh., Yunusobod t., 12-kvartal, 34-uy, 12-xonadon` vs `г. Ташкент, Юнусабад, кв. 12, д. 34, кв. 12`
- Google Maps geocoding covers Tashkent arterials, degrades hard past regional centres, and misses mahallas
- Yandex is better on Tashkent, still weak on rural `MFY`-level addressing
- no open UZ address dataset exists with cadastral linkage
- every bank, insurer, courier, utility, and marketplace re-solves this badly, in-house, per company

## 2 · Why now

- `GISTD` B.2 funds a **national address register** — regulation + information system + Samarkand field capture
- `UZKAD` mandate: every object registered + address register on **`WGS-84` by end-2026**
- 6.3M individual homes being pulled into the registry
- 80 new CORS stations raise positional accuracy nationwide
- window: build the normalisation engine now on scraped/derived data, swap the backing dataset when the
  official register opens — the API contract does not change

`[corrected 2026-08-10]` — the "nobody is building this" premise was wrong on two counts:

- `GISTD` April-2026 procurement plan carries **5 address packages, ~$1.8M**, three open to international
  firms; `QCBS/01` is already Under Review
- the ISR target for the register itself is **June 2030**, and `GISTD` has disbursed 0.31% of $35M
- net effect: the state register arrives late enough that a working matcher has years of runway,
  but the **register itself is not the product** — the crosswalk between the five parallel address stores is
- those stores: Cadastre `UZKAD` + Unified Register of Addresses · MIA `Pasport-viza` · Statistics census
  household points · Tax `TsBD` free-text · utility service-address strings
- **legal ownership is not contested** — CM Res. `1010` (2018-12-14) names the Cadastre Agency, binding on
  all state bodies since 2019-01-01, amended as recently as CM Res. `791` (2025-12-15). Operational
  ownership is contested only because the register does not exist in usable form yet.

## 3 · Product surface

Three things, one service.

| Surface | Input | Output |
|---|---|---|
| **Normalise** | free-text address, any script | canonical structured address |
| **Geocode** | canonical or free-text address | `lat`/`lon` + confidence + admin hierarchy |
| **Reverse** | `lat`/`lon` | nearest canonical address + admin hierarchy |

Plus two derived endpoints that are where the money is:

- **Batch** — CSV/JSONL in, enriched out; how a bank cleans 400k customer records once
- **Autocomplete** — typeahead for checkout and onboarding forms; the volume driver

## 4 · Canonical address model

```
region        Toshkent shahri            // 14 units incl. Karakalpakstan
district      Yunusobod tumani           // ~200
mahalla       Bodomzor MFY               // MFY / community — the level foreign geocoders miss
street        Amir Temur ko'chasi
house         34
block         12-kvartal                 // optional
apartment     12                         // optional
postalCode    100084
cadastralNo   10:09:03:01:01:0001        // optional, when linkable
lat / lon     41.3389, 69.2847           // WGS-84
confidence    0.0 – 1.0
matchLevel    exact | house | street | mahalla | district | region
```

Rules:

- **Latin is canonical**, Cyrillic and Russian forms carried as aliases
- every level resolvable independently — a request that only resolves to `mahalla` returns that, honestly scored
- never invent a house number to raise confidence; `matchLevel` carries the truth

## 5 · Data strategy

Layered, so no single source is a dependency.

| Layer | Source | Licence risk |
|---|---|---|
| base geometry | OpenStreetMap UZ extract | ODbL — attribution, share-alike on derived DB |
| admin hierarchy | official region/district/`MFY` lists | public |
| street + house | OSM + field-derived corrections | ODbL |
| aliases | transliteration rules + observed variants | own |
| cadastral link | `UZKAD` / geoportal, licensed | **unresolved — see §10** |
| corrections | customer feedback loop | own, the moat |

- ODbL share-alike applies to the derived database, not to geocoding results served over an API —
  structure the build so the OSM-derived DB stays separable from the proprietary alias/correction layers
- the **correction ledger** is the durable asset: every customer batch that gets manually fixed feeds it back
- do not scrape the paid registry; the licensing question is answered before any cadastral linkage ships

## 6 · Architecture

Standard conformant product repo — `create-repo` shape.

```
{slug}.backend-services/     .NET 10, Clean Arch 4 projects
  Domain          address model, match levels, confidence scoring
  Application     normalise / geocode / reverse / batch handlers (mediator)
  Infrastructure  tokenizer, transliterator, scorer, tile client
  Persistence     PostgreSQL + PostGIS + pg_trgm
{slug}.frontend-services/    React 19 + Vite, @wow-two-beta/ui
```

- `WoW2.Sdk.Backend.Beta` for hosting, observability, mediator, result/error layer, API keys
- `PostGIS` for spatial index; `pg_trgm` + custom tokenizer for fuzzy string match
- matching is a **cascade**, not a single query: exact → normalised-exact → trigram → phonetic → spatial fallback
- transliteration table is a first-class domain artifact (Cyrillic ↔ Latin ↔ Russian), unit-tested per rule
- no Esri, no proprietary GIS licence anywhere in the stack
- `MapLibre` + self-hosted tiles for the demo/playground frontend

## 7 · API sketch

```
POST /v1/normalize        { "text": "г. Ташкент, Юнусабад, кв.12, д.34" }
POST /v1/geocode          { "text": "...", "hint": { "region": "Toshkent shahri" } }
POST /v1/reverse          { "lat": 41.3389, "lon": 69.2847 }
POST /v1/batch            NDJSON stream in → NDJSON stream out
GET  /v1/autocomplete     ?q=amir+te&limit=8
GET  /v1/admin/regions    hierarchy reference data, free
```

- API-key auth, per-key quota, `429` with `Retry-After`
- every response carries `matchLevel` + `confidence` + `sources[]`
- deterministic: same input → same output, versioned dataset id in the response

## 8 · Packaging

| Tier | Volume | Target |
|---|---|---|
| Free | 1k req/mo | evaluation, side projects |
| Startup | 50k req/mo | marketplaces, delivery |
| Business | 500k req/mo | banks, insurers, utilities |
| Batch | per-record | one-off DB cleanups |
| On-prem | flat | banks with data-residency rules |

- **on-prem is the real enterprise line** — UZ banks resist sending customer addresses to a third party
- batch cleanup is the wedge: a single 400k-record job proves value in one invoice, no integration

## 9 · Build order

1. admin hierarchy + transliteration engine + normaliser — no geocoding yet, testable alone
2. OSM UZ import into `PostGIS`, street/house layer
3. match cascade + confidence scoring, measured against a hand-labelled 1k-address gold set
4. HTTP API + keys + quota
5. batch endpoint + NDJSON streaming
6. playground frontend — paste an address, see the parse, see the pin
7. autocomplete
8. correction ledger + feedback intake
9. cadastral linkage — **gated on §10**

Ship 1–4 before talking to a single customer; the gold-set accuracy number is the sales argument.

## 10 · Kill gates & open questions

- **gate:** ≥85% house-level accuracy on the Tashkent gold set by step 3, else the cascade design is wrong
- **gate:** ≥60% house-level on a regional-centre gold set, else the product is a Tashkent-only tool and prices like one
- **gate:** one paying batch customer before building autocomplete
- can a small company obtain a contractual `UZKAD` / address-register licence, and at what tariff?
- does the official address register expose bulk export, or per-lookup only?
- ODbL derived-database boundary — confirm with a read of the licence before mixing layers
- is IT Park residency needed to invoice enterprise customers cleanly?

## 11 · Why this and not the others

- no procurement, no legal entity requirement, no tender cycle — sells to companies, not to the state
- the state is building the upstream dataset for you, on a published deadline
- it is infrastructure: one build, many verticals, recurring revenue
- it compounds into the rest of the cadastre surface — the appeal assistant, the AVM, and the
  due-diligence report all need a geocoder first
