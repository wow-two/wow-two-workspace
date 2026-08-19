# Menubar

*Last updated: 2026-08-19*

> The application menu strip — the File · Edit · View shape.
> What a nav component is → [nav](../../constructs/visual/nav.md).
> Its full surface → `Menubar.spec.md`.

## Reach for it when

- must group several command menus into one horizontal strip
- must keep one menu open at a time, switching as the pointer crosses triggers
- should carry app-wide commands a desktop reader expects in a bar

---

## Instead of

| Reach for | When |
|---|---|
| [DropdownMenu](dropdownMenu.md) | one trigger owns the only menu |
| [NavigationMenu](navigationMenu.md) | the strip leads to places and opens content panels |
| [CommandPalette](commandPalette.md) | the same commands are found faster by typing |

---

## Values

- must give each `MenubarMenu` a stable `value` — the strip opens by that id
- should keep the default `4` px content offset — tighter than a standalone menu's `6`
