# Components

*Last updated: 2026-08-17*

> The small things that are complete on their own — declared, and immediately doing their whole job.
> Purpose — layer 3: our conventions for a thing needing no service, no domain and no collaborator present.
> Use case — a settings record, a clock seam; anything a domain uses without the domain being what defines it.

## The gate [REQUIRED]

The same test the [LLA gate](../../lla/components/components.md) runs, one scope up.

- must be **self-sufficient** — declared, and doing its whole job with nothing else present.
- must fail the gate when it stays inert until a collaborator exists — an `Entity` needs a store, a `Handler` a dispatcher.
- must run the test by demonstration: declare it in a service with no domain, and use it.
- must move to [constructs](../constructs/constructs.md) when it names a role rather than a whole thing.

---

## What lives here

- [json](json.md) — one type's persisted JSON seam, its options and its pair
- [settings](settings.md) — the config-bound record, its binding and its validation
- [time](time.md) — the clock seam, `TimeProvider`, never `DateTime.Now`
