# Display

*Last updated: 2026-08-19*

> A render of content the component does not own — it shows what it is given and changes nothing.
> Purpose — the largest kind gets one rule set: take data in, render it, emit intent, never mutate.
> Use case — text, cards, tables, media, timelines, charts, avatars, badges, glyphs.

## Gate

- must **not own its content** — a component that produces a value is a [control](control.md).
- must render from props alone, so the same props always render the same output.
- must stay in flow and stay non-blocking; a floating surface is an [overlay](overlay.md).
- must report system state through [feedback](feedback.md) instead of styling an error itself.

```txt
✅ Heading · Card · DataTable · Avatar · Timeline · Sparkline · PdfViewer · VideoPlayer · DotsGlyph
❌ EmptyState             (it stands in for content that is absent — a state)
```

---

## Location

### Group

- must live in `presentation/display/` in the SDK, whatever the medium — text, table, media, or SVG.
- must live in the sub-domain that owns the subject in an app ([architecture](../architecture/architecture.md)).

### Folder

- folder and file shape → [constructs](constructs.md) § *Folder*.

```txt
✅ presentation/display/dataTable/{DataTable.vue, DataTable.spec.md, index.ts}
❌ presentation/display/codesTable/         (a product's subject does not ship from the SDK)
```

---

## Declaration

### Component doc

#### [Renders](../../lla/notation/documentation/documentation.md)

- must name what is shown, never how it is fetched.

### Construct

- must be generic over the row or item type when it renders a collection — `DataTable<TRow>`.
- must keep a compound display's parts in one folder ([architecture](../architecture/architecture.md)).

### Component name

- must end a tabular surface `*Table` · `*Grid` · `*Row` · `*Cell`.
- must end a media render `*Preview` · `*Carousel` · `*Gallery`.
- must end `*Viewer` for a read-only document surface, `*Player` for a media transport one.
- must end `*Card` for a bordered box, `*Badge` · `*Tag` · `*Status` for a chip carrying its own text.
- must end `*Renderer` for a render dispatching on a discriminator, `*Glyph` for a fixed-geometry SVG mark.
- must keep a widely-known bare name bare — `Card` · `Badge` · `Avatar` · `List` · `Tree`.

```vue
<script setup lang="ts">
/** Renders a column-driven table with client-side sorting. */
defineOptions({ name: 'DataTable', inheritAttrs: false });
</script>
```

---

## Content

### Props

#### [The](../../lla/notation/documentation/documentation.md)

- must take the content itself — an array or a scalar, never a fetcher or a query key.
- must pair a scalar prop with a same-named slot when the caller may need rich content.

### Slots

- must expose a slot per repeated unit — the row, the cell, the item, the node.

### Emits

#### [Fires when](../../lla/notation/documentation/documentation.md)

- must emit the user's intent — `select`, `sort`, `expand` — and leave the change to the caller.

```vue
<script setup lang="ts">
defineProps<{ rows: ReadonlyArray<TRow>; columns: ReadonlyArray<ColumnDef<TRow>> }>();   // ✅
defineEmits<{ (e: 'sort', descriptor: SortDescriptor): void }>();                        // ✅ intent
defineProps<{ queryKey: string }>();                                                     // ❌ it would fetch
</script>
```

---

## Composition

- must be composed by a [page](page.md), a [view](view.md), a [panel](panel.md), or a [layout](layout.md).
- must compose [indicator](indicator.md) and [action](action.md) inside its own slots.
- must not mount a [view](view.md), a [panel](panel.md), or a [page](page.md).

```txt
✅ CodesTableView → DataTable → Badge + CopyButton
❌ DataTable → LoadingState      (the caller decides whether there is anything to show)
```

---

## Neighbours

- [state](state.md) — the stand-in when there is nothing to display
- [indicator](indicator.md) — the passive marks a display hangs off its rows
- [feedback](feedback.md) — the kind that reports system state rather than content
- [component catalog](component-catalog.md) — every other kind, and the composition ladder
