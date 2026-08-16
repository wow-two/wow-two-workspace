# Exceptions

*Last updated: 2026-08-16*

> The `<exception>` block — document only the exceptions a method throws itself, not propagated ones.

## Exceptions

- must document the exceptions a method throws **itself**, never one propagated from a callee.
- must write the block as `/// <exception cref="…">{trigger}</exception>`.

```csharp
// ✅ the trigger, on an exception this method raises
/// <exception cref="MigrationDriftException">An applied migration's checksum no longer matches its source.</exception>
```
