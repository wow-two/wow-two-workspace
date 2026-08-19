# Validation

*Last updated: 2026-08-19*

> The Standard Schema seam every layer may reach, and the dependency-free validators built on it.
> Purpose — a boundary check below the forms layer needs a vocabulary that pulls in no schema library.
> Use case — parsing config or a URL param, checking a payload, or giving a rule one voice on both sides.

## The contract

- must make every validator a Standard Schema — the spec property is on the object itself.
- must be accepted unchanged wherever a schema is taken, so one object serves a boot parse and a form.
- must return either the parsed value or every issue with its path, never the first issue alone.
- must not throw; the one assert helper throws only because the caller asked it to.
- must sit at the bottom of the layer graph, so a config parser or a payload check can import it.
- must speak one shared rule-code vocabulary, whichever side reported the issue.
- must render a code through the message catalogue, so a rule reads the same on both sides.
- must leave the issue-to-field plumbing in the forms layer — it is not duplicated here.
- must keep a schema library an optional consumer peer, never a dependency of the seam.
- must not pull a library's runtime into a package that ships zero runtime dependencies.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| built-in | primitives, composites and formats, zero dependencies | boundary checks inside a dependency-free package |
| zod | the spec, from the library | a large, evolving domain schema — the default form pin |
| valibot | the spec, from the library | a size-first swap, decided per form |

---

```txt
✅ object({ email: email(), name: string() })   a Standard Schema, usable as a form schema
✅ useAppForm({ schema: ProductSchema })        zod or valibot, invisible to the SDK
❌ if (!raw.email.includes('@')) throw          a hand-rolled check at the boundary
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [forms](../forms/forms.md) — the consumer that maps issues onto fields
- [config](../config/config.md) — the boundary parse this seam exists to serve
- [swappable modules](../../../../../swappable-modules.md) — how a schema library stays an optional peer
