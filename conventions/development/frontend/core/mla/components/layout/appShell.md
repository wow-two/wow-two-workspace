# AppShell

*Last updated: 2026-08-19*

> The app frame — header, sidebar, main, aside and footer laid out as one grid.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `AppShell.spec.md`.

## Reach for it when

- must give an app its one frame, with a sidebar that collapses on a phone
- must mount the regions as children — header, sidebar, main, footer
- must nest the content and aside regions inside the main one
- should reach for it once per app; a page picks the frame, never builds one

---

## Instead of

| Reach for | When |
|---|---|
| [Navbar](navbar.md) | a header bar is the whole frame the page needs |
| [TwoColumn](twoColumn.md) | the frame is an aside and a main column, nothing more |
| `Drawer` | the panel is an overlay, not a region of the frame |
| [Section](section.md) | the page is bands of content rather than an app frame |

---

## Values

- must pass `sidebarWidth` and `asideWidth` as CSS lengths, not Tailwind classes
- must leave them at `240px` and `280px`, and the breakpoints at `lg` and `xl`
- must not name the regions `AppShell.Header` — the spec is React-era; they ship flat
- should bind one of `sidebarOpen` or `isSidebarOpen` — the second wins when both are set
