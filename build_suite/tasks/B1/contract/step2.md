## Interface contract — step 2: storage

All of the following live in **`homeledger/storage.py`** (importable as `from homeledger.storage import ...`).

- `LedgerData` — dataclass with `accounts: dict[str, Account]` (keyed by id), `transactions: list[Transaction]` (insertion order kept), `budgets: dict[str, Budget]` (keyed by category). All default to empty.
- `JsonStore(path)` — `load() -> LedgerData` returns an empty `LedgerData` if the file doesn't exist or is empty; `save(data)` writes `{"schema_version": 3, "accounts": [...], "transactions": [...], "budgets": [...]}` using each model's `to_dict()`. `load()` always runs `migrate()` first.
- `SqliteStore(path)` — the same `load()`/`save()` interface backed by `sqlite3`. Saving and loading must round-trip every field exactly, including Decimal amounts and tag order.
- `store_for(path)` — returns a `SqliteStore` for `.db`, `.sqlite` or `.sqlite3` files, a `JsonStore` for anything else.
- `migrate(raw: dict) -> dict` — upgrades a stored JSON document to schema version 3 without mutating its argument:
  - **Version 1** (no `schema_version` key): accounts may lack `kind` (default `"checking"`) and `currency` (default `"EUR"`). Each transaction has `amount` as a positive string that may use a decimal comma (`"12,50"`), a `type` of `"income"` or `"expense"` (expense becomes a negative amount; the `type` key is removed), and no `currency` (use its account's currency, else `"EUR"`). Any other `type` raises `MigrationError`.
  - **Version 2**: `tags` is a comma-separated string (`"a, b"`); convert it to a list of stripped, non-empty strings.
  - **Version 3**: returned unchanged (as a copy).
  - A version newer than 3, or a non-integer version, raises `MigrationError`.
