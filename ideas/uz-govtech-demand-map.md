# UZ government-wide demand map — where our products have pull

*Last updated: 2026-08-10*

> **Status:** research output, nothing built. Produced by a 40-agent sweep across 12 ministry/agency clusters
> on 2026-08-10. Companion to [cadastre-agency-analysis.md](cadastre-agency-analysis.md) and
> [uz-geocoder-spec.md](uz-geocoder-spec.md).
>
> **Read the confidence math before you act on any row.** 206 demand signals were extracted; 82 rated
> `strong`; **14 were adversarially verified and 9 of those were refuted** — a 64% kill rate on the tier
> that was supposed to be the most solid. The 68 unverified `strong` signals and all 97 `medium` signals
> should be assumed to carry a similar error rate until individually checked. §1.1 is the only table that
> survived refutation. Everything below it is a lead, not a fact.
>
> Product codes used throughout: `P1` geocoder · `P2` addr-toolchain · `P3` registry-integration ·
> `P4` gis-portal · `P5` valuation · `P6` service-quality/pre-check · `P7` field-capture · `P8` open-data-api.

---

## 1 Cross-government demand map

### 1.1 Confirmed signals (primary text fetched, high/medium confidence)

| Ministry / body | Need | Fit | Urgency driver | Buyer | Tender |
|---|---|---|---|---|---|
| Urbanization Center (`Urbanizatsiya markazi`) | Vectorise + QA master plans for 7,560 settlements | `P4` `P2` `P3` | `PF-104` auto-issuance starts `2026-09-01`; only 12% of settlements digitised ([lex.uz/-8245267](https://lex.uz/docs/-8245267)) | ministry | yes |
| Urbanization Center / `O'zshaharsozlikLITI` | CAD/paper → GIS vector conversion, topology validation, registry serving | `P4` `P7` `P3` | `PQ-252` (07.07.2026): 138 bn UZS, unified plan registry from `2026-11-01`, permits blocked without registry number from `2026-10-01` ([lex.uz/-6600549](https://www.lex.uz/uz/docs/-6600549)) | ministry | yes |
| `Uzsuvtaminot` / `Hududgazta'minot` / `Hududiy elektr tarmoqlari` | Cross-utility GIS normalisation: loads, reserve capacity, connection points | `P4` `P7` `P8` | `PF-104` §4(b): Tashkent end-2026, regions end-2027 ([lex.uz/-8245267](https://lex.uz/docs/-8245267)) | soe | yes |
| `Uzsuvtaminot` JSC | Field capture + geo-mapping of ~75-80k km pipelines, ~4M connections | `P7` `P4` `P1` | ADB `54272-001` Loan `4582-UZB` $125M, 3 QCBS packages $27.68M advertised Q4/2026 ([adb.org](https://www.adb.org/news/adb-supports-digital-transformation-uzbekistan-s-water-sector)) | soe | yes |
| Construction & Housing Inspection | Permit application pre-check feeding AI screening | `P6` `P3` | `PF-104`: AI analysis of permit applications phased from `2026-09-01`, `2 barobargacha` cost-cut target ([lex.uz/-8245267](https://lex.uz/docs/-8245267)) | ministry | yes |

### 1.2 Medium signals (verified source, dependency partly inferred)

Sorted by deadline proximity.

| Ministry / body | Need | Fit | Urgency driver | Buyer | Tender |
|---|---|---|---|---|---|
| Category I/II industrial enterprises | Station→centre integration adapter + data-quality gate | `P3` `P7` `P4` | `PQ-343` §7: `2026-03-01` lapsed, compensation payments at **5x** ([lex.uz/-7847341](https://lex.uz/uz/docs/-7847341)) | private | **no** |
| TPPs + Tashkent industrial sites | Emission telemetry → Committee geoinformation DB | `P3` `P4` | `PF-46` §7v: `2026-05-01` lapsed, compensation at **10x** ([lex.uz/-8101201](https://lex.uz/uz/docs/-8101201?ONDATE=30.03.2026+01)) | soe | **no** |
| Tax advisors / property-heavy corporates | 5-day pre-check + appeal pack for auto-generated assessments | `P6` `P5` | Auto-assessment live `2026-01-01`, silence = acceptance ([gazeta.uz](https://www.gazeta.uz/ru/2026/01/13/property-tax/)) | private | **no** |
| Ecology Committee | Unified Ecological Online Platform: aggregate + publish | `P8` `P3` | `PQ-343`: `2026-09-01`, 22 days out, no platform URL findable ([lex.uz/-7847341](https://lex.uz/uz/docs/-7847341)) | ministry | yes |
| Association of Mahallas + Cadastre Agency | Approve ~10,000 mahalla boundary polygons from cadastral docs | `P4` `P2` `P3` | `PF-116` item 32: July 2026 — **lapsed** ([lex.uz/-8286512](https://lex.uz/uz/docs/-8286512)) | agency | yes |
| Cadastre Agency | Re-inventory mahallas, mint new cadastral numbers in `UzKAD` | `P2` `P3` `P1` | `PF-116` item 34: `UzKAD` amendments due August 2026 — this month | agency | yes |
| Association of Mahallas + MinDigital | Wire 35 named agency systems into `Raqamli mahalla` | `P3` `P8` `P1` | `PF-116` Art. 7(a) + Annex 4: `2026-11-01` | agency | yes |
| Association of Mahallas | Red/yellow/green scoring of every mahalla on 7 indicators | `P4` `P3` | `PF-116` Art. 7(v); quarterly re-scoring after `2026-11-01` | agency | yes |
| Association of Mahallas | Door-to-door household problem capture by the `mahalla yettiligi` | `P7` `P1` `P3` | `PF-116` item 39.3: Sept–Nov 2026 window | agency | yes |
| Ecology Committee + MIA | Tashkent red/yellow/green transport zones + sticker registry | `P1` `P4` | `PF-46` §18–19: both due `2026-12-31` | ministry | yes |
| MIA — Migration & Personalisation | Address normalisation inside the unified migration platform | `P1` `P2` `P3` | Platform due `2026-12-31`; `ZRU-1074` never names the address register ([yuz.uz](https://yuz.uz/uz/news/137656)) | ministry | yes |
| NASP | 25 social services devolve to mahalla, incl. housing adaptation | `P1` `P3` `P7` | All 25 at mahalla level by `2026-12-31` ([gazeta.uz](https://www.gazeta.uz/ru/2026/07/17/social-protection/)) | agency | yes |
| MinDigital — OASIS | Shared address-normalisation service inside the re-platform | `P1` `P3` `P8` | OASIS due `2026-12-01`; 200 DBs, 1,000+ services ([yuz.uz](https://yuz.uz/uz/news/mamlakatda-raqamli-texnologiyalar-joriy-etilishini-yanada-jadallashtirish-chora-tadbirlari-belgilandi)) | ministry | yes |
| Bureau of Compulsory Enforcement | Property identity resolution behind automated executor decisions | `P1` `P3` `P5` | `UP-50`: 70% of decisions automated by `2027-01-01`; decree never names cadastre or address ([lex.uz/8108876](https://lex.uz/ru/docs/8108876)) | agency | yes |
| Ministry of Justice — `NOTARIUS` | Bind deeds to the address register, not free-text strings | `P1` `P3` | `PQ-280`: auto-update to 5 consuming registries live since `2026-04-01` ([lex.uz/-7722035](https://lex.uz/docs/-7722035)) | ministry | yes |
| Ministry of Water Resources | State Water Cadastre ↔ Cadastre Agency reconciliation layer | `P3` `P8` `P4` | Stated April 2026 launch, unconfirmed 4 months on ([spot.uz](https://www.spot.uz/ru/2025/10/13/water-management/)) | ministry | yes |
| MoWR + MoAgriculture | Quota computation off a crop layer with proven defect rate | `P3` `P8` | `Suv hisobi` ↔ `Digital Agriculture` integration being wired now ([gazeta.uz](https://www.gazeta.uz/ru/2025/10/17/wate/)) | ministry | yes |
| MoWR (`PP-250`) | Spatial asset register under 300 devices, 12,080 wells, 1,750 pumps | `P7` `P4` `P8` | Programme 2025-2028, mid-installation ([norma.uz](https://www.norma.uz/novoe_v_zakonodatelstve/upravlenie_vodnymi_resursami_perevoditsya_na_cifrovuyu_osnovu)) | ministry | yes |
| Cadastre Agency (agri land) | Geometry reconciliation on 159,000 ha of area divergence | `P2` `P3` `P7` | `UZKAD` all-objects deadline end-2026; aerophoto survey ~20 months overdue ([gazeta.uz](https://www.gazeta.uz/ru/2023/11/22/cadastre/)) | agency | yes |
| Cadastre Agency — `E-yer nazorat` | Caseload handling for 100k+ annual detections | `P6` `P3` `P7` | Exclusive channel since `2026-01-01`; operator funded by 2% of penalties ([buxgalter.uz](https://buxgalter.uz/oz/publish/doc/text210654_er_uchastkalari_buyicha_yangi_tizim_-_e-yer_nazorat_nima_uchun_yaratilmoqda)) | agency | yes |
| `Uzbekcosmos` | Coordinate→registry matching + queryable surface for detections | `P1` `P8` `P3` | `Samarkand-2028` live Aug 2026 raises detection volume ([gov.uz](https://gov.uz/en/uzspace/news/view/70563)) | agency | yes |
| MoAgriculture + Cadastre Agency | Master-data layer across 3 parallel spatial pictures | `P3` `P4` `P2` | `E-yer nazorat` forces all three into one workflow ([gov.uz](https://gov.uz/oz/agro/pages/geoaxborot-tizimi)) | ministry | yes |
| Ministry of Emergency Situations | Mahalla risk scoring: capture app + polygon layer + roster | `P7` `P1` `P4` | `PP-310` pilot ends ~`2027-01-01`; nationwide proposals `2027-04-01` ([lex.uz/7776340](https://lex.uz/uz/docs/7776340)) | ministry | yes |
| Ministry of Emergency Situations | Ingestion + reconciliation across all agencies' emergency systems | `P3` `P8` | `PP-311`: unified platform `2027-12-01`, only 60% digitisation targeted ([nrm.uz](https://nrm.uz/contentf?doc=791690_postanovlenie_prezidenta_respubliki_uzbekistan_ot_20_10_2025_g_n_pp-311)) | ministry | yes |
| `Uzhydromet` | API / export layer over 26 cities, 66 posts, 28 auto stations | `P8` `P3` | Feeds the `2026-09-01` publishing deadline; no API, no licence ([monitoring.meteo.uz](https://monitoring.meteo.uz/ru/map)) | agency | yes |
| `Uzhydromet` + UNDP/GCF | Geotargeted alerting needs authoritative polygons + address resolution | `P1` `P4` | GCF $9.9M + $30.6M co-fin, closes 2027 ([undp](https://www.adaptation-undp.org/GCF-Uzkekistan)) | donor | yes |
| `REPN` (Hududiy elektr tarmoqlari) | Meter→premise→feeder binding for 150,000 smart meters | `P1` `P2` `P3` | $100M WB + $50M co-fin, results by 2029; no GIS component named ([gazeta.uz](https://www.gazeta.uz/en/2025/05/19/world-bank/)) | soe | yes |
| Ministry of Energy | Mahalla-level balances need boundaries + addressed consumers | `P1` `P2` `P7` `P3` | Draft decree due ~Oct 2026; 13-district expansion is the scoping window ([sputniknews](https://uz.sputniknews.ru/20260807/cifrovizatsiya-kontrol-uzbekistan-novaya-sistema-upravleniya-energetika-59537958.html)) | ministry | yes |
| `Hududgaztaminot` | Meter ↔ premise ↔ taxpayer three-registry join for 129,500 meters | `P1` `P3` | 188 bn som sector debt; 5,000+ meters not transmitting ([gazeta.uz](https://www.gazeta.uz/ru/2023/05/16/gas-movement-system/)) | soe | yes |
| Ministry of Energy / `Uzenerginspection` | Consumption ↔ tax registry reconciliation | `P3` | 48 zero-income firms, 871,000 kWh — found by hand ([nuz.uz](https://nuz.uz/2026/07/27/oshibki-na-milliony-dollarov-prezident-potreboval-reformirovat-energosistemu-uzbekistana/)) | ministry | yes |
| Ministry of Mining & Geology | Georeference 36,000+ reports, legacy datum → WGS-84 | `P2` `P4` `P8` | National Geological Database still at proposal stage; $30bn programme to 2030 ([uza.uz](https://uza.uz/en/posts/measures-to-widely-implement-digital-technologies-in-the-mining-and-geology-industries-reviewed_868686)) | ministry | yes |
| Ministry of Preschool & School Education | Geocoder behind first-grade micro-district assignment | `P1` `P2` `P6` | Annual intake `2026-06-20` / `2026-08-01`; build window is winter 2026 ([dgov.uz](https://dgov.uz/ru/solution/detail/33/)) | ministry | yes |
| MPSE — WB `BILIM` `P513205` | School-level geospatial layer for siting 27,000 seats | `P4` `P3` `P1` | $378M, approved `2026-06-30`, runs to 2030 ([worldbank.org](https://www.worldbank.org/en/news/press-release/2026/06/30/uzbekistan-to-improve-the-quality-of-primary-education-for-2-million-children-and-future-jobs-access)) | ministry | yes |
| MoEF — WB `EduImkon` | Cross-registry means-testing + beneficiary tracking | `P3` `P8` `P6` | $250M, 2026-2028, platform is an early deliverable ([worldbank.org](https://www.worldbank.org/en/news/press-release/2025/12/11/modernized-student-financing-system-to-expand-access-to-education-for-600000-young-people-in-uzbekistan)) | ministry | yes |
| Statistics Committee | Custody + crosswalk for 7.6M geolocated households | `P1` `P2` `P3` `P7` | Final census results `2027-07-01`; custody undecided now ([president.uz](https://president.uz/ru/lists/view/8863)) | agency | yes |
| Statistics Committee — WB `P173450` | Operate-and-maintain GIS capability; staffing package unfilled | `P4` `P7` `P2` | `SSS/C2.4/IC/27` $100k still `Pending Implementation`, plan period expired Dec-2025 ([WB proc. plan](https://documents1.worldbank.org/curated/en/099121025005036382/txt/P173450-9c20ba35-288a-479d-bc00-9b8ab51f73eb.txt)) | donor | yes |
| Tax Committee | Data-quality gate under auto-generated property/land assessments | `P3` `P6` `P2` | Live since `2026-01-01`, five days to correct ([gazeta.uz](https://www.gazeta.uz/ru/2026/01/13/property-tax/)) | agency | yes |
| Tax Committee — VAT refund | Application pre-check | `P6` | 46.4% rejected in 2024 (9,296 of 20,014) — computed from ISR `P173001` ([WB ISR](https://documents1.worldbank.org/curated/en/099061325101540967/pdf/P173001-0fa2abd7-22af-42cc-ad6d-5d844d19092f.pdf)) | agency | yes |
| Cadastre + Tax + Statistics | Crosswalk across 3 unreconciled address geographies | `P1` `P2` `P3` | Auto-assessment turns each mismatch into a dated liability ([lex.uz/4104736](https://lex.uz/docs/4104736)) | agency | yes |
| Statistics — business register | Deduplicated, geocoded establishment addresses for a survey frame | `P1` `P2` `P3` | `P173450` $50M IDA; business census still ahead ([WB PID](https://documents1.worldbank.org/curated/en/622421593166067410/pdf/Concept-Project-Information-Document-PID-Strengthening-the-Statistical-System-of-Uzbekistan-P173450.pdf)) | agency | yes |
| NASP — WB `INSON` `P504420` | Geocode `UNSP` records to report the climate-risk PDO indicator | `P1` `P3` `P4` | $100M IDA + $2M MDTF, runs to 2029 ([PAD](https://documents1.worldbank.org/curated/en/099050724162539809/pdf/BOSIB-14cafc8d-4e42-4b6e-a6b5-096b834eb119.pdf)) | donor | yes |
| NASP | Household↔dwelling key for 5,000 social workers' social passports | `P7` `P1` `P2` | `INSON` sub 1.1 $5M tooling; enumeration already running ([reestr.uz/1967](https://reestr.uz/ru/projects/1967?type=passport)) | agency | yes |
| NASP | Social Register application pre-check | `P6` `P3` | 184 mahallas rejected 2,000 of 2,000 in one month ([gazeta.uz](https://www.gazeta.uz/ru/2026/07/17/social-protection/)) | agency | yes |
| Three utility JSCs | Address→mahalla resolution on millions of accounts | `P1` `P3` | `PF-116` Annex 4 items 33-35: `2026-11-01` | soe | **no** |
| Association of Mahallas + Cadastre | Duplicate mahalla-name resolution + permanent registry module | `P1` `P2` | `PF-116` item 33: July 2026 lapsed; maintenance is `Doimiy` | agency | yes |
| State Assets Agency / `e-auksion` | Geolocation + coordinate capture and validation at auction intake | `P1` `P2` `P7` | `PP-5197` §8 gate codified since 2021; Res. 559 re-asserts it unsolved ([lex.uz/5525729](https://lex.uz/ru/docs/5525729)) | agency | yes |
| Cadastre Agency — `Yerelektron` | Pre-check at auction submission | `P6` `P2` `P1` | ~40% of 90,001 plots never cleared the pipeline (rate derived by us) ([kadastr.uz](https://kadastr.uz/uz/news/Tadbirkorlik%20faoliyatini%20amalga%20oshirish%20uchun%20yer%20uchastkalarini%20auksion%20savdolariga%20chiqarish%20bo%E2%80%98yicha%202022-yil%20davomida%2090%20001%20ta%205%20741,1%20gektar%20maydondagi%20yer%20uchastkalari%20%E2%80%9CYerelektron%E2%80%9D%20tizimiga%20kiritildi)) | agency | yes |
| MPAE + MIIT + SAMA + Cadastre | Cross-registry reconciliation across 4 ordered integrations | `P3` `P6` | Res. 559 integrations due ~Dec 2025 — 8 months overdue ([lex.uz/-7712688](https://www.lex.uz/uz/docs/-7712688)) | agency | yes |
| MoEF — WB `P508451` | Municipal geospatial tooling; coded theme line | `P4` `P3` `P8` | $250M, closes `2031-02-15`; `DLI 4` = $16M GIS asset inventory ([worldbank.org](https://projects.worldbank.org/en/projects-operations/project-detail/P508451)) | donor | yes |
| State Cadastre Chamber + MoA + MoWR | Assemble cadastral maps with coordinate points per auction lot | `P2` `P3` `P7` | Res. 223 3-day SLA per step; 423,586 lease agreements flowing ([lex.uz/-6892013](https://lex.uz/docs/-6892013)) | agency | yes |
| Cultural Heritage Agency | Object passports, 3D/360 capture, integration to Cadastre National GIS | `P3` `P7` `P4` | `reestr.uz` 2826 says system does not exist; IoT target 50 objects by 2026 ([reestr.uz/2826](https://reestr.uz/projects/2826?type=passport)) | agency | yes |
| Heritage Agency + Cadastre | Protection-zone geometry layer for statutory land-plot checks | `P2` `P3` `P4` | Digitisation mandate 2021-2023 unmet; 8,437 objects as of `2026-05-12` ([lex.uz/-5320217](https://lex.uz/docs/-5320217)) | agency | yes |
| Tourism Committee | National Tourism Platform + coordinates on 3 registers | `P1` `P4` `P8` | `PQ-348` date `2026-07-01` passed, non-launch inferred not confirmed ([lex.uz/-7851788](https://lex.uz/docs/-7851788)) | agency | yes |
| MIIT — SEZ/FEZ | Zone parcel inventory to feed the `PP-5197` auction gate | `P2` `P4` `P7` `P1` | Land tax on zone directorates from `2028-01-01` ([lex.uz/-7420262](https://lex.uz/uz/docs/-7420262)) | ministry | yes |
| Insurance Market Development Agency | Geocoded property exposure for catastrophe accumulation | `P1` `P4` `P7` | WB `P173619` sub-2.2 $1.5M; project closes `2027-06-30` ([WB PAD](https://documents1.worldbank.org/curated/en/341821651843155856/pdf/Uzbekistan-Financial-Sector-Reform-Project.pdf)) | agency | yes |
| EDC / MoEF — `FINGROW` `P511700` | Registry auto-fetch + error-free application assembly | `P6` `P3` | $600M operation approved `2025-12-18`; $3M TA component ([WB PAD](https://documents1.worldbank.org/curated/en/099111125164834893/pdf/P511700-4c30f714-7fff-495b-8330-6bf575847bf5.pdf)) | soe | yes |
| Central Bank — SupTech | Structured supervisory reporting to replace email intake | `P3` `P8` | FSAP 2025 grades BCP 10 `Materially Non-Compliant`; phase 2 in vendor selection — source truncated in input | agency | yes |

---

## 2 Where P1 (geocoder) is load-bearing

Each entry names the specific thing that breaks, not "data quality".

### `NOTARIUS` → five consuming registries
- Deed binds to cadastral number + a **free-text address string the notary types**.
- On ownership change, `PQ-280` auto-updates Cadastre, Energy, Construction, Ecology, Tax, `Uzsuvtaminot`.
- Mismatched string → the automatic update lands on the wrong object or fails silently in all five at once.
- Live since `2026-04-01`; every bad string written since then compounds. [lex.uz/-7722035](https://lex.uz/docs/-7722035)

### Bureau of Compulsory Enforcement
- `UP-50` requires 70% of executor decisions automated by `2027-01-01`.
- Core business is seizure, arrest and auction of immovable property.
- Decree contains **no** mention of cadastre, address register, geolocation or mapping.
- Failure mode: an arrest order automated against an unnormalised property description hits the wrong dwelling. [lex.uz/8108876](https://lex.uz/ru/docs/8108876)

### MIA — residence registration
- `ZRU-1074` moved registration to **notification-based, self-declared**.
- Registered address stored in MIA's own `Pasport-viza` DB, parallel to the cadastre's register.
- No normalisation → MIA's store and `UZKAD` diverge at national scale, with nothing forcing reconciliation. [yuz.uz](https://yuz.uz/uz/news/137656)

### `Hududgaztaminot` — 129,500 household meters
- Meter must join to premise address **and** to a taxpayer record for automatic e-invoicing.
- Three-registry join with no named component performing it.
- Failure mode: invoices generated against identities nobody reconciled; 188 bn som sector debt already booked. [gazeta.uz](https://www.gazeta.uz/ru/2023/05/16/gas-movement-system/)

### `REPN` — 150,000 smart meters
- No GIS or meter-to-premise matching named anywhere in the $150M programme.
- Without it each meter is a serial number with no verified customer, premise or feeder.
- Precedent: 5,000+ gas meters in the previous generation still not transmitting. [gazeta.uz](https://www.gazeta.uz/en/2025/05/19/world-bank/)

### Three utility JSCs → `Raqamli mahalla`
- `PF-116` Annex 4 items 33-35 require integration by `2026-11-01`.
- Utility customer bases are keyed by **service-address strings**, not PINFL and not mahalla.
- Address→mahalla resolution on millions of accounts is the whole job. [lex.uz/-8286512](https://lex.uz/uz/docs/-8286512)

### First-grade school admission
- `my.maktab.uz` assigns a school from the child's permanent registration address inside a closed micro-district.
- Documented functionality names no map, no coordinates, no distance calculation — points to a hand-maintained address→micro-district table.
- Failure mode: unmatched address drops the family into a manual quota-bound transfer procedure, decided in 3 working days, ~100k new entrants a year. [dgov.uz](https://dgov.uz/ru/solution/detail/33/)

### NASP — 25 devolved services
- `Housing adaptation for disability` and `social-housing placement` are dwelling-specific.
- `UNSP` records carry `PINFL` only — a person key.
- Failure mode: a dwelling-scoped service cannot be queued, catchment-assigned or audited against a person-only registry. [gazeta.uz](https://www.gazeta.uz/ru/2026/07/17/social-protection/)

### WB `INSON` PDO indicator
- Indicator: share of people in **climate-risk areas** registered in `UNSP`.
- Requires resolving PINFL-keyed records to coordinates and intersecting hazard zones.
- No geocoding capability described anywhere in the project → the headline indicator is unreportable as designed. [PAD](https://documents1.worldbank.org/curated/en/099050724162539809/pdf/BOSIB-14cafc8d-4e42-4b6e-a6b5-096b834eb119.pdf)

### `Uzbekcosmos` → enforcement registries
- 100,000+ annual detections are coordinate-native (footprints, quarries, dumps, burn scars).
- Receiving registries are address-based.
- Failure mode: a detection cannot be attributed to an owner or object without coordinate→address→registry matching. `Samarkand-2028` raises volume from Aug 2026. [gov.uz](https://gov.uz/en/uzspace/news/view/70563)

### Ecology transport zoning (Tashkent)
- `PF-46` §18-19: zones plus a vehicle sticker registry, both due `2026-12-31`, two agencies.
- A zone boundary that does not resolve to buildings and street segments cannot be enforced against a vehicle at a location. [lex.uz/-8101201](https://lex.uz/uz/docs/-8101201?ONDATE=30.03.2026+01)

### Tax auto-assessment
- Six taxes auto-generated since `2026-01-01`; five days to correct, silence accepts.
- Assessment rests on object area, location, category, ownership held in registers the Tax Committee does not own.
- Failure mode: every unreconciled address becomes a binding liability on day six. [gazeta.uz](https://www.gazeta.uz/ru/2026/01/13/property-tax/)

### Statistics — 7.6M census household geolocations
- Largest live household point layer in government, fresher than anything the Cadastre Agency publishes.
- No crosswalk to the Unified Register of Addresses or the `GISTD` national register.
- Failure mode: a one-shot asset that decays between censuses and cannot join to tax or cadastre objects. [president.uz](https://president.uz/ru/lists/view/8863)

### Ministry of Energy — mahalla balances
- Model organises supply `в разрезе районов и махаллей` with an `адресный подход`.
- A mahalla-level energy balance is arithmetically impossible without mahalla boundaries and addressed consumers.
- Neither is named as an input; no source states the national address register will supply them. [sputniknews](https://uz.sputniknews.ru/20260807/cifrovizatsiya-kontrol-uzbekistan-novaya-sistema-upravleniya-energetika-59537958.html)

### `e-auksion` land plots
- `PP-5197` §8: application without photographs, geolocation and coordinates is **returned**.
- ~40% of 90,001 plots never cleared the pipeline (rate derived by us from Cadastre Agency 2022 figures).
- Failure mode: unsold hectares and forgone state revenue at intake, not at auction. [lex.uz/5525729](https://lex.uz/ru/docs/5525729)

---

## 3 Adjacent product pull

Count = distinct organisations with an independently-sourced need.

| Product | Bodies | Who |
|---|---|---|
| `P3` registry-integ | ~24 | MinDigital `OASIS` · MoWR water cadastre · MoA↔Cadastre · Tax · Enforcement Bureau · MoJ notariat · MIA migration · MoES `PP-311` · Ecology telemetry (5x/10x penalty buyers) · `Raqamli mahalla` 35-agency wiring · NASP · Res. 559 four-system integration · CBU SupTech · `FINGROW` |
| `P4` gis-portal | ~18 | Urbanization Center · three utility JSCs · `Uzsuvtaminot` · WB `P508451` `DLI 4` · mahalla scoring · MoES risk zones · Ecology geoinformation DB · Mining · `BILIM` school siting · Heritage zones · IMDA exposure |
| `P1` geocoder | ~16 | see §2 |
| `P7` field-capture | ~11 | `Uzsuvtaminot` ($27.68M in named packages) · `mahalla yettiligi` door-to-door · NASP social passports · MoES on-site mahalla studies · `PP-250` device siting · agri geometry · Heritage 3D/360 · SEZ parcel inventory |
| `P8` open-data-api | ~9 | `Uzhydromet` (no API at all) · Ecology platform `2026-09-01` · `Uzbekcosmos` · MoWR · Mining · MoES · `Raqamli mahalla` · `EduImkon` · CBU |
| `P6` svc-quality | ~8 | Construction Inspection AI screening · VAT refund 46.4% · NASP 2,000/2,000 · `Yerelektron` ~40% · Tax 5-day window · `FINGROW` · school admission · `E-yer nazorat` caseload |
| `P2` addr-toolchain | ~12 | mostly co-sold with `P1`; standalone pull from mahalla re-inventory, agri 159,000 ha, Mining 36,000 reports, Statistics business register |
| `P5` valuation | 2 | Enforcement Bureau (auction sale) · tax-advisor appeal packs. Weakest pull in the set. |

- `P3` is the real centre of gravity, not `P1` — every deadline in 2026-2027 is an integration deadline.
- `P1` is load-bearing *under* `P3`: the joins that `P3` must perform are address joins in ~16 of 24 cases.
- `P5` collapsed under scrutiny — no funded mass-valuation buyer surfaced outside the Tashkent pilot in the baseline.
- `P6` has the only two **tender-free** buyers in the whole map (tax advisors, penalised enterprises).

---

## 4 The five biggest single opportunities

### 4.1 `Uzsuvtaminot` GIS/AMS field capture — ADB `54272-001`

- Body: `Uzsuvtaminot` JSC, executing agency; ADB Loan `4582-UZB`.
- Need: geo-referenced asset inventory across 15-16 of 17 suvtaminots — ~75-80,500 km pipelines, ~4M customer connections.
- Money: three QCBS packages `CSWMP-CS-02/03/04` = **$9,212,027 + $7,538,881 + $10,933,263 = $27.68M**; separate SI package `CSWMP-IT-01` $25.21M.
- Deadline: advertised Q4/2026 per the 13-May-2026 procurement plan; none awarded; realistic award mid-2027 after a ~12-month slip.
- Build: mobile field-capture app for pipeline and connection survey, coordinate QA, deduplication, and the ingest pipeline into the AMS/GIS.
- Why we win: international advertising, 70:30 quality-cost, no domestic preference, no prequalification. Entry is JV or sub-consultant to an international prime — our slice is exactly the capture tooling and data QA the prime does not want to build. [adb.org](https://www.adb.org/news/adb-supports-digital-transformation-uzbekistan-s-water-sector)
- Risk: prime selection rewards firm-level survey track record we do not have. Sub-consultant only.

### 4.2 Master-plan vectorisation for the Urbanization Center

- Body: `Urbanizatsiya va shaharsozlik hujjatlarini ishlab chiqish respublika markazi` — GIS administrator under `PQ-252`.
- Need: 1,462 existing plans to convert, 6,098 settlements with no plan; machine-readable zoning geometry per settlement.
- Money: **138 bn UZS** allocated by `PQ-252` (07.07.2026).
- Deadlines: `PF-104` automatic `ASHT` issuance from `2026-09-01`; unified electronic master-plan registry from `2026-11-01`; permits blocked without a registry number from `2026-10-01`.
- Build: CAD/raster→GIS vectorisation pipeline, zoning-geometry topology validation, WGS-84 reconciliation against cadastre, registry serving API. `CM-85` (12.02.2025) permits **licensed private specialised organisations** to supply topographic data.
- Why we win: 88% of the country falls back to manual issuance on day one of a presidentially-announced automation; the content gap is structural, not a backlog — pipeline of 154+144 plans lifts coverage only to ~32.5% by end-2027. [lex.uz/-8245267](https://lex.uz/docs/-8245267) · [lex.uz/-6600549](https://www.lex.uz/uz/docs/-6600549)
- Risk, and it is the weakest link: neither decree contains a PPP or procurement clause. Commercial channel is **unverified**. A named in-house state centre owns mandate and budget; we enter as subcontractor or not at all.

### 4.3 Emission-telemetry integration adapters — the penalty-priced buyers

- Bodies: Category I/II industrial enterprises (`PQ-343`); TPPs and Tashkent industrial sites (`PF-46`).
- Need: station→centre and stack→geoinformation-DB integration, common schema, spatial join from source to owning enterprise/parcel.
- Money: not a budget line — a **penalty multiplier**. `PQ-343` §7 applies compensation payments at **5x** for non-integration; `PF-46` §7v applies **10x**.
- Deadlines: both **already lapsed** — `2026-03-01` and `2026-05-01`. Exposure is accruing monthly right now.
- Build: telemetry ingestion adapter + data-quality gate + spatial join to enterprise/parcel. We sell integration, not sensors.
- Why we win: **the only procurement-free buyers at scale in the map.** An enterprise or SOE buys this as ordinary capex against a priced penalty. The ROI arithmetic is written into the decree. `PF-46` also references JICA $100M and EBRD $200M industrial-modernisation loans, so capex capacity exists. [lex.uz/-7847341](https://lex.uz/uz/docs/-7847341) · [lex.uz/-8101201](https://lex.uz/uz/docs/-8101201?ONDATE=30.03.2026+01)

### 4.4 `Raqamli mahalla` — address→mahalla resolution across 35 agencies

- Bodies: Association of Mahallas + MinDigital + Cadastre Agency; 35 named systems in `PF-116` Annex 4.
- Need: mahalla boundary polygons (~10,000), new mahalla cadastral numbers in `UzKAD`, duplicate-name resolution, address→mahalla resolver, door-to-door capture tooling, 7-indicator scoring.
- Money: not stated in the decree — **source not captured** for a budget figure.
- Deadlines, all clustered: boundaries July 2026 (**lapsed**) · `UzKAD` code changes August 2026 (**this month**) · integration list July 2026 (lapsed) · platform `2026-11-01` · household capture Sept-Nov 2026.
- Build: boundary approval workbench, address→mahalla resolver as a service, mobile capture for the `mahalla yettiligi`, scoring/render layer.
- Why we win: `PF-116` item 34 confirms from primary text that the **cadastral number is being made the mahalla join key** — that is our seam, and the three utility JSCs on the same deadline are keyed by address strings that nothing resolves. Multiple lapsed deadlines with a hard `2026-11-01` behind them is the classic buy-don't-build moment. [lex.uz/-8286512](https://lex.uz/uz/docs/-8286512)
- Risk: no procurement seam visible; Association builds in-house inside MinDigital's platform.

### 4.5 Rejection pre-check as a commercial product — tax + social + auction

- Bodies (state): Tax Committee VAT refund, NASP Social Register, Cadastre `Yerelektron`, Construction Inspection.
- Bodies (private, no tender): tax-advisory firms, accountants, property-heavy corporates.
- Need: validate a submission before it enters the pipeline; assemble the appeal pack when the machine says no.
- Numbers: VAT refund **46.4% rejected** — 9,296 of 20,014 reviewed in 2024, computed from ISR `P173001`. NASP: 184 mahallas rejected **2,000 of 2,000** in one month. `Yerelektron`: ~40% of 90,001 plots never cleared (our derived rate). Cadastre baseline: ~1/3 of 1M+ requests rejected in six months.
- Deadline shape: recurring, not a one-off — every quarterly filing is a fresh five-day crunch.
- Build: rule engine over the statutory checks + registry lookups; per-domain rule packs; appeal-pack generator for the tax case (statutory m² minima 3.53M Tashkent / 2.35M Nukus & regional centres / 1.39M elsewhere, across a 208-district coefficient table).
- Why we win: **no tender needed on the private side**, revenue starts before any state contract lands, and the state-side evidence is published by the state itself. Critically, WB `P173001` measures VAT processing *speed* (18 days actual vs 30-day target) and **not rejection** — the failure mode is unmeasured, which is precisely the space the product occupies. [WB ISR](https://documents1.worldbank.org/curated/en/099061325101540967/pdf/P173001-0fa2abd7-22af-42cc-ad6d-5d844d19092f.pdf) · [gazeta.uz](https://www.gazeta.uz/ru/2026/07/17/social-protection/) · [buxgalter.uz](https://buxgalter.uz/publish/doc/text212837_chto_menyaetsya_v_naloge_na_imushchestvo_v_2026_godu)

---

## 5 Patterns across government

### Pattern A — cadastre proliferation
- At least four "cadastres" stand up in parallel with no cross-reference.
- `UZKAD` (Cadastre Agency) · State Water Cadastre (MoWR, April 2026) · State Urban Planning Cadastre (Urbanization Center) · pollution cadastre (Ecology Committee).
- Neither the water cadastre coverage nor `GISTD` documentation acknowledges the other. [spot.uz](https://www.spot.uz/ru/2025/10/13/water-management/)
- Consequence: the same hectares carry different identity in each, and `E-yer nazorat` forces three of them into one workflow from `2026-01-01`.

### Pattern B — three spatial pictures of one field
- MoA `Geoaxborot tizimi` holds field contours + AI crop-type identification. [gov.uz](https://gov.uz/oz/agro/pages/geoaxborot-tizimi)
- `UZKAD` holds the legal parcel.
- `Uzbekcosmos` produces a third imagery-derived polygon set.
- Evidence the mismatch is already priced: **159,000 ha** where registered area diverges from actual; subsidised credit and water quotas issued off the MoA layer while title sits in `UZKAD`. [gazeta.uz](https://www.gazeta.uz/ru/2023/11/22/cadastre/)

### Pattern C — the address layer is nobody's dependency
- `ZRU-1074` (migration, highest address volume in the country) never mentions the address register or the Cadastre Agency.
- `UP-50` (enforcement, automates decisions about immovable property) never mentions cadastre, address or mapping.
- `PQ-280` (notariat, auto-updates five registries on ownership change) never names the address register.
- Res. 1010 **defines a `geokod` field but names no coordinate reference system** — not WGS-84, not SK-42. [lex.uz/4104733](https://www.lex.uz/docs/4104733?ONDATE=30.07.2025)
- Pattern: every statute that touches addresses at scale routes around the statutory address authority.

### Pattern D — deadlines set by decree, funded by donor, on different clocks
- `PQ-286`: national address register on WGS-84 by `2026-12-31`, **no budget line, no procurement mechanism** in the decree text.
- WB `GISTD` `P506803` ISR Seq. 3 (07-Aug-2026): indicator "National Address Registry System established" targets **June 2030**; disbursed $0.11M of $35.00M = **0.31%**. [ISR](http://documents1.worldbank.org/curated/en/099080726033013763/txt/P506803-2a579591-2680-4438-b235-d843c083525e.txt)
- The funded plan already tacitly ignores the decree date. Decree dates are political signals; donor plans are the real schedule.
- Same shape elsewhere: `PQ-299` mandate 2024 vs 1,044 plans digitised in 2026; Res. 559 integrations 8 months overdue; Tourism platform slipped 13 months in one decree cycle.

### Pattern E — in-house operator assigned before the market sees the requirement
- `Uy-joy` platform → `Urbanizatsiya laboratoriyasi MCHJ`, 40 bn soum, contracted **`tender hamda tanlov savdolarini oʻtkazmasdan`** — without tender. [lex.uz/-8071993](https://lex.uz/uz/docs/-8071993)
- `OASIS` → MinDigital in-house; `UZINFOCOM` named sole integrator.
- `E-yer nazorat` → Cadastre Agency's own computerisation centre, funded by 2% of collected penalties.
- `Raqamli mahalla` → Association of Mahallas' own `Raqamli mahalla` IS.
- Consequence: prime contracting is mostly closed. The realistic shapes are **sub-contract**, **component supply**, and **donor-procured lots**.

### Pattern F — Esri incumbency, but not everywhere
- `open.ngis.uz` runs ArcGIS JS 4.22 (baseline).
- `Hududgazta'minot` runs ArcGIS Enterprise Advanced (`ArcGIS-HGT`, Namangan pilot Mar 2026, Jizzakh rollout) + ArcGIS QuickCapture.
- Implication for `P4`: a non-Esri PostGIS + MapLibre stack competes on price at the **municipal/regional** tier, where WB `P508451` `DLI 4` only requires "a GIS unit with ≥1 GIS specialist + basemaps" — a bar a region clears with desktop QGIS and a contractor.
- Do not fight Esri at the utility or national tier.

### Pattern G — donor money is the only reliably open door
- Open-to-international, verified: ADB `54272-001` ($27.68M consulting), WB `GISTD` `P506803` (~$1.8M address packages), WB `P508451` ($9.625M IPF under 2025 IPF Regulations, below OPRC thresholds), WB `P173450` ($100k GIS package still `Pending Implementation` after its plan period expired).
- Every one runs REOI → shortlist → RFP → evaluation. No bilateral emergency buy exists in this map.

### Pattern H — automation shipped ahead of the data it consumes
- Tax: six taxes auto-assessed from `2026-01-01` off registers the Tax Committee does not own.
- Construction: AI screening of permit applications from `2026-09-01` with 88% of settlements lacking digitised zoning.
- Notariat: auto-update to five registries from `2026-04-01` off typed address strings.
- Enforcement: 70% automation by `2027-01-01` with no property-identity layer.
- This is the single most repeated shape in the map, and it is what makes `P6` and `P3` sellable at the same time.

---

## 6 Who actually owns addressing

**Contested in practice; settled on paper.**

On paper:
- CM Res. **1010** of 14.12.2018 establishes the **Unified Register of Addresses of Real Estate Objects** as the single register of record. [lex.uz/4104733](https://www.lex.uz/docs/4104733?ONDATE=30.07.2025)
- Supervisor = **Cadastre Agency**; addresses are assigned, changed and cancelled by its territorial State Cadastre Chamber branches.
- Art. 3 ¶1 binds local executive authorities to consume it in e-services and interagency exchange; ¶2 puts **personal responsibility on heads of state bodies** for timely, reliable submission.
- Still maintained: amended by CM Res. 620 (27.10.2022) and CM Res. **791 of 15.12.2025**. [lex.uz/7926688](https://lex.uz/docs/7926688)
- Parent body correction to the baseline: kadastr.uz states the agency sits under the **Committee on Urbanization and Housing Market**, not the Ministry of Economy and Finance. [kadastr.uz](https://kadastr.uz/uz/agentlik-haqida)

In practice, four rivals:

| Claimant | What it actually holds | Status |
|---|---|---|
| Cadastre Agency | Unified Register of Addresses + `UZKAD`; `GISTD` B.2 funds the national register to **June 2030** | statutory owner, register not yet delivered |
| MIA Migration | `turgan joyi bo'yicha ro'yxatga olingan manzili` inside `Pasport-viza`; `ZRU-1074` names neither the register nor the agency | de-facto parallel store, self-declared, highest volume |
| Khokimiyats | Not a register — a **document source** feeding the Chamber's assignment workflow | the "third address authority" framing is refuted (§7) |
| Statistics Committee | 7.6M geolocated households from the 2026 census, tablet-captured, GIS-monitored | largest and freshest point layer; custody undecided |
| Tax Committee | `Юридический адрес` + `Фактический адрес` + branch addresses per entity in `TsBD`, free-text | consuming store, no schema |
| Post | No claim surfaced in this research — **source not captured** | unassessed |

The answer:
- **Legal ownership is not contested** — Cadastre Agency, since 2019-01-01, mandatory for all state bodies.
- **Operational ownership is contested** because the register does not exist yet in usable form, so five bodies each maintain a working substitute.
- Three geographies, one mandatory-use rule, **zero published crosswalk** — and since `2026-01-01` property tax is assessed automatically off that unreconciled base. [lex.uz/4104736](https://lex.uz/docs/4104736)
- The commercial consequence: sell the **crosswalk**, not a rival register. A rival register competes with a World Bank-funded obligation; a crosswalk is what every one of the five needs regardless of who wins.

---

## 7 Refuted claims

| Claim | Killed by |
|---|---|
| `PQ-286` is a Ministry of Digital Technologies decree | `PQ` = Presidential Resolution; issuer is the President. Ministries cannot issue `PQ` acts. [lex.uz/7730357](https://lex.uz/uz/docs/7730357) |
| No address-normalisation toolchain exists / vacuum to fill | `GISTD` April-2026 procurement plan has 5 packages, ~$1.8M, three open to international firms; `QCBS/01` already Under Review |
| Address register due `2026-12-31` creates a Q4-2026 emergency buy | ISR targets **June 2030**; 0.31% disbursed; decree carries no budget line |
| Mahalla registry keys on cadastral number, breaking joins | CM Res. **586** (15.09.2025) retrieves by **mahalla code or STIR**; it is a ~10k-row reference book, not a transactional join. [gazeta.uz](https://www.gazeta.uz/oz/2025/09/18/mahalla-reestr/) — note `PF-116` item 34 later *does* mint mahalla cadastral numbers, so the mechanism revives on a different basis |
| Unified state-governance platform is an open per-region geospatial slot | Same gap is the problem statement of active $35M `P506803`; geospatial is 1 of ~7 co-equal data categories; the president "reviewed proposals", no decree |
| 130+ databases merge with unnormalised addresses as the blocker | Cross-registry key is `PINFL`/`STIR`, not address; `UZINFOCOM` is named integrator; OASIS built in-house |
| 70% e-service target by end-2026 is a live scramble | Already **81.5%** as of Q1 2026; programme superseded by `Byurokratiyani bartaraf etish — 2030` from `2026-01-01`. [gazeta.uz](https://www.gazeta.uz/ru/2026/05/14/government-services/) |
| WB `LPCP` `P508451` names no GIS tooling | `DLI 4` = $16M, "operationalized GIS-based asset inventory", 4 DLRs specifying layers. Also: total is **$410M** not $430M, IPF is **$9.625M** not $9.8M, approval **2025-12-11** |
| Address authority split across three registers, no reconciliation mechanism | Cited URL was the wrong document (`5112432` = CM Res. **732** of 2020, not Res. 1010). Res. 1010 is the *unification* instrument. Res. 732's «манзил» hits are «манзилли дастур» — a capital-works list, not an address register |
| Five registries, no lifecycle owner — open opportunity | `PQ-73` (24.02.2026) created `Uy-joy` platform, 40 bn soum, operator `Urbanizatsiya laboratoriyasi MCHJ`, contracted **without tender**. [lex.uz/-8071993](https://lex.uz/uz/docs/-8071993) |
| Tashkent courtyard inventory ordered with no system behind it | `E-yer nazorat` is the exclusive channel since `2026-01-01` under `PQ-287`; the PGO is a mandated participant. The cited "CM Res. 732 in 2020" origin is unverifiable |

Surviving fragments worth keeping:
- `gis.kadastr.uz` TLS SAN mismatch reconfirmed (cert covers `*.fmmi.uz`).
- The address register genuinely does not exist yet — all five `GISTD` packages Pending or Under Review.
- The Lolazor failure mode (**legally issued** permit → 27.5 m tower on a courtyard) is *not* what `E-yer nazorat` detects. No register of courtyard or playground polygons surfaced. That missing designation layer is real and unclaimed.
- Geographic Nomenclature Classifier: provincial authorities register all street names, align with the State Registry of Geographic Objects by `2026-07-01`. [norma.uz](https://www.norma.uz/ru/novoe_v_zakonodatelstve/razrabotan_klassificator_geograficheskih_obectov2) — unchecked against `P1`/`P2`.

---

## 8 Sequencing

Prior ranking (cadastre-only): geocoder > rejection pre-check > valuation appeal > municipal geoportal > utility field app.

Revised:

| # | Build | Change vs prior | Why |
|---|---|---|---|
| 1 | **Rejection pre-check** (`P6`) | ↑ from #2 | Only product with tender-free buyers. VAT 46.4%, NASP 2,000/2,000, `Yerelektron` ~40%, tax 5-day window. Revenue before any state contract. |
| 2 | **Registry crosswalk / integration layer** (`P3`) | **new — was not ranked** | Largest independent demand (~24 bodies). Every 2026-2027 deadline is an integration deadline. Includes the two penalty-priced, procurement-free Ecology buyers. |
| 3 | **Geocoder** (`P1`) | ↓ from #1 | Still load-bearing under ~16 bodies, but sells as the **engine inside** `P3`, not as a standalone register competing with a WB-funded obligation to 2030. |
| 4 | **Field capture** (`P7`) | ↑ from #5 | $27.68M in named, internationally-advertised ADB packages, Q4/2026. Plus `mahalla yettiligi` Sept-Nov 2026 and NASP social passports. The single largest funded line in the map. |
| 5 | **Municipal geoportal** (`P4`) | ≈ holds #4 | WB `P508451` `DLI 4` $16M and the Urbanization Center's 138 bn UZS. Non-Esri stack competes at the municipal tier only. |
| — | **Valuation appeal** (`P5`) | **dropped out** | Only 2 buyers surfaced, one of them folded into `P6` as an appeal-pack feature. No funded mass-valuation procurement found outside the Tashkent pilot. |
| — | `P2` addr-toolchain | co-sold | Never sells alone; ships as the data-quality half of `P1`/`P3`. |
| — | `P8` open-data-api | opportunistic | ~9 bodies, cheapest to build over an existing `P3` core. `Uzhydromet` is the cleanest single case — no API at all, feeding a `2026-09-01` publishing deadline. |

What actually changed and why:
- The cadastre-only view made `P1` the wedge. The cross-government view makes `P1` a **component** — the buyers are buying integration and are blocked by addresses, not shopping for a geocoder.
- `P6` moves to #1 purely on **channel**: two buyer classes need no tender at all, and one of them (penalised enterprises) has a decree-priced ROI at 5x and 10x.
- `P5` dies on demand, not on merit.
- The sequencing constraint is not technical. It is that Pattern E closes prime contracting almost everywhere: build `P6` for the private buyers, `P3` for the penalty buyers, and use both as the reference that gets us sub-contracted into the ADB and WB lots.

Start with #1 + #2 in parallel — they share the rule engine and neither needs a tender.
---

## 9 What this sweep got wrong or never checked

An adversarial completeness pass ran beside the synthesis. Its findings limit how far §1–§8 can be trusted.

> Method caveat on this section: the critic exhausted its search budget and fell back to a DuckDuckGo fetch
> proxy for most items. **Every lead below is unverified** unless marked otherwise.

### 9.1 The likely-wrong core assumption

- The map treats "hard deadline + near-zero data baseline" as an unclaimed opportunity
- vacancy was inferred from public silence about vendors
- Uzbek decrees and press do not name subcontractors — silence is a publishing convention, not a market fact
- one accidental hit surfaced a **3-year Korean NSDI project** sitting on the flagship "unowned" slot (§9.3)
- sharper version: five clusters report **every** deadline lapsing with **no published consequence**
- a body that missed five deadlines for free can miss a sixth for free
- lateness without penalty indicates **no budget pressure**, which inverts the buying signal
- second-order: every quantified failure cited is borne by citizens or banks, never by the signing agency's budget
- the two signals that survive this test are the **penalty-priced** ones — `PQ-343` at 5x, `PF-46` §7v at 10x

### 9.2 Bodies missed entirely

| Body | Why it matters |
|---|---|
| `Uzbekcosmos` / Space Agency | tasking authority for the imagery behind every land-violation stream |
| Geodesy & cartography licensing regime | **a gate on us doing survey or field-capture work at all** ([lex.uz/acts/-7086](https://lex.uz/acts/-7086)) |
| Central Election Commission | `Saylovchilarning yagona elektron ro'yxati` — a fifth national address consumer |
| MoD topographic service + SSS certification | coordinate/aerial-imagery classification rules; hard blocker for `P4`/`P7` |
| `Uzstandart` | the unowned geodata standard would issue as an `O'z DSt`; drafting it is a way in |
| `Uzaeronavigatsiya` + airports | drone/aerial-survey clearance for field capture |
| `Uzarxiv` | custodian of the paper master plans `P4` proposes to vectorise |
| State Forestry Agency | forest-fund cadastre = a fifth parallel land register |
| Prosecutor General, Chamber of Accounts, Anti-monopoly | procurement-complaint channel a small vendor needs |
| Telecom operators (`Uzbektelecom`, Beeline, Ucell, Mobiuz) | largest private address consumers, **non-tender buyers**, entirely absent |
| Samarkand khokimiyat, Karakalpakstan CoM | Samarkand is the named `GISTD` pilot city; Karakalpakstan is a separate jurisdiction |
| `Yagona integrator` (`PP-415`), `Unicon Soft`, `O'zdavyerloyiha` | named as gatekeepers/incumbents, never profiled |

### 9.3 Donor programs not surfaced

- **KOICA + LX Corporation** — National Spatial Information Integration Capability Strengthening System,
  Aug 2023 – Apr 2026. Overlaps `GISTD` component A.1 by construction. **Verify this before anything else.**
- **EU + UNDP + MinJust** — Capacity Building on Spatial and Master Plans, launched 2026-07-15;
  donors are already inside the master-plan digitisation problem §4.2 calls unowned
  ([eeas](https://www.eeas.europa.eu/delegations/uzbekistan/eu-and-undp-contributes-strengthening-digital-urban-planning-capacity-uzbekistan_en))
- **EU + UNDP** — Further Improvement of Public Service Delivery, board Dec 2025; direct overlap with `P6`
  ([undp](https://www.undp.org/uzbekistan/press-releases/improving-public-services-together-eu-and-undp-review-reform-progress-uzbekistan))
- **UNDP + GCF** — GIS-based disaster-management system already launched; the ecology cluster claims no such layer exists
- **National NSDI Forum, 2025-11-20** — Cadastre Agency + World Bank + EU, 150+ participants including private sector.
  That attendee list is a literal target list.
- **UNECE WPLA** — Cadastre Agency head of methodology presented "Digitizing the national cadastre", May 2025;
  a named, reachable technical counterpart
- **JICA — verified absent**, not a gap: no mapping/GIS/cadastre project as of Jul 2026
  ([jica.go.jp](https://www.jica.go.jp/english/overseas/uzbekistan/Projects/index.html))
- unsearched: KfW · AIIB · IsDB · USAID-successor · UNICEF · FAO · UN-Habitat · Gulf funds. EBRD inconclusive.

### 9.4 Claims to re-check before use

- `OASIS` — the most load-bearing cross-cutting claim; **no decree number attached anywhere**, deadline self-contradicts
- AI law "signed 2026-03-04", solely-AI decision ban, 50–100 BCU fines — **no `ZRU` number found**
- IT Park export quotas 20%/35%/50% — no source, and it determines the business model
- "Ministry of AI and Digital Development" rename — **probably false**, likely confused with Kazakhstan
- "7.6M geolocated households, Jan–Feb 2026" — largest data-asset claim in the sweep, **carries no source**
- two records contradict themselves internally: the `Uzsuvtaminot` and `PQ-299` signals retract in `signal`
  what their own `evidence` field still asserts
- inherited-but-unre-verified baselines: ~1/3 cadastre rejection rate · 6.3M homes · ~150k OLX listings ·
  4M water connections · 42M ha / 94%

### 9.5 Research modalities never run

- **live procurement portals — the largest omission.** Not one lot number, award price, or winning supplier
  appears anywhere in 12 clusters. Unqueried: [xarid.uzex.uz](https://xarid.uzex.uz/) ·
  [exarid.uzex.uz/uz/tender](https://exarid.uzex.uz/uz/tender) · [xt-xarid.uz](https://xt-xarid.uz/procedure/tender) ·
  [e-xarid.uz](https://e-xarid.uz/en) · [xarid.imv.uz](https://xarid.imv.uz/) (filters lots by **supplier**)
- `reestr.uz` — the register of state information systems; 403s to fetch, needs a real browser session.
  The authoritative "what already exists" list; would likely have caught KOICA/LX.
- `regulation.gov.uz` — draft acts in public discussion; the only influenceable window
- donor **bid pipelines** rather than project pages: World Bank STEP, ADB consultant notices, UNDP eTendering
- job postings (`hh.uz`, Telegram) for `ArcGIS`/`PostGIS`/`geodeziya` — cheapest test of the capacity hypothesis
- company-registry lookups on `Unicon Soft`, the `Yagona integrator`, `UZINFOCOM` subsidiaries
- certificate-transparency enumeration of `*.gov.uz` for unpublicised systems
- Telegram — primary announcement channel for Uzbek agencies, untouched
- **human channel — zero contacts made**

---

## 10 Corrections to the earlier cadastre analysis

- **Parent body moved.** `PQ-347` (2025-11-19) created the `Urbanizatsiya va uy-joy bozorini barqaror
  rivojlantirish milliy qo'mitasi`; `kadastr.uz` now places the Cadastre Agency under that committee, not
  under `MEF`. EEAS still said `MEF` in Nov 2025 — pin the claim by date rather than treating it as a conflict.
- **The address register is real but far off.** `GISTD` ISR Seq. 3 (2026-08-07) targets the National Address
  Registry System for **June 2030** and reports **$0.11M of $35.00M disbursed (0.31%)**. The `PQ-286`
  end-2026 decree date has no budget line behind it.
- **Address normalisation is already procured.** The `GISTD` April-2026 procurement plan carries 5 packages
  worth ~$1.8M, three open to international firms, with `QCBS/01` already Under Review. The "vacuum to fill"
  framing in the geocoder spec is wrong on this point.
- **Legal ownership of addressing is not contested** — CM Res. `1010` (2018-12-14) names the Cadastre Agency,
  binding on all state bodies since 2019-01-01, still amended as recently as CM Res. `791` (2025-12-15).
  What is contested is operational ownership, because the register does not exist in usable form.
- `gis.kadastr.uz` TLS SAN mismatch **reconfirmed** — the certificate covers `*.fmmi.uz`.

---

## 11 Next research, in order

1. **KOICA/LX** — does a Korean-built NSDI already occupy `GISTD` A.1? Kills or confirms `P4` at national tier.
2. **Procurement portals** — run all five, filter by supplier, extract who wins GIS and integration lots and at what price.
3. **`reestr.uz`** via browser session — enumerate what state systems already exist before proposing any.
4. `PQ-343` and `PF-46` penalty exposure — confirm the 5x/10x multipliers and identify enterprises already paying.
5. Verify the 68 unverified `strong` signals, or discard the tier.
6. NSDI Forum participant list — the only ready-made contact list in this research.
