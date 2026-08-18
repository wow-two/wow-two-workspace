# Component Catalog

*Last updated: 2026-07-10*

> A lookup so building something starts from "what already exists", not a blank file. Two parts: **SDK components** — the reusable `@wow-two-beta/ui` library primitives (check here before hand-rolling, per [`components.md`](components.md) §6) — then **app instances** — the smart-qr reference frontend's concrete components, grouped by the kinds in [`components.md`](components.md) §1. Name + one-liner only; paths live in the tree.

## SDK components (`@wow-two-beta/ui`)

> Every exported component under the library's `src/presentation/*`, grouped by category — the subpath you import from (`@wow-two-beta/ui/presentation/{category}`). One row per component folder; compound parts (e.g. `Card.Header`, `Tabs.Trigger`) ship under their root. Deprecated one-release aliases omitted. Source of truth: `wow-two-sdk-beta.ui/src/presentation/`.

### actions — buttons, toggles, and other action triggers

| Component | Purpose |
|---|---|
| `Button` | Action button for text and/or icon content; variant / size / tone surface. |
| `ButtonGroup` | Visually groups action children; collapses inner radii when attached. |
| `ToggleButton` | Two-state button (on/off) with `aria-pressed` + `data-state`. |
| `ToggleButtonGroup` | Single-select toggle-button group, generic over the value type. |
| `SegmentedControl` | iOS-style connected pill row for single-select. |
| `OptionTile` | Square single-select preset tile (icon-only toggle) for shape / fill grids. |
| `OptionTileGroup` | Labelled `<fieldset>` row of `OptionTile`s with a shared accessible name. |
| `CopyButton` | Clipboard-copy button for code blocks, IDs / URLs, inline copy affordances. |
| `DisclosureButton` | Trigger with a rotating chevron; sets `aria-expanded` + `data-state`. |
| `BackToTopButton` | Floating button revealed past a scroll threshold; smooth-scrolls to top. |
| `FAB` | Floating action button — fixed-position circular button with shadow. |
| `SpeedDial` | FAB that expands into a fan of action buttons (compound Trigger + Action). |
| `Link` | Anchor with consistent focus / hover styling; `asChild` swaps in router links. |
| `Toolbar` | Grouped action controls sharing one tab stop with arrow-key navigation. |

### display — content, media, and data presentation

| Component | Purpose |
|---|---|
| `Heading` | Semantic heading; outline level and visual size set independently. |
| `Text` | Body text with size / tone variants. |
| `GradientText` | Gradient-filled text via `background-clip: text`. |
| `Eyebrow` | Tiny uppercase mini-heading above sections. |
| `SectionHeader` | Section / page header: title + description + actions row. |
| `Highlight` | Wraps each occurrence of a query in the text with `<Mark>`. |
| `Mark` | Highlighted text (`<mark>`). |
| `Quote` | Block quote with left border + italic body. |
| `Code` | Inline or block code. |
| `Snippet` | Code text with a built-in copy button. |
| `Kbd` | Keyboard-key affordance (`<kbd>`). |
| `KeyboardShortcut` | Sequence of `Kbd` keys with connectors (⌘ + K). |
| `Card` | Compound raised surface for grouped content with optional subparts. |
| `FeatureCard` | Marketing feature tile: tinted icon badge + title + description. |
| `PricingCard` | Pricing tier card: name + price + feature list + CTA slot. |
| `StepCard` | Numbered "how it works" step: faint number overlay + icon badge. |
| `InfoRow` | Row of label + value with an optional leading icon. |
| `DescriptionList` | Semantic `<dl>` for label-value pairs. |
| `MetaInline` | Inline row of meta items (badges, chips, status) + trailing actions. |
| `Stat` | Metric tile: label + big value + optional trend + helper. |
| `MetricChip` | Label-value chip with a leading tone-tinted icon. |
| `Badge` | Pill-shaped status / category indicator (non-interactive). |
| `Tag` | Pill with an optional close button (interactive counterpart to `Badge`). |
| `CountBadge` | Numeric badge for notification / inbox counts. |
| `BadgeOverlay` | Overlays a badge / dot on top of any child (avatar, button, image). |
| `NotificationDot` | Tiny colored unread / notification dot. |
| `Status` | Colored dot + label (server status, presence, build state). |
| `Avatar` | Person / entity image with initials fallback. |
| `AvatarGroup` | Overlapping stack of avatars with an optional "+N more". |
| `Image` | Image with a built-in error fallback. |
| `Separator` | Visual divider (semantic or decorative). |
| `List` | Semantic `<ul>` / `<ol>` with markers + `Item` primary/secondary + slots. |
| `Table` | Low-level semantic `<table>`: density + bare / radius variants (compound). |
| `DataTable` | Data-driven table: column defs + client sort, generic over the row type. |
| `DataGrid` | First-gen editable data grid (spreadsheet-like cells). |
| `Tree` | Hierarchical list with expandable folders + selectable leaves. |
| `Tabs` | Tabbed panels (compound List / Trigger / Content) with roving focus. |
| `Accordion` | Expandable sections, single/multiple open (compound Item / Trigger / Content). |
| `Collapsible` | Single show/hide region — a trigger toggles a panel. |
| `Timeline` | Vertical timeline of status nodes (left / alternating align). |
| `Sortable` | Compound drag-to-reorder list (root + `Item` + `Handle`). |
| `SwipeActions` | Drag a row to reveal action slots. |
| `Sparkline` | Inline trend chart (line / area / bar / dot). |
| `Gantt` | First-gen Gantt chart. |
| `ScheduleView` | Multi-resource single-day schedule grid. |
| `EventCalendar` | Month / week / day / agenda calendar with events. |
| `HeatmapCalendar` | Year-long contribution-style heatmap. |
| `DiffViewer` | Line-level diff viewer (split / unified). |
| `NodeEditor` | First-gen node-graph editor. |
| `AudioPlayer` | Custom-controls audio player. |
| `AudioWaveform` | SVG bar-style audio waveform. |
| `VideoPlayer` | Custom-controls video player. |
| `PDFViewer` | Inline PDF viewer. |
| `Carousel` | Slide-show: prev / next + dot indicators, optional autoplay / loop. |
| `Marquee` | Continuously scrolls its children. |
| `ChatBubble` | Single chat message bubble (left / right side). |
| `ThreadView` | Single-thread panel: parent message + replies + composer. |
| `CommentThread` | Threaded comments: avatar + author + timestamp + body, nested replies. |
| `ActivityFeed` | Vertical activity feed: actor / verb / target sentence + timestamp + preview. |
| `MessageList` | Auto-scrolling message stream; sticky scroll-to-bottom, header / footer slots. |
| `ReactionBar` | Row of reaction chips + an optional add-reaction button. |
| `EmptyState` | No-results affordance: icon + title + description + actions. |
| `AnimatedNumber` | Animates the displayed number whenever the value changes. |
| `CountUp` | Number that animates up on mount or on enter-viewport. |
| `Typewriter` | Char-by-char typewriter text. |
| `ScrollReveal` | Reveals children on enter-viewport. |
| `Tilt` | 3D card tilt from cursor position. |
| `Confetti` | Confetti burst. |
| `Tooltip` | Hover- / focus-triggered tooltip. |
| `AnnotationMarker` | Marks an annotation, wrapping content or standing alone. |
| `FrameGlyph` | Nested-frame glyph (scanner / QR-eye indicator). |
| `RadiusGlyph` | Concentric-circle glyph whose inner disc scales with extent. |
| `DotsGlyph` | Fixed-geometry module glyph (dots) for QR / module previews. |

### feedback — status, progress, and notifications

| Component | Purpose |
|---|---|
| `Alert` | Slotted alert: icon + title + description + actions. |
| `AlertSimple` | Atomic alert container with free-form children. |
| `Banner` | Slotted full-width banner. |
| `BannerSimple` | Full-width status banner, typically pinned app-top. |
| `Callout` | Quieter `Alert`: colored left rule, no fill. |
| `Toast` | Slotted toast (visual only; queue / portal via `Toaster`). |
| `ToastSimple` | Atomic toast card with free-form children. |
| `Toaster` | Viewport that subscribes to the toaster store and renders toasts. |
| `FeedbackToasts` | `/feedback` bus → `Toaster` adapter; renders the toast viewport. |
| `UndoBar` | Snackbar with a single "Undo" action. |
| `Spinner` | Indeterminate loading spinner. |
| `InlineSpinner` | Spinner + label inline. |
| `Skeleton` | Loading placeholder shape. |
| `LoadingState` | Centered section / page loading: spinner + title + description. |
| `LoadingOverlay` | Scrim + centered spinner blocking a region during a task. |
| `ProgressBar` | Linear progress indicator. |
| `ProgressCircle` | Circular (SVG) progress indicator. |
| `ProgressSteps` | N-of-M progress dots / pills with connectors. |
| `MeterBar` | `ProgressBar` whose fill reflects threshold zones (green / amber / red). |
| `TrendIndicator` | Up / down / flat arrow + value + optional label. |
| `StatusIndicator` | Two-line status: colored dot + bold label + helper. |
| `PresenceIndicator` | Colored dot for presence (online / idle / busy / offline / invisible). |
| `TypingIndicator` | Three-dot "someone is typing" indicator. |
| `LiveCursor` | Remote-user cursor for collaborative canvases. |
| `NotificationCenter` | Notifications panel: header + count + action slot + empty state + footer. |
| `OnboardingChecklist` | First-run task list with progress; collapsible, auto-dismiss at 100%. |
| `Tour` | Multi-step product tour. |

### forms — inputs, pickers, editors, and form chrome

| Component | Purpose |
|---|---|
| `TextInput` | Single-line text input. |
| `TextAreaInput` | Multi-line text input. |
| `EmailInput` | `<input type="email">` with sensible defaults. |
| `UrlInput` | `<input type="url">` with url inputmode / autocomplete. |
| `TelInput` | `<input type="tel">` with tel inputmode / autocomplete. |
| `SearchInput` | Search input with a leading icon + clear button. |
| `PasswordInput` | Password input with an optional visibility toggle. |
| `PasswordStrength` | Strength meter for password fields. |
| `NumberInput` | Numeric input with stepper buttons. |
| `CurrencyInput` | `NumberInput` with a leading currency symbol. |
| `PercentInput` | `NumberInput` with a trailing `%` decoration. |
| `MaskedInput` | Text input with a character-class mask. |
| `PinInput` | OTP / PIN input: N cells with auto-advance + paste-spread. |
| `CharacterCount` | Character counter for limited fields; destructive past max. |
| `Checkbox` | Native checkbox with a custom visual. |
| `CheckboxField` | Checkbox + label + optional description in one `<label>`. |
| `CheckboxGroup` | Multi-select group of `CheckboxField` children. |
| `Radio` | Native radio with a custom visual. |
| `RadioField` | Radio + label + optional description in a `<label>`. |
| `RadioGroup` | Mutex group of `RadioField` children. |
| `ChoiceCard` | Radio styled as a clickable card (title + description + icon). |
| `Switch` | Toggle switch (native checkbox as an iOS track + thumb). |
| `SwitchField` | Switch + label + optional description in one `<label>`. |
| `Slider` | Single-value range slider (native, cross-browser styled). |
| `Knob` | Rotational dial input. |
| `Stepper` | Step progress indicator: ordered steps with active / complete state. |
| `Select` | Single-select dropdown: typed options, searchable registry, clearable. |
| `MultiSelect` | Multi-select dropdown; selected values render as removable tags. |
| `Combobox` | Text input + dropdown; type to filter / search options. |
| `Listbox` | Selectable option list — the primitive behind `Select` / `Combobox`. |
| `TagsInput` | Free-form tag entry. |
| `Field` | One-stop label + control + helper + error wrapper. |
| `LabeledInput` | Lighter `Field`: just label + control, no helper / error. |
| `Label` | `<label>` wired to FormControl context (auto `htmlFor` / `id`). |
| `Legend` | `<legend>` styled to match `Label`. |
| `Fieldset` | Semantic `<fieldset>` for grouping controls. |
| `FormHelperText` | Helper / hint text below a form control. |
| `FormErrorMessage` | Error copy under a form control. |
| `InputAddon` | Leading / trailing addon slots visually joined to an input. |
| `InputGroup` | Joins a row / column of inputs into one connected control. |
| `Calendar` | Standalone month-grid date picker (the block behind `DatePicker`). |
| `DateField` | Atomic `<input type="date">` styled; emits `Date`. |
| `DatePicker` | Date input with a `Calendar` popover. |
| `RangeCalendar` | Calendar that selects a `{ start, end }` range. |
| `DateRangePicker` | Date-range input with a `RangeCalendar` popover. |
| `TimeField` | Atomic `<input type="time">` styled; emits `{ hours, minutes }`. |
| `TimePicker` | Time input with an hour / minute popover. |
| `RecurrenceEditor` | Visual RRULE (RFC-5545) recurrence editor. |
| `CronInput` | Cron-string input with a human-readable preview. |
| `ColorSwatch` | Color preview chip. |
| `ColorField` | Hex color text input with a leading swatch; validates on blur. |
| `ColorArea` | 2D saturation / value picker square. |
| `ColorSlider` | Single-channel color slider (hue / sat / value / alpha). |
| `ColorWheel` | Circular hue picker (conic-gradient ring). |
| `ColorSwatchPicker` | Grid of preset color swatches; pick one. |
| `ColorPicker` | Color picker: swatch / hex trigger opening a popover (area + sliders). |
| `GradientPicker` | Visual gradient editor: kind / angle / stops. |
| `EmojiPicker` | Emoji picker: search + recents + category nav. |
| `EmojiSizeControl` | Emoji-size tile set previewing a glyph at each preset. |
| `ReactionPicker` | Quick-pick row of common emoji reactions. |
| `IconPicker` | Searchable icon-picker grid. |
| `FontPicker` | Font-family picker with live preview. |
| `FilePicker` | Styled trigger + hidden native file input. |
| `FileUpload` | Drag-drop file zone with a click-to-pick fallback. |
| `AddressForm` | Country-aware address form. |
| `PhoneInput` | International phone input: dial-code select + national number. |
| `KeyboardShortcutPicker` | Captures a key chord; emits the joined shortcut. |
| `Editable` | Inline-edit text: click to edit, commit on Enter / blur. |
| `CodeEditor` | First-gen code editor: textarea + line gutter + Tab indent. |
| `JSONEditor` | JSON editor with tree-view and raw-text modes. |
| `MarkdownEditor` | Markdown input + live preview. |
| `ChatComposer` | Chat input row: auto-resizing textarea + send button. |
| `Wizard` | Multi-step form flow with per-step validation + central state (`useWizard`). |

### layout — structural primitives and page frames

| Component | Purpose |
|---|---|
| `Box` | Lowest-level layout primitive (polymorphic element). |
| `Flex` | Bare flex container (no direction / gap opinions). |
| `Stack` | Vertical / horizontal flex container with gap + alignment. |
| `HStack` | Stack preset: row direction. |
| `VStack` | Stack preset: column direction (default). |
| `Grid` | CSS grid container with column + gap variants. |
| `Cluster` | Centered wrapping row (CTA clusters, footer links). |
| `Inline` | Wrapping horizontal row with a consistent gap. |
| `Center` | Flex shorthand centering children on both axes. |
| `Spacer` | Flexible empty box that pushes siblings apart. |
| `AspectRatio` | Constrains children to an aspect ratio. |
| `Container` | Centered max-width wrapper with horizontal padding. |
| `Section` | Full-bleed `<section>` band with an inner centered `Container`. |
| `TwoColumn` | Two-pane layout: fixed aside + flexible main. |
| `ControlGroup` | Labelled group of controls (label beside / above). |
| `Divider` | Rule / separator: plain (orientation required) or labelled "or". |
| `Surface` | Styled visual surface from the surface-variants matrix. |
| `Frame` | Bordered shell with padding + radius (`Card` without slots). |
| `ScrollArea` | Native scrollable container with stable visuals. |
| `ResizablePanel` | Split-pane layout with draggable separators. |
| `Overlay` | Positioned overlay anchored to its nearest positioned ancestor. |
| `AppShell` | Top-level page frame (Header / Sidebar / Main / Aside / Footer); sidebar collapses to a `Drawer`. |
| `Navbar` | Header band with start / center / end slots inside a `Container`. |
| `PullToRefresh` | Pull-to-refresh wrapper. |

### nav — menus, wayfinding, and navigation

| Component | Purpose |
|---|---|
| `Menu` | Raw floating menu primitive (bring your own anchor / state). |
| `DropdownMenu` | Button-triggered menu (the most common shape). |
| `ContextMenu` | Right-click menu opening at the pointer. |
| `Menubar` | Horizontal menu strip (File · Edit · View). |
| `NavigationMenu` | Top-level nav with rich content panels ("mega menu"). |
| `CommandPalette` | Cmd / Ctrl-K searchable action menu (modal combobox). |
| `NavItem` | Sidebar / nav row: icon + label + trailing slot + active state. |
| `Breadcrumb` | Linear position trail of links + separators. |
| `Pagination` | Compact page-number row with prev / next + ellipses. |
| `TableOfContents` | Heading outline (explicit items or auto-extracted). |
| `ScrollSpy` | Render-prop scroll-spy (active section by viewport). |

### overlays — modals, sheets, and floating panels

| Component | Purpose |
|---|---|
| `Modal` | Centered modal dialog: backdrop + focus-trap (compound subparts). |
| `AlertModal` | Confirm dialog requiring explicit action to close. |
| `Drawer` | Edge-anchored sliding panel (left / right / top / bottom) with focus-trap. |
| `BottomSheet` | Mobile bottom sheet with a drag handle + snap points. |
| `ActionSheet` | iOS-style action list sliding up from the bottom. |
| `Popover` | Click-triggered floating panel anchored to a trigger. |
| `HoverCard` | Hover / focus floating panel (richer than `Tooltip`). |
| `Backdrop` | Fixed-position scrim behind overlays. |

---

> **App instances — smart-qr reference frontend.** Concrete instances of the [`components.md`](components.md) §1 kinds. **Start = the codes (create-code) surface.** Marketing / billing / identity areas: TBD.

## Screens (routed; own a viewport section)

- `CreateCodeScreen` — the code builder (create, or edit when `codeId` set): a 3-tab card (Content · Design · Routing) + live preview + save.
- `CodesListScreen` — the owner's codes list: manage / edit / delete / toggle-active.

## Views (one tab body each; card + tab-strip stay in the screen) — *planned, Iter 7*

- `ContentView` — the Content tab: name, content-type select, the per-type controls.
- `DesignView` — the Design tab: fill / shape / emoji accordion + preview.
- `RoutingView` — the Routing tab: the ordered rule list.

## Design controls (`*Controls` — a labeled input group bound to one style slice)

- `FillControls` — foreground fill: solid color or a linear/radial gradient (presets + stops).
- `ShapeControls` — module (body) shape + finder-eye external/internal shapes.
- `EmojiControls` — center-emoji picker + per-emoji size (thin app wrapper over SDK `EmojiPicker`).
- `ContrastCallout` — passive WCAG scannability guardrail; warns on low / inverted contrast, else silent.

## Preview

- `QrPreview` — live, debounced, server-rendered SVG preview — byte-parity with the downloadable asset.

## Routing controls

- `RuleControls` — ordered first-match routing rules (condition → destination); drag-reorder.

## Content controls (`*Controls` — per content-type input groups)

- `ContentTypeControls` — dispatcher: renders the chosen type's control group (`id → component`) + its note.
- `UrlControls` · `MobileAppControls` · `TextControls` · `EmailControls` · `SmsControls` · `PhoneControls` · `GeoControls` · `WifiControls` · `VCardControls` · `CalendarControls` — each renders its content type's field group.

## Field primitives (`*Field` — one labeled input; `fields.tsx`)

- `TextField` — single-line text-like input (SDK `TextInput`).
- `TextAreaField` — multi-line native `<textarea>`, styled to match the SDK input.
- `DateTimeField` — native `datetime-local`, styled to match.
- `SelectField` — SDK `Select` over `{ value, label }` options.
- `FieldRenderer` — dispatches a registry field to the right `*Field` by `FieldKind`.

## Display maps (`*Displays` — enum → label / icon / swatch; co-located data, not components)

- `ShapeDisplays` · `GradientPresets` · `BarcodeFormatDisplays` · `RuleConditionTypeDisplays` — the enum → display metadata each control renders from.
