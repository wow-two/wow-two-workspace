# Conventions — wow-two

*Last updated: 2026-07-10*

> **The single index to every convention.** When a task touches *how we build* — code, repo structure,
> naming, versioning — search HERE first, then open only the file(s) you need. Lookup table,
> **not auto-loaded**; do not pre-read the targets. Area indexes are named `{area}-conventions.md`; this is the root.

## How to use

1. Find what the task touches below.
2. Open that ONE file (leaf files live in the area sub-folders).
3. A repo-level rule (`workbench/{repo}/CLAUDE.md` or `.claude/rules/`) **overrides** a convention for that repo.

## Authoring a convention

Every convention doc follows this shape:

```markdown
# {Title}                         ← noun, matches the file name

*Last updated: YYYY-MM-DD*

> {What — one line}.
> Purpose — {why it exists / the problem it solves}.
> Use case — {when / where you reach for it}.

## {Section}

- compact bullet · backtick every `Symbol` and `path/to/file`
- one fact per bullet, no paragraph > 2 lines

---

## {Next section}

- ...
```

Rules:

- **Super-compact by default** — a convention is a *reference, not a tutorial*. Cut every word that doesn't change what the reader does; if a rule fits in
  a table row or a 1-line bullet, it must not be a paragraph.
- **Shape** — `# Title` → `*Last updated:*` → description blockquote → `##` sections. `---` between **every** section. No `## See also` — link inline only
  where load-bearing.
- **Description** — **one line**: **What** it governs + the scope boundary. Add **Purpose** (*why*) / **Use case** (*when*) only when they aren't obvious from What — and never restate a fact (e.g. a path) in both the description and the body. Not "Conventions for X" filler.
- **Budget — the rule that makes the rest measurable.** A line is **≤120 characters**, **75 preferred**; over 120 is an exception a claim earns by keeping its scope, causality or negation words. No cap on a doc's length — a doc is as long as its rules, and padding is caught by compaction, not by a line count.
- **Compaction — every rule earns its characters.** Cut a line the reader already believes; cut a line that changes nothing they do next; cut the motive clause unless it changes the action. Prefer the verb to its nominalization, and the actor as the subject. A rule that survives all three cuts is the rule; anything else was commentary.
  doc is carrying something that is not a rule — split it or move it (→ *Rationale lives elsewhere*). Check with
  `wc -l` and `expr $(wc -w < f) / $(wc -l < f)`; a words-per-line above ~8 means the bullets have become sentences. `controllers.md` sits at ~4.6.
  Exempt: this file and the `{area}-conventions.md` indexes — an index is a lookup table, and its length tracks the tree, not its own verbosity.
- **Rationale lives elsewhere.** A convention states **what to do**; *why* belongs in a co-located `{name}-rationale.md` or an `ideas/` analysis,
  linked once from the section. Evidence, RFC citations, counter-arguments, and measured findings are analysis — a reader looking up a rule pays
  for them on every read. Keep at most a one-clause because when it changes what the reader does.
- **`## Open` is capped at 5 items** — an unresolved question older than that is a stalled analysis, not a convention note. Move it to the
  rationale / analysis doc and link it.
- **Density** — super-compact bullets, imperatives, one fact per line. No prose paragraph > 2 lines. Code fence for multi-line only; backticks for every
  identifier.
- **Directive rules** — write each rule as `- must {action}` / `- must not {action}` / `- may {action}`: one atomic rule per bullet, the exact action, no rationale unless it changes what's done. Turn a description ("the latest folder is active") into a directive ("must treat the latest folder as active").
- **Plain-noun headers** — section headers are flat nouns (`Scope`, `Invariant`, `Naming`, `Lifecycle`), never narrative phrases (`The wall`).
- **Hard wrap** — wrap prose at **150 cols** (the editor's setting).
- **Tables vs bullets** — tables only for narrow 3+-item × 2+-col data that fits inside 150 cols. If any row would exceed the 150-col hard wrap,
  convert that table to bullet points — a wrapped wide table is unreadable.
- **Citation** — concrete symbols (`IKeyedEntity<TId>`, `AddDatabaseBespokeMigrations`) + file paths, **never namespaces** (they go stale — grep the
  symbol). Verify a symbol exists in source before citing; examples come from real code.
- **No duplication** — reference another convention inline; don't restate it. Supersede a stale note in place rather than stacking.
- **Location** — `{sub-domain}/{name}.md`; a folder's lead doc is `{folder}.md`, `README.md` only at a repo root.
- **One level per folder** — docs describing different levels never sit at the same folder level. A doc about *what you declare* and a doc about *how you write it* are two levels; separate them by folder or by nesting, never by filename alone.
- **A constraint earns a rule only when no positive rule already excludes it** — a starter rule fixes the starter, so a wrong starter is only a ❌ example; nothing about a correct starter forbids a type from bridging two services, so that needs its own rule.
- **An example demonstrates its own section, never the whole doc** — a code sample under `Member docs` shows the member-doc rules and may omit everything else the type needs. Repeating every convention in every example is what makes examples stale.
- **A layer references one layer down for doc rules, never restates them** — a component doc's `### Type doc` cites the layer below it and stops there; the reader crawls down for the merged set. Restating a lower layer's rule creates a second copy that drifts.
- **One whole-shape example per component, placed last and marked illustrative** — after `## Content`, a single fence shows the finished file top to bottom so a reader sees how the sections compose. It is not normative: the sections remain the authority, and a rule stated only in the shape example does not exist.
- **One example per doc-comment section, placed last** — it sits after the final field sub-heading so it covers every field the section declared, not only the first.
- **A table degrades to bullets** — if any row would exceed 120 characters, the table becomes bullet points. A wrapped cell is unreadable, and the wrap is the signal that the rows carry sentences rather than fields.
- **No files beside folders** — once a folder holds a sub-folder, every other doc in it gets its own folder too. The folder's own lead doc (`{folder}.md`) is the single exception.
- **Bullet case** — a bullet is a **lowercase fragment**, not a sentence (capitalize only an identifier / proper noun that opens it). Terse `key - detail` fragments; `controllers.md` is the reference.
- **Order is normative** — list sections and their bullets in the **order they're applied**; readers + adopters follow that order unless a special case is called out (e.g. the attribute order, the doc-block order in `controllers.md`).

## Domains

| Domain | Covers | Status |
|---|---|---|
| **development** (below) | how we build — repo shape, backend & frontend code style | Active |
| **planning** (below) | how we plan — version docs (grows over time) | Active |
| **agentic-workflow** (below) | how parallel chats / agents share a repo — lanes · no-revert · scope containment | Active |
| **marketing** (below) | how we name, brand & go to market — naming/domains · GTM · channels · SEO · content formats | Active |
| **design** (below) | how we design — variant-driven exploration · per-app specs · light/dark parity | Active |
| **deployment** (below) | how we ship & host — single-host serving · dev-port ledger (Docker · CI/CD · release to come) | Active |
| security | secrets handling, auth patterns, threat model | Planned |

---

## development — index: [development/development-conventions.md](development/development-conventions.md)

Cross-area: **[dev-cycle.md](development/dev-cycle.md)** — 2-cycle app↔SDK maturation (implement in-app → extract to SDK + conventions → adopt across the named active apps).
Cross-area: **[swappable-modules.md](development/swappable-modules.md)** — engine-wrapping SDK modules: house contract + adapter subpaths (optional peers) + one shared conformance suite + app-side one-line engine pin.

### repo/ — repo shape & setup · [repo-conventions.md](development/repo/repo-conventions.md)

| Need | File |
|---|---|
| Repo layout (product / venture) · `product/` + `engineering/` · code under `engineering/codebase/{slug}.{backend,frontend}-services` · naming · folder-docs (no README below root) · archetypes · **image-publish contract** (§13) · **audit** | [development/repo/structure/repo-structure.md](development/repo/structure/repo-structure.md) |
| SDK / library repo shape · `engineering/` + npm package under `engineering/codebase/{slug}/` · `src/` source-only + `tests/{unit,stories}` · config repoint · dist-only publish | [development/repo/structure/sdk-structure.md](development/repo/structure/sdk-structure.md) |
| Commit-message format (`{type}: {past-tense verb} {subject}`, 50–70 chars, subject only · one cohesive change) **+ commit protocol** — agent stages + commits; the human pushes, and history ops need a rapid-building marker (hook-enforced) **+ large files** — LFS vs gitignore, and repairing a binary already in pushed history | [development/repo/version-control/git.md](development/repo/version-control/git.md) |

### backend/ — .NET conventions (cut by scope) · [dotnet-conventions.md](development/backend/dotnet/dotnet-conventions.md)

Backend rules live under the stack that owns them (`backend/dotnet/`), and each stack is cut by **how far a rule reaches**.

| Scope | Reaches | Docs |
|---|---|---|
| `lla/` | one symbol | `naming` · `documentation/` (6 blocks) · `members` · `code-organization` · `models` · `idioms` · `banned-constructs` |
| `mla/components/` | a kind of type you declare | `components` · `service` · `client` · `broker` · `repository` · `controller` · `request-model` · `response-model` · `entity` · `enum` · `settings` · `result` · `validator` |
| `mla/layers/` | where a type lives | `layers` · `domain-structuring` · `testing` · `test-databases` |
| `mla/platform/` | how the service builds, starts and answers | `build/` · `host-configuration` · `startup-defaults` · `launch-profiles` · `time` · `serialization` · `problem-details` · `api-context-building` · `known-endpoints` |
| `mla/domains/` | a concrete technology or use case | `identity/` · `messaging/` · `persistence/` (+ `migrations/`) |
| `hla/` | between our own services | gateway · gRPC contracts · cross-service events · quotas — **empty by design** |

**Routing.** Kind of type → `mla/components/{kind}.md` · any symbol → `lla/` · where it lives → `mla/layers/` ·
build and start → `mla/platform/` · a technology or use case → `mla/domains/{domain}/` · both ends ours → `hla/`.

### frontend/ — React / TS code style · [frontend-conventions.md](development/frontend/frontend-conventions.md)

| Group | File |
|---|---|
| `code-style/` | `naming` · `documentation` · `imports` · `code-organization` · `models` · `type-mapping` · `enums` · `extensions` |
| `architecture/` | `architecture` · `state-and-data` |
| `presentation/` | `components` · `component-catalog` (SDK component inventory + app instances) · `forms` · `hooks` · `styling` |

---

## planning — index: [planning/planning-conventions.md](planning/planning-conventions.md)

| Area | File |
|---|---|
| Rough-track docs — `r{X.Y}` unbounded first build: one task per subsystem, no sub-steps + template | [planning/rough-track/rough-track.md](planning/rough-track/rough-track.md) |
| Version-track docs — `v{X.Y}` versions: naming, lifecycle, cadence + iteration template | [planning/version-track/version-track.md](planning/version-track/version-track.md) |
| Polish-track docs — `p{X.Y}` behavior-invariant cleanup, tasks per file, decoupled + template | [planning/polish-track/polish-track.md](planning/polish-track/polish-track.md) |
| Vector-track docs — subject lanes, one chat each: archetype ladders, seams, git + build contention, release cuts + template | [planning/vector-track/vector-track.md](planning/vector-track/vector-track.md) |
| Engineering planning — repo roadmap + backlog | [planning/engineering-planning/engineering-planning-conventions.md](planning/engineering-planning/engineering-planning-conventions.md) |

## agentic-workflow — index: [agentic-workflow/agentic-workflow.md](agentic-workflow/agentic-workflow.md)

| Need | File |
|---|---|
| Parallel chats on one tree · assume-intentional / no-revert · lane discipline · scope containment · commit discipline | [agentic-workflow/agentic-workflow.md](agentic-workflow/agentic-workflow.md) |

## marketing — index: [marketing/marketing-conventions.md](marketing/marketing-conventions.md)

| Need | File |
|---|---|
| Brand-name + domain selection — taxonomy · scoring rubric · verification runbook (TM · RDAP · handles · cross-language) · domain strategy · checklist | [marketing/brand-naming-and-domains.md](marketing/brand-naming-and-domains.md) |
| Go-to-market meta — laws · launch sequence · activation/retention · pricing & CRO (fee-efficiency) · metrics · workflow · checklist | [marketing/go-to-market.md](marketing/go-to-market.md) |
| Channels catalog — audience-fit + effort/payoff per channel (SEO · short-form · Pinterest · directories · integrations · communities · partnerships) | [marketing/channels/channels.md](marketing/channels/channels.md) |
| SEO — intents · comparison pages · programmatic SEO | [marketing/channels/seo.md](marketing/channels/seo.md) |
| Content formats — short-form video + content library (viral · sell · educate) | [marketing/channels/content-formats.md](marketing/channels/content-formats.md) |
| Meme templates — reusable meme/cultural/trending-audio shells (Nobody's-gonna-know · two-button · expanding-brain · POV …) | [marketing/channels/meme-templates.md](marketing/channels/meme-templates.md) |

## design — index: [design/design-conventions.md](design/design-conventions.md)

| Need | File |
|---|---|
| Design exploration — variant-driven (a few in-context options → pick → lock → cascade → spec) · other modes · mode-selection · per-app spec shape | [design/research/design-exploration.md](design/research/design-exploration.md) |

## deployment — index: [deployment/deployment-conventions.md](deployment/deployment-conventions.md)

| Need | File |
|---|---|
| Single-host serving (product / venture) — SPA baked into the backend `wwwroot` (vite `outDir` + static-serve + `BuildSpa` target + dev proxy) · CORS posture | [deployment/hosting/single-host-serving.md](deployment/hosting/single-host-serving.md) |
| Port ledger — allocated dev ports | [deployment/hosting/ports.md](deployment/hosting/ports.md) |

## Scaffolding

- New conformant repo → skill **`create-repo`**. Template repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/`.

## Precedence

A convention applies to **every** repo under `wow-two-ws/`; a repo-level rule overrides for that repo. **Naming + documentation conventions are centralized here** — they apply to the backend-beta SDK too. The SDK keeps only package **layout / registry** as internal architecture under its own `docs/` (`docs/architecture/package-layout.md`, `docs/package-registry.md`).
