# SQL Authoring

*Last updated: 2026-06-18*

> Apply/Rollback dialect idioms for the bespoke migrator — Postgres and SQLite today, SqlServer later.
> Purpose — the engine runs `.sql` verbatim (no auto-quote, rewrite, or portability check), so per-provider
> correctness is the author's job.
> Use case — hand-writing a migration's `Apply.sql` / `Rollback.sql` and needing the dialect-correct form.

---

## Scope

- engine lifecycle + file layout → [bespoke-migrations.md](bespoke-migrations.md); this doc is dialect idioms only.
- must not confuse it with the engine's internal `IMigrationDialect` seam (SDK `Bespoke/bespoke.md`) — that seam
  owns the migrator's *own* SQL (advisory lock, `migration_history` DDL), not your migration SQL.

---

## Postgres

> The default dialect — every rule in this section is Postgres-specific.
> SQLite is covered in `## SQLite` below; SqlServer gets a sibling section when that track lands.

### Reserved-word quoting

- must hand-quote every reserved word — the engine does not auto-quote (EF does): `"order"`, `"user"`, `"group"`.
- must quote it everywhere the column appears — `CREATE TABLE`, every index, every constraint, every `Rollback.sql`.
- canonical example — `routing_rules."order"` in `001-baseline/Apply.sql`:

```sql
CREATE TABLE routing_rules (
    id       uuid    NOT NULL,
    "order"  integer NOT NULL,
    ...
);
CREATE INDEX ix_routing_rules_code_id_order ON routing_rules (code_id, "order");
```

- should rename around a reserved word while the schema is still fluid.
- must quote only when the column name is load-bearing — a domain term like `order`.

---

### Rollback idioms

- must ship with every `Apply.sql` a `Rollback.sql` that inverts it — a missing one fails the scan.
- at run time rollback is a guarded recovery op, gated by `MigrationOptions.AllowRollback`.
- roll forward by default; rollback is prod-allowed for recovery.
- mandate + gating → [bespoke-migrations.md](bespoke-migrations.md).
- must drop in reverse dependency order — children before parents, inverting Apply's create order.
- a child holding an FK to a parent can't be dropped once the parent is gone.
- must put `IF EXISTS` + `CASCADE` on every drop — the script must be safe on partial state.
- partial state is a half-applied `@no-transaction` Apply, or a re-run.
- `001-baseline` is the reference — Apply creates `codes` → `routing_rules` → `scan_events`.
- its `Rollback.sql` drops the reverse:

```sql
DROP TABLE IF EXISTS scan_events CASCADE;
DROP TABLE IF EXISTS routing_rules CASCADE;
DROP TABLE IF EXISTS codes CASCADE;
```

- `CASCADE` also clears dependent objects the Apply created implicitly (FKs, indexes) — drop the table, not its parts.
- invert `ALTER TABLE ... ADD COLUMN` with `ALTER TABLE ... DROP COLUMN IF EXISTS`.
- invert `CREATE INDEX` with `DROP INDEX IF EXISTS`.
- a native-enum `ADD VALUE` is not rollback-able — PG can't drop an enum label.
- must leave a no-op `Rollback.sql` with a comment saying so, and roll forward instead.

---

### `@no-transaction` idempotency

- default — the engine wraps each file in a per-file transaction (PG transactional DDL).
- a failed Apply leaves zero partial schema, so plain non-idempotent DDL is fine.
- a file led by `-- @no-transaction` runs outside a transaction and records separately.
- a crash mid-file leaves it partially applied and unrecorded, so the next run re-executes it.
- the directive + recording semantics are the engine's ([bespoke-migrations.md](bespoke-migrations.md)).
- the idempotency idioms below are the author's.
- must make a `@no-transaction` Apply idempotent — re-running it on a partially-applied state must succeed.

Idempotency idioms:

| Idiom | Use |
|---|---|
| `CREATE INDEX CONCURRENTLY IF NOT EXISTS …` | the common case — concurrent index build |
| `IF NOT EXISTS` / `IF EXISTS` on every `CREATE`/`DROP`/`ALTER` | guards re-execution |
| guarded `DO $$ … $$` block | conditional logic a bare `IF NOT EXISTS` can't express |

```sql
-- @no-transaction
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_codes_user_id ON codes (user_id);
```

```sql
-- @no-transaction
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'code_status') THEN
        CREATE TYPE code_status AS ENUM ('active', 'paused');
    END IF;
END $$;
```

**Statements that forbid a transaction** (must carry `-- @no-transaction`):

| Statement | Why |
|---|---|
| `CREATE INDEX CONCURRENTLY` | concurrent build can't run inside a tx block |
| `ALTER TYPE … ADD VALUE` | new enum label not usable in the same tx that adds it (PG) |
| `VACUUM` / `VACUUM FULL` | maintenance commands forbid a tx block |
| `REINDEX … CONCURRENTLY` | same concurrent-build constraint |

- should keep a `@no-transaction` file single-statement where possible.
- each statement autocommits independently, so a multi-statement file has more partial-failure points to guard.

---

### Native enum changes

- adding a value to a native PG enum is a migration — `ALTER TYPE foo_status ADD VALUE 'archived'`.
- `ADD VALUE` cannot run in a transaction → the file must be `-- @no-transaction`:

```sql
-- @no-transaction
ALTER TYPE code_status ADD VALUE IF NOT EXISTS 'archived';
```

- `IF NOT EXISTS` on `ADD VALUE` makes it idempotent — required by the `@no-transaction` rule above.
- a brand-new enum type (`CREATE TYPE … AS ENUM (…)`) can run in a normal transactional migration.
- only `ADD VALUE` against an existing type forces `@no-transaction`.
- the C#/EF side maps the enum with `NpgsqlDataSourceBuilder.MapEnums(CaseStyle.Snake, …)` via
  `PostgresServiceCollectionExtensions` → [postgres](../../database/postgres/postgres.md) § *Enum column mapping*.
- must author the SQL label in snake_case — PascalCase C# `Archived` ↔ PG label `'archived'`.

---

### Schema-mirror discipline

- must treat Apply SQL as the schema-first source of truth — EF maps over it, never generates it.
- the ownership rule lives in [bespoke-migrations.md](bespoke-migrations.md) and `database.md`.
- must write columns to mirror the EF model the product already uses.
- snake_case names · enums as a native type (text on non-PG) · `jsonb` for JSON · `timestamptz` for instants.
- `001-baseline/Apply.sql` is the worked example — see its header comment.
- must name constraints explicitly, so `Rollback.sql` and later `ALTER`s can reference them by name —
  `CONSTRAINT pk_codes PRIMARY KEY (id)` · `CONSTRAINT fk_routing_rules_codes_code_id FOREIGN KEY (code_id)
  REFERENCES codes (id) ON DELETE CASCADE`.

---

## SQLite

> The `Sqlite` dialect (SDK `Bespoke/bespoke.md`) — for drydock / secrets-vault and any SQLite-backed product.
> Select it with `MigrationOptions.Provider = DatabaseProvider.Sqlite` + `AddSqliteConnectionFactory(connectionString)`.
> Authoring differs from Postgres in types, enums, `ALTER TABLE`, foreign keys, and transactionality.

### Type affinity

- SQLite has five affinities — `INTEGER`, `TEXT`, `REAL`, `BLOB`, `NUMERIC` — not rich types.
- must write columns to mirror the EF model's *stored* shape.
- EF-on-SQLite mappings — GUID → `TEXT` · bool → `INTEGER` (0/1) · `byte[]` → `BLOB`.
- enum → `INTEGER` (ordinal); `DateTimeOffset` → the product's converter.
- drydock / secrets-vault use `DateTimeOffsetToBinaryConverter` → `INTEGER`.
- the migrator's own `migration_history` uses `TEXT`.
- must match what the product's EF model already stores, so EF round-trips the migrated schema.
- `INTEGER PRIMARY KEY` is the rowid alias (autoincrement); a GUID PK is `id TEXT NOT NULL PRIMARY KEY`.

### No native enums

- SQLite has no enum type — store enums as `INTEGER` (ordinal) or `TEXT`.
- optionally guard the column with `CHECK (status IN (0, 1, 2))`.
- there is no `ALTER TYPE … ADD VALUE` migration — adding an enum member is a code-only change, not a schema change.

### Reserved-word quoting

- same as Postgres — double-quote reserved words: `"order"`, `"group"`, `"user"`.
- SQLite also accepts backticks / `[brackets]`; prefer the standard double quote.
- must quote it everywhere the column appears, `Rollback.sql` included.

### Transactional DDL + `@no-transaction`

- SQLite has transactional DDL like Postgres — a file's transaction rolls back cleanly on failure.
- plain non-idempotent DDL is therefore fine in a normal migration.
- there is no `CREATE INDEX CONCURRENTLY` — indexes build inside the transaction.
- must not mark an index migration `@no-transaction`.
- `@no-transaction` is rarely needed here — the realistic case is a connection `PRAGMA` that can't run inside a
  transaction, e.g. `PRAGMA journal_mode = WAL`.
- the same idempotency rule applies when used — `CREATE INDEX IF NOT EXISTS`, guarded statements.

### Limited `ALTER TABLE`

- SQLite `ALTER TABLE` supports only `ADD COLUMN`, `RENAME TO`, `RENAME COLUMN`, `DROP COLUMN` (3.35+).
- there is no `ALTER COLUMN` type or constraint change.
- must use the table-rebuild pattern in the Apply for anything else — a type change, a constraint add/drop, a reorder.
- `CREATE` the new table → `INSERT INTO new SELECT … FROM old` → `DROP TABLE old`
  → `ALTER TABLE new RENAME TO old`, recreating indexes.
- must invert the rebuild in `Rollback.sql`.

### Foreign keys

- SQLite enforces FKs only when `PRAGMA foreign_keys = ON` is set per connection — off by default.
- declaring the FK in DDL is necessary but not sufficient.
- the host must set the pragma on every connection for `ON DELETE CASCADE` etc. to fire.

### Rollback + schema-mirror

- same discipline as Postgres — every `Apply.sql` ships an inverting `Rollback.sql`.
- reverse dependency order · `DROP TABLE IF EXISTS` · drop the table, not its parts.
- Apply SQL is the schema-first source of truth EF maps over, never generates.
