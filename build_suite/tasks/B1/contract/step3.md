## Interface contract — step 3: features

**`homeledger/importers.py`**
- `ColumnMapping(date="date", amount="amount", payee="payee", memo=None)` — frozen dataclass naming the CSV columns (matched case-insensitively).
- `import_csv(text: str, account_id: str, mapping: ColumnMapping | None = None, currency: str = "EUR") -> list[Transaction]` — the first line is a header; the delimiter is auto-detected among `,`, `;` and tab. Blank lines are skipped. Amounts use `parse_amount`, dates `parse_date`. A missing column raises `ImportFormatError` with `line == 1`; a bad row raises `ImportFormatError` whose `line` is that row's 1-based line number in the text. Every imported transaction gets a non-empty `id` and `imported_id`; both are deterministic (the same input gives the same values) and unique within one import, even when two rows are identical.
- `is_duplicate(a, b, window_days: int = 3) -> bool` — true when both are on the same account, have the same amount, their dates are at most `window_days` apart, and their payees are similar: `difflib.SequenceMatcher` ratio ≥ 0.8 after lower-casing and collapsing whitespace. If either payee is empty, payee similarity is not required.
- `merge_imported(existing, incoming) -> (added, skipped)` — incoming transactions that duplicate any existing one go to `skipped`, the rest to `added`, both in input order.

**`homeledger/rules.py`**
- `Rule(conditions: list[str], category: str | None = None, tags: tuple = (), priority: int = 0)` — conditions are strings: `payee~text` (case-insensitive substring), `payee=text` (case-insensitive equality), `memo~text`, `memo=text`, and `amount<N`, `amount<=N`, `amount>N`, `amount>=N`, `amount=N` (compared with the signed Decimal amount). A rule with no conditions, or any malformed condition, raises `ValidationError` when the `Rule` is created. All conditions must match.
- `apply_rules(tx, rules) -> Transaction` — rules are considered by descending `priority` (ties keep list order). The first matching rule that has a category sets it, but only if the transaction has no category yet. Tags from every matching rule are added.

**`homeledger/budgets.py`**
- `spent(transactions, budget, period) -> Decimal` — the net outflow in the budget's category within the period, as a positive number (refunds in the category reduce it); never below zero.
- `rollover(budget, previous_spent) -> Decimal` — 0 unless `budget.rollover`; otherwise `limit - previous_spent` (negative when overspent), clamped to `[-rollover_cap, rollover_cap]` when a cap is set.
- `BudgetStatus` — frozen dataclass `(category, available, spent, remaining)`.
- `status(transactions, budget, month: date) -> BudgetStatus` — for the budget's period containing `month`: `available = limit + rollover(budget, spent in the previous period)`, `remaining = available - spent`.

**`homeledger/search.py`**
- `search(transactions, query: str) -> list[Transaction]` — keeps input order; every term must match. Terms are separated by spaces, and double quotes group words (`payee:"k market"`). Supported terms:
  - `category:X` (case-insensitive equality), `payee:X` (case-insensitive substring), `tag:X`, `account:ID`
  - `after:DATE` (on or after), `before:DATE` (strictly before), where DATE is anything `parse_date` accepts
  - `amount<N`, `amount<=N`, `amount>N`, `amount>=N`, `amount=N` on the signed amount (`amount<-20` means spending over 20)
  - a bare word: case-insensitive substring of the payee or memo
  - a leading `-` negates any term (`-category:rent`); a token like `-5` is not negated
- An unknown key (`foo:bar`) or a malformed amount term raises `ValidationError`.
