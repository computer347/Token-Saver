## Interface contract — step 4: reports and command line

**`homeledger/reports.py`**
- `monthly_summary(transactions) -> dict` — keys are `"YYYY-MM"` in ascending order; each value is `{"income": Decimal, "expense": Decimal, "net": Decimal}`, where income sums positive amounts, expense sums outflows as a positive number, and `net = income - expense`.
- `category_breakdown(transactions, month: str) -> list[tuple[str, Decimal]]` — outflows in that month per category, as positive numbers, sorted by amount descending then name; an empty category is reported as `"uncategorized"`.
- `top_payees(transactions, n=5) -> list[tuple[str, Decimal]]` — total outflow per non-empty payee, same ordering, at most n.

**Command line: `python -m homeledger.cli --data PATH COMMAND ...`** (the module must be runnable this way). The store is chosen with `store_for(PATH)`. On any `HomeLedgerError`, print `error: <message>` to stderr and exit with code 2; otherwise exit 0. Every command below accepts `--json`, which prints exactly one JSON value to stdout. In JSON output, money is a string with two decimals (`"-12.50"`) and transactions use `Transaction.to_dict()`.

- `account add ID NAME [--currency EUR] [--kind checking]` — JSON: the account's `to_dict()`.
- `account list` — JSON: a list of account dicts.
- `add ACCOUNT DATE AMOUNT PAYEE [--category C] [--memo M] [--tag T]...` — validated with `validate_transaction`; the currency is the account's; an unknown account is an error. Generates a unique id. JSON: the new transaction's dict.
- `import ACCOUNT FILE` — `import_csv` then `merge_imported` against existing transactions; saves the added ones. JSON: `{"imported": N, "skipped": M}`.
- `report monthly` — JSON: `{"YYYY-MM": {"income": "...", "expense": "...", "net": "..."}, ...}`.
- `search QUERY` — JSON: list of matching transaction dicts.
- `budget set CATEGORY LIMIT [--rollover] [--cap N]` — creates or replaces the budget for the category (lower-cased).
- `budget status --month YYYY-MM` — JSON: a list of `{"category", "available", "spent", "remaining"}` for every budget.
