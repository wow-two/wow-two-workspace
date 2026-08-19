# AudioWaveform

*Last updated: 2026-08-19*

> The bar waveform — amplitudes drawn as SVG, optionally seekable.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `AudioWaveform.spec.md`.

## Reach for it when

- must show a clip's shape without a full transport — a message row, a preview
- must hand in `peaks` already normalised to `0..1`; it resamples, it never decodes
- should pass `onSeek` when the bars should be clickable and arrow-key seekable

---

## Instead of

| Reach for | When |
|---|---|
| [AudioPlayer](audioPlayer.md) | the reader needs play, volume and speed too |
| [Sparkline](sparkline.md) | the series is data rather than audio amplitude |

---

## Values

- should leave `width` at `320`, `height` at `48`, `barWidth` at `2`, `gap` at `1`
- should leave `tone` at `brand`
- must leave `isInteractive` unset; it falls back to whether `onSeek` was passed
