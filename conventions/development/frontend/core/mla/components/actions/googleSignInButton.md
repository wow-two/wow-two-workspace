# GoogleSignInButton

*Last updated: 2026-08-19*

> Google's own sign-in control, drawn by GIS — the one button here whose pixels are not ours.
> What an action is → [action](../../constructs/visual/action.md).
> Its full surface → `GoogleSignInButton.vue`.

## Reach for it when

- must reach for it for the Google ID-token sign-in flow
- must reach for it over a Google-styled house button — their branding is required
- should render it only where a `clientId` is set; without one, guest-only

---

## Instead of

| Reach for | When |
|---|---|
| [Button](button.md) | sign-in runs against the product's own identity endpoint |

---

## Values

- must treat the credential as an ID token, not a session — verify it server-side
- must keep `width` at or below the `400` px GIS cap; omit it to size to the host
- should set `locale` only when the app's language differs from the browser's
- should leave `autoSelect` off unless a returning user may sign in without a click
