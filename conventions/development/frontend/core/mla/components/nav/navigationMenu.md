# NavigationMenu

*Last updated: 2026-08-19*

> The top-level strip whose entries can drop a rich panel — the mega-menu shape.
> What a nav component is → [nav](../../constructs/visual/nav.md).
> Its full surface → `NavigationMenu.spec.md`.

## Reach for it when

- must carry the app's or site's top-level sections in one horizontal strip
- must let some entries open a panel of rich content and others link straight out
- should back a marketing header or an app-wide section selector

---

## Instead of

| Reach for | When |
|---|---|
| [Menubar](menubar.md) | the strip holds app commands rather than destinations |
| [NavItem](navItem.md) | the destinations stack in a sidebar instead of a strip |
| [DropdownMenu](dropdownMenu.md) | the entry drops a flat list of rows, not a panel |

---

## Values

- must give every trigger entry a stable `value` — the strip opens by that id
- must render a panel-less entry as `NavigationMenuLink` — it joins the roving tab stop
- should replace the default `Main navigation` label when a second nav shares the page
