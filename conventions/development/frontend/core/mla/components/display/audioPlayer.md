# AudioPlayer

*Last updated: 2026-08-19*

> Audio with the app's own transport — play, scrub, volume, speed.
> What a display is → [display](../../constructs/visual/display.md).
> Its full surface → `AudioPlayer.spec.md`.

## Reach for it when

- must play a recording inside the page — a voice note, a track, an episode
- must pass `peaks` to swap the plain scrubber for a waveform
- should read position from `@time-update` rather than reaching for the element

---

## Instead of

| Reach for | When |
|---|---|
| [AudioWaveform](audioWaveform.md) | only the waveform is wanted, with no transport |
| [VideoPlayer](videoPlayer.md) | the media has picture as well as sound |
| `<audio controls>` | the browser's own chrome is acceptable |

---

## Values

- should leave `defaultVolume` at `1` and `defaultPlaybackRate` at `1`
- must leave `autoPlay` unset unless the page exists to play — browsers reject it anyway
- should set `isCompact` where the player sits inside a row rather than owning a block
