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

## One type, one file [REQUIRED]

Holds for every construct, component and domain type below. A doc states it again only to record a
**deviation**, never to repeat it.

- must keep a generic and its non-generic companion together — `Result.cs` holds `Result` and `Result<T>`,
  because they are one contract in two arities.
- must not split a type across files to shorten one — a file too long to read is a type doing too much.

### Partial types

A `partial` is the one sanctioned second file, and only for a reason the split itself makes visible.

| Reason | Example |
|---|---|
| a source generator owns the other half | `[GeneratedRegex]`, `JsonSerializerContext` |
| the composition order must read on its own, apart from what each step does | `HostConfiguration` |

- must name a part `{Type}.{Aspect}.cs`, beside the base file in the same folder —
  `HostConfiguration.Extensions.cs`, never `HostConfigurationExtensions.cs` in a second folder.
- must keep the type doc on `{Type}.cs` alone; a part carries no `<summary>` for the type.
- must let the base file read alone — a reader who opens only `{Type}.cs` learns what the type is and,
  where order matters, in what order it runs
  ([host configuration](platform/startup/host-configuration.md) § *The partial split*).
- must not add a part for a reason the table does not list — a third reason earns a row here first.

---

## The boundary

- must reach no further than one service — a rule spanning services we both own is [hla](../hla/hla.md).
- must adapt a third party here, never contract with it in `hla/` — we own neither end of that wire.
- must sink a rule to [lla](../lla/notation/notation.md) when it holds for any symbol, whatever kind it is.
