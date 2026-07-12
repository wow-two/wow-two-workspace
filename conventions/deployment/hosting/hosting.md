# Conventions — Deployment — Hosting

*Last updated: 2026-07-12*

> Where a product runs and how it is served — the single deployable's serving model + the shared dev-port ledger.

| File | Covers |
|---|---|
| [single-host-serving.md](single-host-serving.md) | Backend serves the SPA from `wwwroot` — vite `outDir` + static-serve/fallback + `BuildSpa` MSBuild target + dev proxy + CORS posture |
| [ports.md](ports.md) | Port ledger — allocated dev ports (check before picking one) |
