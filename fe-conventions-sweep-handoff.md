# Handoff — frontend conventions sweep

*Last updated: 2026-08-16*

> **Read this once, drain it, delete it.**
> For the chat that owns `conventions/development/frontend/`. The backend tree was rebuilt on 2026-08-16;
> this states what the frontend can inherit, what it must not, and what it decides alone.
> Supersedes the 2026-08-16 morning version of this file — the tree moved underneath it.

## The backend shape, as it now stands

`conventions/development/backend/dotnet/{lla,mla,hla}/`, cut by **how far a rule reaches**.

- `lla/` — one symbol: `constructs/` (what C# offers) · `components/` (roles needing no service) · `notation/` (naming · documentation · style)
- `mla/` — one service: `components/` · `architecture/` · `platform/` · `domains/`
- `hla/` — between our own services; empty by design

The frontend is expected to map onto the same three scopes, not to copy the folder names.

## Two models worth copying

**A component doc states what a type _is_, never its shape.**

- `mla/components/components.md` § *Adding a component* — two sections only: `Location` (folder · file) and
  `Declaration` (type doc · type name). No `Content`, no members, no shape.
- shape belongs to whoever owns it: the SDK for a type it declares, the domain for everything else.
- the folder is the **plural of the suffix** — `Mapper` → `Mappers/`; a component names its own exceptions.
- `lla/components/components.md` § *Adding a component* keeps a third `Content` section, because an LLA role is
  self-sufficient and its members are the whole contract.

**A domain is one contract plus one folder per provider.**

- `mla/domains/domains.md` — the lead states the capability provider-free; every technology-tied rule sits in its
  provider's folder (`persistence/{schema,ef,dapper,sql,dbup}`).
- the frontend has the same split waiting: a data-fetching contract vs `react-query`; a form contract vs the engine pin.

## Inherit verbatim — already language-neutral

Four rules transfer as written; only their address was wrong. Cite them, do not restate them.

- **Name the referent** — `lla/notation/documentation/documentation.md` § *Name the referent*. Name the subject only
  when the value is **not** the type's own; the absence is the signal. The FE currently does the inverse (`CodeDto.ts:9`).
- **The falsifiability test** — `lla/notation/documentation/summary.md`. Six failing shapes, each with what falsifies it.
- **The comment anti-pattern catalogue** — `lla/notation/documentation/documentation.md`, 8 named failures; the FE has 1.
- **Acronym casing** — `lla/notation/naming/naming.md`, already canonical for the whole ecosystem. Violated at `client.ts:8,13`.

## Does not transfer — and that is not a backend defect

Both of these were carried as blockers in the previous handoff. They are closed, refuted rather than fixed.

- **The data/behavior axis** is stated per C# construct in `lla/constructs/constructs.md`. That is correct: the whole
  tree is scoped under `backend/dotnet/`, and no other .NET language is in use. The frontend states its own axis.
- **Expression-body gates 1, 2 and 6** are C#-shaped (`lla/notation/style/style.md` § *The body*). Gates 3, 4 and 5
  transfer as ideas; the frontend writes its own list rather than inheriting six gates about C# members.

## Resolved since the last handoff

- **Request naming** — settled and written down. An **api request** is verb-first (`{Verb}{Noun}ApiRequest`), because it
  serves one controller action; an **application request** is noun-first (`{Domain}{Action}{Kind}`), because it is
  searched by domain. `mla/components/data/api-request.md` and `application-request.md`.
- **`components.md:72`** no longer legislates for the frontend. It states its own scope: every suffix there names a type
  inside a .NET service, and a browser-side type carries none of them. Copy the *pattern* — a rule states its scope and
  names what crosses.
- **`Provider`** — folded to `Service` on the backend. React's `*Provider` is framework-fixed, the same category as
  `Middleware` / `Filter` / `Interceptor`, which the keep-list already exempts. No backend change needed.
- **Response payload naming** — the backend side is now in `mla/domains/api/api-messages.md`: `Response` is the
  envelope's word, never a payload's; a payload is always `{Entity}Dto`.

## Still open — do not map yet

- **The nested sub-block suffix.** `{Noun}ApiRequest` and `{Noun}Dto` are both written down, one sentence apart in
  intent. Recorded in `mla/domains/api/api-messages.md` § *Open*. The frontend copied **both**; leave it until the
  backend chat decides.

## The one the frontend owns outright

**`Helper` is banned on the backend and shipped as a suffix on the frontend.**

- `lla/notation/naming/naming.md` and `mla/components/components.md` ban `Helper` / `Util` / `Utils` / `Common` /
  `Manager` outright, public or internal.
- `frontend/code-style/naming.md:51,57` ships `*Helpers.ts` as a supported suffix and routes work to it.
- Neutral form: *a name describing no role is banned in every language; dependency-free logic over a domain is `Extensions`.*

## Yours alone — no backend rule supplies these

components (one-per-folder, `readonly` props, `{Component}Props`) · prop-name vocabulary (`is*` / `has*` / `can*` /
`show*`, `on*` inbound-only, the controlled triad, `asChild`) · hooks · styling (Tailwind v4 `@theme`, tokens, `cn()`,
`tailwind-variants`) · routing · imports (5 groups, layer-ordered) · forms (engine pin, ProblemDetails→field mapping) ·
server-state vs UI-state · const-object enums instead of TS `enum` · `{Enum}Displays` / `{Enum}Payloads` · compound
components · the component role→suffix table.

Two notes on those:

- the **component role→suffix table** (`frontend/architecture/architecture.md:52-96`) is the FE's own keep-list. Run it
  through the coining gate in `mla/components/components.md` § *Adding a new suffix* — that gate is language-neutral.
- **Descriptor + Catalog** are the FE's names for what the backend calls `Registry` / `Mapper`. That needs a
  cross-reference, not a fresh rule.

## Authoring rules the tree now enforces

In `conventions/conventions.md` § *Authoring a convention*; adopt them for any frontend doc you rewrite.

- one level per folder; no files beside folders except the folder's own `{folder}.md` lead
- a rule states what the code **must have** — the negative lives in the ❌ example
- a constraint earns its own rule only when no positive rule already excludes it
- each doc field gets its own `#### [Field](link)` sub-heading; an undeclared field is forbidden
- one ✅/❌ fence per doc section, placed after the last field sub-heading
- a table degrades to bullets if any row passes 120 characters
- a link's display text names the thing, never the path
- a line reference is `{file}:{line}`
- `---` between **every** `##` section; no `## See also`

## Where to start

1. Read `mla/components/components.md` § *Adding a component* — the two-section template, and why `Content` is absent.
2. Read `mla/domains/domains.md` — the contract + provider split, which the frontend needs for data fetching and forms.
3. Fix `Helper` first — the only direct contradiction the frontend owns.
4. Inherit the four verbatim rules; map the resolved set; leave the nested sub-block suffix alone.

## Do not

- **Do not touch `conventions/development/backend/`** — another chat owns it.
- **Do not resolve a contradiction that changes a rule's meaning.** Surface it, take the decision, then edit.
- **Agents never commit.** Stage one cohesive change, print the message, stop.
