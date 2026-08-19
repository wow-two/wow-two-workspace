# VideoPlayer

*Last updated: 2026-08-19*

> Video with the app's own transport, auto-hiding controls and keyboard shortcuts.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `VideoPlayer.spec.md`.

## Reach for it when

- must play a clip in the page with chrome that matches the app
- must pass `tracks` for captions — they render as native `<track>` children
- should give it a `poster`, so the frame is not blank before the first play

---

## Instead of

| Reach for | When |
|---|---|
| [AudioPlayer](audioPlayer.md) | the media is sound only |
| [Image](image.md) | a still frame is enough |
| `<iframe>` | the video is hosted and played by a third party |

---

## Values

- should leave `aspectRatio` at `16 / 9`, `defaultVolume` and `defaultPlaybackRate` at `1`
- must leave `autoPlay`, `loop`, `muted` unset; the native element defaults them
- must autoplay muted or not at all — an unmuted autoplay is rejected
