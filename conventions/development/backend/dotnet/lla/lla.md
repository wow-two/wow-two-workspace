# Lla

*Last updated: 2026-08-18*

> Every rule whose reach is **one symbol** — the form it is declared in, the roles that need nothing around
> them, and how it is written down.
> Use case — a rule that holds whatever kind of type the symbol belongs to, and needs no service to mean anything.

## The three buckets

| Bucket | Answers | Lead |
|---|---|---|
| [constructs](constructs/constructs.md) | which C# form may I write | the construct and statement catalogues |
| [notation](notation/notation.md) | how is it written down | naming, documentation, style |

---

## The boundary

- must hold for **any** symbol — a rule naming a kind of type is [mla](../mla/mla.md).
- must sink a rule here from `mla/` once it survives with no service, domain or collaborator present.
- must let a higher layer override a rule here, stated in that layer's own file, never by editing this one.
