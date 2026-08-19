# ScrollArea

*Last updated: 2026-08-19*

> The scrolling region — one box overflows while the page around it stays put.
> What a layout is → [layout](../../constructs/visual/layout.md).
> Its full surface → `ScrollArea.spec.md`.

## Reach for it when

- must scroll one region of the page rather than the page itself
- must give the box a height, or the overflow has nothing to clip
- should reach for it around a long list, a log, a wide code block

---

## Instead of

| Reach for | When |
|---|---|
| [AppShell](appShell.md) | the scrolling region is the shell's own content area |
| [Box](box.md) | the overflow classes are written directly |
| [PullToRefresh](pullToRefresh.md) | the scrolling region also refreshes on a drag |

---

## Values

- must leave `axis` at `vertical` — it hides the cross axis outright
- must reach for `both` rather than nesting two areas for two axes
- must not wait for the custom-scrollbar organism the spec names — none ships
