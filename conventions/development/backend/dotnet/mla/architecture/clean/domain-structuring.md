# Domain structuring

*Last updated: 2026-08-16*

> How a domain's folders are cut inside a [layer](clean.md) — subdomains, role groups,
> and where a component folder may appear.
> Purpose — the layer set says which projects exist; this says how each one is divided.

## Pattern

```
{Domain}/
  Core/           ← the entity itself: queries, models, DTOs, projections
  {Operation1}/   ← lifecycle phase or concern (e.g. Capturing, Processing)
  {Operation2}/
  ...
```

`Core/` is always present when a domain has subdomains. It holds the reusable read model,
so any consumer — CRM, API, reports, pipelines — references `Core` without pulling in operation-specific code.

---

## Example

A `Listings` domain spans the full lifecycle: scraping → classifying → querying → triaging → publishing.
Each phase is a subdomain.

**Domain layer** (`{Repo}.Domain/Listings/`) — entities and enums:

| Subdomain | What it owns |
|---|---|
| `ListingsProcessing/` | The listing entity + classification outputs |
| `ListingCapturing/` | Raw external data before classification |
| `ListingsBoard/` | CRM triage state |

**Infrastructure layer** (`Infrastructure/Listings/`) — implementations grouped by subdomain:

| Subdomain | What it does |
|---|---|
| `Core/` | Read model — querying, filtering, projecting |
| `Capturing/` | Scraping raw listings from external sources |
| `Processing/` | Classifying raw → structured |
| `Publishing/` | Distributing to channels |

---

## `Core/` vs operation subdomains

| Put in `Core/` | Put in `{Operation}/` |
|---|---|
| Read queries (filter, search, paginate) | Write operations (scrape, classify, publish) |
| Request/response DTOs for API consumers | Pipeline nodes and orchestrators |
| Projections and view models | External API clients (LLM, scraper) |
| Shared constants or lookup helpers | Operation-specific models and settings |

---

## Naming rules

- **Domain folder** — PascalCase plural (`Listings/`, `Channels/`, `Locations/`)
- **Subdomain folder** — PascalCase gerund or noun describing the concern (`Capturing/`, `Processing/`, `Core/`)
- **Role-group folder** — a **plural role noun** naming the type-role it holds, never the activity.
  - `Entities/` · `Enums/` · `Models/` · `Services/` · `Validators/`
  - `Mappers/` · `Commands/` · `Queries/` · `Handlers/`
  - ✅ `Validators/` holds validators · `Mappers/` holds mappers
  - ❌ `Validation/` · `Mapping/` — an activity reads as a subdomain, and every sibling names a role
- **Avoid generic names** — `Helpers/`, `Utils/`, `Misc/` are banned.
  - what fits no subdomain belongs in `Core/`
- **Mirror across layers** — Domain `Listings/ListingCapturing/` → Infrastructure `Listings/Capturing/`
  - drop the redundant prefix

---

## Source folder casing

- **Backend source folders are PascalCase**, matching their namespace segment 1:1.
  - `Mediator/Cqrs/`, `Application/Channels/Queries/`, `Data/Migrations/`
  - the top-level **project** dir `{slug}.backend-services/` stays kebab — it is the IDE-collision-proof
    project folder, not a source folder ([repo structure](../../../../../repo/structure/repo-structure.md) §3).

---

## Component folders across layers

A component states its folder **name** once ([components](../../components/components.md) § *Adding a component*);
where that folder may appear is this file's rule, and the two together are not duplication.

- must allow a component folder in **any** layer that declares the component.
  - `Enums/` is legal under Domain, Application and Infrastructure alike.
- must scope the folder to its subdomain, never to the project root.
  - `Listings/Enums/`, never a single `Enums/` per assembly.
- must not read a folder's presence in one layer as a claim on the others; a layer that declares none carries none.

---

## Layer alignment

Domain and Infrastructure mirror each other, but are not forced to be 1:1.
An Infrastructure subdomain may exist without a Domain counterpart — `Publishing/` has no domain entities,
it only formats and sends.

```
{Repo}.Domain/                          {Repo}.Service/Infrastructure/
  Listings/                               Listings/
    ListingsProcessing/   ←── mirrors ──→   Core/        (read model for the entity)
      Entities/                              Processing/  (classify pipeline)
      Enums/
    ListingCapturing/     ←── mirrors ──→   Capturing/   (scrape pipelines)
      General/
      Channels/Olx/
    ListingsBoard/        ←── (no infra) ── triage is DB-only, no infra logic yet
                          ←── (no domain) → Publishing/  (infra-only, formats + sends)
```

Which layer declares an [entity](../../constructs/data/entity.md) or an [enum](../../components/enums.md) is the
declaring domain's call; this file governs only the folder it lands in.
