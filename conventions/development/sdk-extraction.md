# Extract / Keep / Remove

*Last updated: 2026-07-11*

> For any component / helper / module — already built or being built — decide: **extract to a shared SDK**, **keep in the app**, or **remove it**. Applies to both SDKs (frontend `@wow-two-beta/ui`, backend beta) and to app code. Complements [dev-cycle.md](dev-cycle.md) (the extract→adopt rhythm) and [swappable-modules.md](swappable-modules.md) (engine-wrapping modules); this doc is the **decision**.

## The two questions

1. **Generic or app-bound?** A reusable primitive any product could want, or does it carry *this* app's domain / business logic?
2. **Does it justify existing?** For an app-local piece — especially a low-level one wrapping an SDK primitive — *why* is it there? "To avoid duplication" / "to extend a prop" / "to restyle" is a **red flag**, not a reason.

> **Logic amount does not decide.** A label-only `Field` has almost no logic yet belongs in the SDK; `ContentView` has plenty yet stays in the app. Genericness decides *where*; the red-flag check decides *whether it should exist at all*.

---

## Extract → SDK

Generic / reusable, not tied to this app's domain. Extract **even if**:

- it carries little logic — a `Field` (label + control) is still an SDK primitive; and
- only one app uses it today — `DateTimeField`: build it once, the next product finds it there.

An **atom** (lowest-level input / control) that's generic is *always* SDK, never app-local.

---

## Keep in the app

It carries **app-bound** (domain / business) logic. Keep it as a component for **encapsulation, separation, and readability** — a good reason on its own, not only DRY. E.g. `ContentView` (builds the app's content panel from app rules).

---

## Remove

An app-local piece whose only reason to exist is **DRY, a prop-extend, or a restyle** over an SDK primitive. Don't let it linger — resolve it:

- the extension is generic → **extract** it into the SDK (the primitive gains the prop / variant), then use the SDK version;
- the SDK already covers it → **delete** and use the SDK primitive directly.

Duplicating an SDK-primitive composition across call sites is fine — **never** wrap it in an app-local component just for DRY.

---

## Worked calls

- `Field` (label + control, ~no logic) → **extract → SDK** — generic primitive; no app wrapper to "save duplication"
- `DateTimeField` (Temporal + a11y logic) → **extract → SDK** — generic; extract even though only this app uses it
- `ContentView` (app content panel) → **keep in app** — app-bound logic; earns its place by encapsulation, not DRY
- `SelectField` (app-local, wraps SDK `Select`) → **investigate** — why does it exist? generic extension → extract to SDK; else the SDK covers it → delete + use `Select` directly

---

## Mechanics

- missing a generic primitive → build it in the SDK first (mirror the nearest sibling), publish, consume it — don't grow it in the app "to move fast" and leave it
- built it in the app before the call was clear? re-decide against the two questions and extract or delete — a working app-local primitive is not a resting state
