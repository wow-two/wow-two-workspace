# Extensions

*Last updated: 2026-08-16*

> The static-logic tier over a domain's types.
> Purpose — keep dependency-free behaviour off the type it extends, without inventing a service for it.
> Use case — reach here for encoding, projection or registration logic that needs no collaborators.

## Location

### Folder
- must sit in an `Extensions/` folder beside the domain it extends.

### File
- must give each extensions class its own file, named for the type.

## Declaration

### Type doc


- must start with **Extends**, then `<see cref>` the target, then `for {purpose}`.
- must name the purpose category, never the methods it holds.

```csharp
// ✅
/// <summary>Extends <see cref="WifiContentValueObject"/> for payload encoding.</summary>
// ❌ names the additions, which change with every method
/// <summary>Extends <see cref="WifiContentValueObject"/> with Encode and Parse.</summary>
```

### Type name
- must declare `public static class {Domain}Extensions`, named for the vector.

```csharp
// ✅ the vector
public static class WifiContentExtensions
// ❌ one target, so the class cannot grow
public static class WifiSsidEncodingExtensions
```

## Content

### Member docs


- must start the `<summary>` with the method's own verb — `Adds`, `Maps`, `Encodes`.
- must carry a `<param>` for every parameter, the receiver included.
- must carry `<returns>` unless the method returns `void`, `Task` or `ValueTask`.
- must carry `<remarks>` only for a directive, a spec reference, or a constraint the signature hides.

```csharp
// ✅
/// <summary>Encodes the content as a WIFI URI payload.</summary>
/// <param name="content">The content to encode.</param>
/// <returns>The payload string.</returns>

// ❌ a parameter set that is complete or the doc is wrong
/// <summary>Encodes the content as a WIFI URI payload.</summary>
```

### Members
- must take the receiver as a `this` parameter or as a plain argument.
- must be reachable by its type name at the call site.
- may be `async` when the receiver's own work is asynchronous, returning `Task<T>` or `ValueTask<T>`.
- may use `=>` for a member that returns or delegates — extensions take no collaborators to accumulate
  ([style](../notation/style/style.md) § *The body*).
- must produce its result from the receiver and its arguments alone — a method that joins two collaborators' results is a `Service`.
- must declare a constant here when this class is its only caller, and in a `Constants` class the moment a second caller appears.
- must order constants first, then methods.

```csharp
// ✅ the receiver and its own constant, nothing reached for
private const string PayloadShape = "WIFI:T:{0};S:{1};P:{2};;";

public static string ToPayload(this WifiContentValueObject content) =>
    string.Format(PayloadShape, content.Encryption, content.Ssid, content.Password);

// ❌ bridges two collaborators, so it is a Service
public static string ToPayload(this WifiContentValueObject content, IFormatBroker broker, IStyleClient client) =>
    broker.Render(content, client.GetTheme());
```

## See also

- [summary](../notation/documentation/summary.md) — the starter table
- [components](../../mla/components/components.md) — the suffix keep-list
