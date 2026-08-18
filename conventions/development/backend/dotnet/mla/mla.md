# Mla

*Last updated: 2026-08-16*

> Every rule whose reach is **one service** — what it declares, where those declarations sit, how it starts, and
> what it consumes.
> Use case — a rule that needs a service around it to mean anything, and stops at that service's boundary.

## The five buckets

| Bucket | Answers | Lead |
|---|---|---|
| [constructs](constructs/constructs.md) | what role am I declaring | the suffix keep-list and the coining gate |
| [components](components/components.md) | what is complete on its own | the self-sufficiency gate |
| [architecture](architecture/architecture.md) | where does it live | one folder per pattern, plus solution grouping |
| [platform](platform/platform.md) | how does the service build, start and answer | the boot floor |
| [domains](domains/domains.md) | which technology or use case | one folder per capability |

---

## The boundary

- must reach no further than one service — a rule spanning services we both own is [hla](../hla/hla.md).
- must adapt a third party here, never contract with it in `hla/` — we own neither end of that wire.
- must sink a rule to [lla](../lla/notation/notation.md) when it holds for any symbol, whatever kind it is.
