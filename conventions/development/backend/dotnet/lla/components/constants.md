# Constants

*Last updated: 2026-08-16*

> A static class holding values the codebase names once.
> Purpose — one home for a value's authority, so a literal never has to be explained twice.
> Use case — reach here when a value is fixed by a spec, a wire format, or a third-party contract.

## Location

### Folder
- must sit in a `Constants/` folder beside the code that owns the values.

### File
- must give each constants class its own file, named for the type.

## Declaration

### Type doc

#### [Summary](../notation/documentation/summary.md)
- must start with **Contains**.
- must name the set the values belong to.

```csharp
// ✅
/// <summary>Contains the canonical kebab-case slugs for every channel.</summary>
// ❌ names no set
/// <summary>Contains constants.</summary>
```

### Type name
- must declare `public static class {Name}Constants`, or `{Name}` when the noun already reads as a set.

```csharp
// ✅
public static class ChannelSlugs
// ❌ the suffix says nothing the noun does not
public static class ChannelSlugsConstants
```

## Content

### Member docs

#### [Summary](../notation/documentation/summary.md)
- must start with **Holds**.
- must name the authority that fixes the value — a spec, a wire format, a third-party contract.
- must state the shape of a format string, never its slots.

#### [Remarks](../notation/documentation/remarks.md)
- must carry `<remarks>` only to name the spec the value answers to — `Follows RFC 6068.`

```csharp
// ✅ the authority, not the literal
/// <summary>Holds the token an open network carries in a WIFI payload.</summary>
public const string OpenNetwork = "nopass";

// ❌ restates what the line already shows
/// <summary>Holds the value "nopass".</summary>
```

### Members
- must use `const` for a compile-time value, `static readonly` for anything else.
- must assign a literal, or an expression built from literals declared above it.
- must order from the primitive value to the composed one, or in the order the flow consumes them.
- must separate every constant from the next with one blank line.
- must split a group into its own file once the class passes 60 lines — regions hide length, files state it.

```csharp
// ✅ literals, primitive first, the composed shape after
public const string Scheme = "WIFI:";
public const string PayloadShape = Scheme + "T:{0};S:{1};P:{2};;";

// ❌ reaches out for its value, so the class no longer holds the authority
public static readonly string PayloadShape = WifiFormats.BuildShape();
```

## See also

- [../notation/documentation/summary.md](../notation/documentation/summary.md) — the starter table
- [../notation/style/style.md](../notation/style/style.md) — lifting a structured literal into a named `const`
