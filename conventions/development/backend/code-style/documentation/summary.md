# Summary

*Last updated: 2026-06-22*

> The `<summary>` block — its mandated first word per type-kind (the starter table) + tone. The canonical summary reference; every convention links here.

## Starter table (REQUIRED)

The first word of every `<summary>` is fixed by type-kind. This is the canonical reference — every other file in `conventions/` links here.

| Type-kind | Starter | Example |
|---|---|---|
| Interface | **Defines** | `Defines the contract for stamping audit fields on save.` |
| Enum | **Defines** | `Defines the execution status of a pipeline run.` |
| Enum value | **Represents** | `Represents a run that finished successfully.` |
| Entity / record / model class | **Represents** | `Represents an external listing channel.` |
| DTO | **Represents** (or describe projection) | `Represents a flat channel projection for the CRM grid.` |
| Service | **Provides** | `Provides channel and pipeline seeding on application startup.` |
| Client (HTTP wrapper) | **Wraps** or **Integrates with** | `Wraps the Telegram Bot API for sending messages and managing topics.` |
| Factory | **Creates** | `Creates AI clients keyed by provider + model tier.` |
| Repository | **Fetches** (read-heavy) or **Persists** (write-heavy) | `Fetches unclassified listings via Dapper.` |
| CQRS marker / handler interface (`IQuery`, `ICommand`, `IQueryHandler`, …) | **Defines** | `Defines a query that returns <typeparamref name="TResult"/>.` |
| Query/Command (concrete CQRS message) | **Represents** | `Represents a query to get all channels with their pipelines and sources.` |
| Query/Command handler | **Handles `<see cref="X"/>`** | `Handles <see cref="ChannelGetAllQuery"/>.` |
| Static constants class | **Contains** | `Contains the canonical kebab-case slugs for every channel.` |
| Constant field (`const` / `static readonly`) | **Holds** | `Holds the token an open network carries in a WIFI payload.` |
| Static registry class | **Tracks** or **Holds** | `Tracks live pipeline executions keyed by pipeline id.` |
| Extension class | **Extends** | `Extends <see cref="WifiEncryption"/> with its WIFI-URI spelling.` |
| Extension method | (verb at start: `Adds`, `Uses`, `Maps`, `Configures`) | `Adds the JWT bearer authentication scheme with sane defaults.` |
| Configuration class (settings record) | **Configuration for** | `Configuration for AI classification pipeline behavior.` |
| EF `IEntityTypeConfiguration<T>` class | **Configures** | `Configures the listings table mapping and relationships.` |
| HostConfiguration extension | **Configures** | `Configures typed HTTP clients for external API integrations.` |
| Hosted service | **Runs** or **Schedules** | `Runs EF Core migrations on application startup with connect-retry.` |
| Result base (abstract) | **Represents the outcome of** | `Represents the outcome of reading seed data for an entity type.` |
| Result `Success` variant | (describe the success state) | `Seed data read successfully — entities ready for upsert.` |
| Result `Failure` variant | (describe the failure state) | `Seed data read failed — error tracked for diagnostics.` |
| Property (read-only) | **Gets** | `Gets the kebab-case slug of the channel.` |
| Property (read-write) | **Gets or sets** | `Gets or sets the kebab-case slug of the channel.` |
| Method (action) | Verb at start: `Adds`, `Gets`, `Creates`, `Sends`, `Configures`, `Maps`, `Builds` | `Sends the OTP to the resolved Telegram chat.` |
| Controller (class) | **Manages** (resource) · **Reports** (non-resource) | `Manages portfolio products.` · `Reports the vault's seal state.` |
| Controller action | Verb at start (HTTP method shape): `Gets`, `Creates`, `Updates`, `Deletes`, `Executes`, `Cancels` | `Gets all channels with their pipelines.` |
| Request model (`{Verb}{Noun}ApiRequest`) | **Represents** | `Represents the create-code request body.` |

A doc violating the starter table is a style miss regardless of content quality.

**Enum type vs value:** the enum *type* uses **Defines** (it declares the closed set); each *value* uses **Represents** (it is one data case). This is the same split as everywhere — `Defines` the type/contract, `Represents` the instance/case/message. (Chosen over `Refers to`, which implies an indirection an enum value doesn't have.)

**Defines / Represents / Handles** — the CQRS verb trio, by layer: **Defines** an interface / marker definition · **Represents** a concrete message model · **Handles** a handler. Same three verbs apply to the mediator markers — see [mediator.md](../../messaging/mediator.md) (§ Comment conventions).

## Summary — tightest accurate sentence

- One sentence. Start with the mandated starter word.
- For **capability interfaces** (entity traits with members), prefer `Defines a/an {noun} {that|with} {capability}` over `Defines the contract for {types} that {verb}…`. Shorter, same meaning.
  - ✅ `Defines an entity with creation and update timestamps.`
  - ❌ `Defines the contract for entities that participate in timestamp auditing — CreatedAt populated on insert, UpdatedAt on every update.`
- For an **empty marker interface** (no members — it tags a category rather than imposing a shape), use `Defines the marker for {X}`. Don't call it a "shape" — a marker has none. When the tagged concept is broad, define it inline with an em-dash.
  - ✅ `Defines the marker for an entity — a type persisted to a data store.`
- For **behavior interfaces** (handlers, stampers, service-shaped contracts), `Defines the contract for {action}` is fine — there's no noun to name.
- Don't spill member-level detail into the type summary — the members carry it.
- Drop filler: `the SDK convention`, `with a custom X type` (the type parameter is already visible in the signature).

## Constants

`Holds` — a member-sized verb, matching how properties take `Gets`. **Not `Defines` / `Represents`**: those are type-kind starters, and a `const` is a member. It has no accessor either, so no `Gets`.

- **must not restate the value** — `= "WPA"` is on the line; `Represents the WPA token` says nothing the reader can't see
- **must name the authority that fixes the value** when one exists — a spec, a wire format, a third-party contract. That is the fact the literal alone hides: `"nopass"` is unguessable until you know the WIFI URI scheme mandates it
- **may omit the summary entirely** when the enclosing type already carries the authority and the name is plain. A `private const` is an internal member; a comment on each one restates the group's summary N times
- **a format-string constant documents its shape, never its slots** — `Holds the payload shape of a WIFI URI.` The `{0}`…`{n}` are visible; what a reader needs is which spec the shape comes from
- **must not comment a constant that exists only to name a magic number in place** — `private const int MaxNameLength = 200;` is already self-describing

## Extract a format string when the literal has structure

A literal with fixed structural parts is a **contract shape**, not an implementation detail.

- must lift a payload / URI / template literal into a named `const` and build it with `string.Format` once it carries any constant segment beyond a single prefix
- the constant then shows the whole shape in one place, which interpolation scatters across the expression
- a bare prefix (`$"tel:{phone}"`) stays inline — there is no shape to see
- keep the segments that appear conditionally as their own constants, so the parent shape stays readable

## Extension classes

`Extends`, not `Provides`. An extension class hosts methods bolted onto a type it does not own — it supplies no behaviour of its own, so the service starter overstates it.

`Extends <see cref="X"/> for {purpose}.` — the target, then the **purpose category**.

- `Extends <see cref="WifiContentValueObject"/> for payload encoding.`
- **name the purpose, not the additions** — what a class adds changes every time a method lands; why it exists does not
- **cref the target when there are one or two** — the reader clicks through
- **use an abstract name when the targets are many or open** — `Extends the host builder for observability wiring.` A list of crefs stops being readable past two, and an open target set has nothing to cref
- individual extension methods keep a verb start (`Adds`, `Maps`, `Builds`)

## Expression body vs block

- **block body by default.** An expression body is for a single trivial delegation or a direct member return
- ✅ `public override string Encode() => this.ToPayload();`
- ✅ `public string Slug => _slug;`
- ❌ an expression body whose expression wraps across lines, takes several parameters, or contains a conditional — that wants a block
- the tell: if the `=>` expression needs line breaks to read, it is a method body pretending to be an expression

## Properties on entities + DTOs

- Start with `Gets` or `Gets or sets` — always state what the property holds, even if obvious from name
- **`{ get; init; }` takes `Gets`** — the setter closes after construction, so a consumer only ever gets
- **Applies to every C# model kind**, value objects included. A bare noun phrase (`The network name.`) is the TypeScript style — TS has fields, C# has properties, and the accessor is what the starter names. Don't carry the frontend's phrasing across
- **A method that produces a formatted payload gets `<inheritdoc />` + `<remarks>`, not a re-described `<summary>`.** The format string lives in the code; a summary spelling it out (`Builds the <c>WIFI:T:…;S:…;;</c> payload`) restates it and goes stale. `<remarks>` carries only what the code doesn't show — escaping rules, an omitted segment, a spec quirk
- Always state the parent entity context: `Gets or sets the kebab-case slug of the channel`, not `Gets or sets the slug`
- PKs / FKs: `<summary>` like every other member — state what the key identifies
- **State what the value is — not who sets it, when, or how.** No "stamped by the interceptor", "populated by the DB", "set at construction". An entity-trait contract describes the field; the population mechanism (interceptor, trigger, app code) is the implementer's choice and must not leak in.
  - ✅ `Gets or sets the timestamp when the entity was created.`
  - ❌ `Gets or sets the UTC timestamp when the entity was created. Stamped by the audit interceptor on insert; preserved on every subsequent update.`
- **Don't restate type-implied facts** — `DateTimeOffset` is already a timestamp (don't write "UTC timestamp"); an interface named `IHasXmin` already implies Postgres (don't repeat "Postgres xmin" on the member)
