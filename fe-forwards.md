# Forwards — backend → frontend conventions

*Last updated: 2026-08-19*

> Decisions the backend lane settled on 2026-08-19 that the frontend tree has to mirror or answer.
> Drain it, then delete it. Each numbered line is a prompt; the citation is where the rule now lives.

## Shared conventions — already merged, nothing to decide

These landed in files both trees answer to. Read them; no frontend edit unless a frontend doc contradicts one.

1. **The layers of a thing** — `development/development-conventions.md`. Baseline · construct · application,
   and layer 3 splits by self-sufficiency into `components/` or `domains/`.
2. **Both scopes carry both roles** — same file. `lla/constructs` + `lla/components`, `mla/constructs` +
   `mla/components`; a language form's own conventions never file under `mla`.
3. **Whose thing earns a doc** — same file. Platform, framework and our own SDK only; a third-party name may
   be cited, never documented.
4. **Section-to-section linking** — `conventions.md` § *Authoring a convention*. A child doc cites the owning
   section once and states only its override.
5. **A restatement is allowed only when the rule cannot be lifted** — same file.

---

## The recut — the biggest thing to mirror

`conventions/development/backend/dotnet/` now splits twice, orthogonally:

```
backend/dotnet/
  core/      lla/ · mla/ · hla/            — holds whatever the deliverable is
  shapes/    service/ · library/ · sdk/ · cli/
```

- **The test** (`shapes/shapes.md` § *The test*) — not *does the rule change between deliverables*, but
  **does the rule have a subject when this shape is absent?** Middleware order never changes and is still
  shape-bound, because a CLI has no pipeline.
- **A vector lives inside a shape** — `service/` carries `architecture/` (clean written; onion, hexagonal,
  vertical-slice as shells), `platform/`, `topology/`, `delivery/`.
- **Placement left the constructs.** A construct doc names its folder — `Services/`, `Entities/` — and the
  shape says which project holds it (`shapes/service/architecture/architecture.md` § *Where a folder is
  created*). Every component `## Location` is now a pointer to its construct.

Also settled while recutting: a construct doc that gained a construct **also** stopped restating it — the
six component docs reduced their `## Location` and `## Declaration` to a pointer, and the two family leads
lifted their shared doc-template rules into `core/mla/mla.md` § *Writing a doc in this scope*.

Frontend prompt: run the same two cuts. A React app, a component library and `@wow-two-beta/ui` are three
shapes; `lla`/`mla`/`hla` is the scope cut and belongs under `core/`.

---

## Prompts to run in the frontend lane

1. **Re-open `lla/components/`.** `lla/constructs` rules the language form, `lla/components` rules that form
   used end to end, and `mla/*` rules only our own things — re-cut the deleted docs on that line.
2. **Register vocabulary is merged, not mirrored.** `components.md` § *The registers* reads
   definition · application · surface on both sides; `judgement` became `application`, and the frontend's
   `surface` register survived into the shared table. Confirm nothing still says *judgement*.
3. **Every `mla/components` doc needs an `mla/constructs` doc.** The backend found six missing and wrote them.
   Run the same count — a component is layer 3 *of* something.
4. **One type, one file, lifted.** The backend moved 27 copies of the per-doc location rule into one parent
   rule plus a partial-types section. Check for the same repetition.
5. **Deduplicate the index against the scope lead.** `dotnet-conventions.md` had § *The three scopes* and
   § *What each scope owns* restating what `core/core.md` owns; both moved into the folder's own lead, and the
   index keeps only the two cuts, the layers map, layer direction and the `Files` table. Run the same check on
   `frontend-conventions.md` against its scope leads.
6. **The nested sub-block suffix is settled: `{Noun}Dto`.** `core/mla/domains/api/api-messages.md` §
   *Nested sub-blocks*. A body one action binds is `{Verb}{Noun}ApiRequest`; anything nested inside it is a
   `Dto`, in a request or a response. Drop `{Noun}ApiRequest` for sub-blocks.

---

## Not forwarded

- `BackgroundService` replacing `HostedService`, the `SqlNaming` split, the `Program.cs` group count, the
  entity contracts, the `Api/{Domain}/Controllers/` placement — backend-only, no frontend analogue.
