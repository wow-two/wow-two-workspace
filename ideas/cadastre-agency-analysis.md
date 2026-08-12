# Kadastr Agency (UZ) — direction map & solution surface

*Last updated: 2026-08-09*

> **Status:** research complete, nothing built. Target = `Kadastr agentligi` under the Ministry of Economy and
> Finance (`MEF`). Two plays analysed together: **B2G** (sell to the agency) and **B2B** (build on their data).
> Verdict: their entire investment portfolio is one program — `GISTD` — and every funded line in it is
> data plumbing. The sellable work sits in layers they have neither budget nor staff for.
> Spec for the top pick: [uz-geocoder-spec.md](uz-geocoder-spec.md).
>
> **Superseded in part (2026-08-10)** by the government-wide sweep in
> [uz-govtech-demand-map.md](uz-govtech-demand-map.md). Three corrections land here — parent body,
> address-register timing, and the fact that address normalisation is already under `GISTD` procurement.
> They are marked `[corrected 2026-08-10]` inline. The §7 ranking is superseded by that document's §8.

---

## 1 · The organisation

- `Kadastr agentligi` — parent body **moved** `[corrected 2026-08-10]`: `PQ-347` (2025-11-19) created the
  `Urbanizatsiya va uy-joy bozorini barqaror rivojlantirish milliy qo'mitasi`, and `kadastr.uz` now places
  the agency under that committee. Chain: State Tax Committee (2021) → `MEF` (ПҚ-405, 2022-10-20) →
  Urbanisation & Housing Market Committee (2025-11). EEAS still wrote `MEF` in Nov 2025 — pin by date.
- June 2026 — leadership reshuffle; new director under the National Committee for Urbanisation & Housing Market
- June 2026 — corruption in the cadastre system reported as causing state losses over ~2.5 years
- call centre `1097`; State Cadastres Chamber runs a Telegram bot for defect reports
- subordinate bodies: Chamber of State Cadastres + territorial departments, `Geoinnovation Center`,
  Republican Center for Airborne Geodesy, `Kartografiya`, State Fund for Geodesy-Cartography, `Uzdavyerloyiha`

---

## 2 · Direction map

Four tracks run in parallel. Only track 1 carries donor money.

| # | Track | Driver | Horizon | Money |
|---|---|---|---|---|
| 1 | `GISTD` / UZ-NSDI | World Bank + EU | 2025–2030 | $35M + €6.6M + $5.7M |
| 2 | Service redesign | Presidential reform, 2026-08-04 | immediate | state budget |
| 3 | Mass valuation | Decree, 2025-03-05 | 2025 → 2027 | ~40bn soum |
| 4 | Registry completion | `UZKAD` mandate | **deadline end-2026** | state budget |

### Track 1 — `GISTD` (the only investment project they publish)

`gov.uz/oz/kadastr/sections/invistitsiya-loyihalari` lists **only** the `GISTD` safeguard set —
`SEP` · `ESMF` · `ESCP` · `LMP` · `WMP`. No technical annexes are published.

| Line | Funded deliverable |
|---|---|
| A.1 | NSDI architecture, data standards, data-sharing agreements |
| A.1 | **3 new data centres** (hardware + software procurement) |
| A.1 | national UZ-NSDI geoportal + **one** regional geoportal |
| A.2 | IT infra for contributing institutions; Samarkand region + municipality |
| B.1 | surveying/mapping upgrade, **80 CORS stations** |
| B.2 | **national address register** — regulation, IS, Samarkand field capture `[see correction below]` |
| B.3 | Samarkand pilots — **3D city model**, **utility cadastre** |
| C | capacity building, incl. university curriculum integration |

Agency-stated gaps, verbatim in the World Bank concept note:

- no data-sharing culture → silos and duplication
- no common standard for data specifications and services
- agencies hold data in different formats and systems
- **no sustainable business model**
- CORS network density insufficient
- data completeness and accuracy defects persist
- **local governments lack systems to manage and use geospatial data**

Stakeholders named in the `SEP` — these are the downstream customers:
`Uzsuvtaminot` (water) · `Hududgaztaminot` (gas) · Regional Electric Networks · `O'ztransgaz` ·
`O'zbekneftgaz` · `O'zbekgidroenergo` · `O'zbekiston Temir Yo'llari` · notaries ·
**individual evaluation companies** · third-party service providers.

Consultation minutes (2024-09 → 2025-03) recur on three questions: cadastre data digitisation procedure,
**inter-agency data sharing mechanisms**, and access to digital data at community level.

### Track 2 — service redesign (approved 2026-08-04)

- principle: **one application — one payment**, replacing 4–6 filings per transaction
- proactive services: application auto-generated when a right arises
- 30–50 review stages across 3 admin levels collapse to district level
- 1M+ service requests in 6 months, **~1/3 rejected**
- target: ~500k applications/year settled in seconds vs 10–15 days
- 1.2M applicants save time annually; 200k fewer applications/year
- staffing: 44% do service work, 56% supervise; 700+ vacancies; 40% off-specialty
- 30%+ of republic-level staff move to district offices; Chamber merged with service units
- `Kadastr maslahat burchagi` + `Operativ kadastr` ordered within one week
- ~90% of services already online — remaining value is **quality**, not channel

### Track 3 — mass valuation

- `National Mass Valuation Center` inside the agency, ~40bn soum
- Tashkent 2025–26 → Nukus + regional centres 2026–27 → **all regions from 2027**
- price zones per region; comparative / cost / income; benchmark-object model
- inputs: listings, transactions, build year, materials, area, floors, location, condition
- results published by cadastral number; **90-day public objection window**; then court
- purpose: pull cadastral value toward market value → property tax follows
- the state's own housing index is built by scraping **~150k `OLX.uz` listings per quarter** —
  no transaction-price registry exists

### Track 4 — registry completion

- `UZKAD` holds 42M ha (94% of land); pre-2021 only 1M ha
- 150k dwellings, 707k non-residential premises, 44k apartment buildings (Apr 2025)
- target: all **6.3M individual homes**
- **end-2026 deadline**: every object in `UZKAD` + address register on `WGS-84`
- `[corrected 2026-08-10]` that date is a decree signal, not a plan — `GISTD` ISR Seq. 3 (2026-08-07)
  targets the National Address Registry System for **June 2030**, with **$0.11M of $35.00M disbursed (0.31%)**
- `[corrected 2026-08-10]` address normalisation is **already procured** — the April-2026 `GISTD` plan
  carries 5 packages worth ~$1.8M, three open to international firms, `QCBS/01` already Under Review
- integrated with mortgage registry, `Notarius`, taxpayer registry, State Property IS, licences
- known defect: migration bound citizens' names to properties not theirs (Sept 2025)

---

## 3 · Verified technical state (probed 2026-08-09)

- `gis.kadastr.uz` ArcGIS Server — **TLS certificate SAN mismatch**; fails verified HTTPS
- `open.ngis.uz` — public geoportal on Esri ArcGIS JS `4.22` (2021 build), licence-heavy
- geoportal service layer is undocumented Tomcat: `/services/f-by-cad-num`, `/services/f-cadastral-files/`
- `api-portal.gov.uz` root returns bare `API is running` — no public developer catalog
- these agency sections render **empty**: `tanlovlar-va-tenderlar`, `interaktiv-davlat-xizmatlari`,
  `tasdiqlangan-dasturlar-va-ularning-ijrosi`, `kadastr-yo-nalishi`, `geodeziya-va-kartografiya-yo-nalishi`
- data access model: government free · private persons and companies **paid** ·
  free for all = cadastral number + address + use-purpose only
- cadastral engineers pay 1 `BRV`/month for system access

---

## 4 · Gap → solution matrix

| Gap (their words or their metric) | Solution | Track |
|---|---|---|
| local governments lack geospatial systems | municipal geodata workbench | A.2 |
| national address register unbuilt | address toolchain — dedup, conflict resolution, field capture | B.2 |
| utility cadastre pilot only | field capture app + utility-JSC rollout | B.3 |
| 33% of applications rejected | pre-filing validator | 2 |
| ownership-binding defects | reconciliation console vs `Notarius` + tax registry | 4 |
| no sustainable business model | metered API gateway over paid data | A.1 |
| four transparency sections empty | lightweight publishing CMS | — |
| no national geocoder | address normalisation + geocoding API | B2B |
| no transaction-price registry | AVM / valuer SaaS | B2B |
| 90-day objection windows, nationwide 2027 | valuation appeal assistant | B2B |

---

## 5 · B2G candidates

- **Municipal geodata workbench** → A.2. One regional geoportal is funded; 13 regions + ~200 districts are not.
  `PostGIS` + `MapLibre` undercuts Esri per-seat cost, which is the actual purchasing argument.
- **Address-register toolchain** → B.2. Dedup, conflict resolution, `WGS-84` reconciliation, mobile capture
  at 6.3M-home scale. Deadline pressure is end-2026.
- **Utility cadastre capture app** → B.3. Three utility JSCs already sit in the stakeholder list.
- **Rejection-prevention pre-check** → track 2. Their 33% reject rate is the published KPI.
- **Data-quality reconciliation console** → track 4. Surfaces ownership conflicts across integrated registries.
- **Open-data / API publishing layer** → A.1 + the business-model gap. Turns paid access into a revenue line.
- **Transparency-section CMS** → cheap door-opener against four mandated-but-empty sections.

Entry routes: `xarid.uzex.uz` · `etender.uzex.uz` · request-for-proposals procurement type live since 2026-01-01
(УП-259, 2025-12-26). World Bank lines go to international competitive bidding — realistic route for a small
team is **subcontracting the prime**, not bidding the program.

---

## 6 · B2B candidates

- **UZ geocoding + address normalisation API** — the missing national primitive; banks, utilities, insurers,
  couriers, marketplaces all need it. Spec: [uz-geocoder-spec.md](uz-geocoder-spec.md)
- **AVM / valuer SaaS** — "individual evaluation companies" are named GISTD stakeholders
- **Mass-valuation appeal assistant** — fixed 90-day windows, cadastral-number lookup, evidence pack
- **Property due-diligence report** — encumbrances + restrictions; 171k transactions per half-year
- **Developer site-screening map** — zoning, use-purpose, ownership overlays for land acquisition

Market pull: Q1-2026 110.1k transactions (+48.4% YoY) · H1-2026 171k+ (+25.3%) ·
Tashkent new-build prices +5% YoY · `uybor.uz` incumbent at ~$7M revenue on a small team.

---

## 7 · Ranking

| # | Build | Play | Procurement needed | Blocker |
|---|---|---|---|---|
| 1 | Address/geocoding API | B2B | no | dataset licence |
| 2 | Rejection pre-check | B2G-adjacent | no | reject-reason taxonomy |
| 3 | Valuation appeal assistant | B2B | no | valuation-result feed |
| 4 | Municipal geodata workbench | B2G | yes | legal entity + prime |
| 5 | Utility cadastre field app | B2G | yes | subcontract to GISTD winner |

Fastest credible contact: report the `gis.kadastr.uz` TLS defect through official channels, attach a one-page
geoportal proposal. Costs nothing, proves competence, bypasses the cold-outreach problem.

---

## 8 · Open questions — verify before committing

- can a small company obtain a contractual `UZKAD` data licence, and at what tariff?
- is IT Park residency required to contract with the agency?
- does an official API catalog exist behind `api-portal.gov.uz` auth?
- are mass-valuation results published in bulk, or only per-cadastral-number lookup?
- who won / will win the `GISTD` system-integration lots?

---

## 9 · Sources

- [Spot — cadastre reform, 2026-08-04](https://www.spot.uz/ru/2026/08/04/cadastre-reforms)
- [Sputnik — one application, one payment](https://uz.sputniknews.ru/20260805/agentstvo-po-kadastru-uzbekistana-izmenit-printsip-raboty-59493733.html)
- [president.uz — cadastre plans review](https://president.uz/ru/lists/view/8091)
- [World Bank GISTD PID (P506803)](https://documents1.worldbank.org/curated/en/099073024220030738/pdf/P50680319f2c730a190df141d1feca8814.pdf)
- [GISTD Stakeholder Engagement Plan (March 2025)](https://api-portal.gov.uz/uploads/184/2025/04/01/f8623dae-4b14-7816-bf68-7a4776645ab5_media_13099.pdf)
- [Cadastre Agency — investment projects](https://gov.uz/oz/kadastr/sections/invistitsiya-loyihalari)
- [EEAS — NSDI national forum](https://www.eeas.europa.eu/delegations/uzbekistan/national-forum-advances-geospatial-data-sustainable-territorial-development-uzbekistan_en)
- [Spot — mass valuation methodology](https://www.spot.uz/ru/2026/06/26/real-estate-valuation)
- [Gazeta — mass appraisal decree](https://www.gazeta.uz/ru/2025/03/06/mass-appraisal/)
- [Norma — open-data geoportal, access tariffs](https://www.norma.uz/novoe_v_zakonodatelstve/do_konca_goda_budet_zapushchen_geoportal_otkrytyh_dannyh)
- [Kursiv — H1-2026 transaction volume](https://uz.kursiv.media/2026-08-02/prodazhi-zhilya-v-uzbekistane-vzleteli-na-253-za-god-czeir/)
- [Zamin — cadastre corruption](https://zamin.uz/jamiyat/205816-ozbekiston-kadastr-tizimidagi-korruptsiya-davlatga-millionlab-zarar-keltirdi.html)
- [Gazeta — xarid.uzex.uz procurement](https://www.gazeta.uz/ru/2026/05/07/xarid-uzex-uz/)
