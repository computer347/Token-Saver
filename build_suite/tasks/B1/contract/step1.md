## Interface contract — step 1: core

Python 3.11+, standard library only. A package `homeledger/` at the project root; `homeledger/__init__.py` defines `__version__` (any string) and `SCHEMA_VERSION = 3`.

**`homeledger/errors.py`**
- `HomeLedgerError(Exception)` — base class of every error the library raises on bad input.
- `ValidationError(HomeLedgerError, ValueError)`
- `NotFoundError(HomeLedgerError, KeyError)`
- `ImportFormatError(HomeLedgerError)` — constructor `ImportFormatError(message, line=None)`; keeps the line number in `.line`.
- `MigrationError(HomeLedgerError)`

**`homeledger/money.py`** — all money is `decimal.Decimal`; never use float.
- `parse_amount(text: str) -> Decimal`. Accepts `"12.50"`, `"-12,50"`, `"1 234,56"`, `"1,234.56"`, `"1.234,56"`, `"(12.50)"` (= -12.50), `"€12"`, `"$5"`, `"12 kr"`, a trailing minus `"12.50-"` (= -12.50), and a leading `+`. Spaces (including non-breaking) are ignored. The decimal separator is whichever of `.` or `,` appears last, but only if it is followed by exactly one or two digits; otherwise every `.` and `,` is a thousands separator (`"1,234"` = 1234). Empty or unparseable input raises `ValidationError`.
- `quantize(amount: Decimal, currency: str = "EUR") -> Decimal` — round half-up to 2 decimals; to 0 decimals for `JPY`, `KRW`, `ISK`.
- `format_amount(amount, currency="EUR", locale="en") -> str` — `en`: `"-1,234.50 EUR"`. `fi`: `"-1 234,50 €"`, using U+00A0 (non-breaking space) as the thousands separator and the symbol `€`, `$` or `£` for EUR/USD/GBP, else the currency code.
- `split_evenly(amount: Decimal, parts: int, currency="EUR") -> list[Decimal]` — shares that sum exactly to the quantized amount, differing by at most one cent, with the extra cents on the first shares. `parts <= 0` raises `ValidationError`.

**`homeledger/dates.py`**
- `parse_date(text) -> datetime.date` — accepts a `date`, ISO `"2026-01-05"`, Finnish `"5.1.2026"`, `"5/1/2026"` (day/month/year), `"2026/1/5"`, compact `"20260105"`, and OFX timestamps such as `"20260105120000"` or `"20260105120000[0:GMT]"`. Anything else, or an impossible date, raises `ValidationError`.
- `parse_month("2026-01") -> date(2026, 1, 1)`; invalid input raises `ValidationError`.
- `month_key(d) -> "YYYY-MM"`.
- `month_end(d) -> date` — last day of d's month.
- `add_months(d, n) -> date` — clamps the day: Jan 31 + 1 month = Feb 28 (or 29); works for negative n.
- `iter_months(start, end)` — yields the first day of every month from start's month to end's month inclusive.
- `Period` — frozen dataclass with `start` and `end` (both inclusive) and `contains(d) -> bool`.
- `period_for(d, kind) -> Period` for `kind` in `"monthly"`, `"weekly"` (Monday–Sunday), `"quarterly"`, `"yearly"`; anything else raises `ValidationError`.
- `previous_period(period, kind) -> Period` — the period of the same kind immediately before.

**`homeledger/models.py`** — frozen dataclasses. Amounts are signed: negative = money out, positive = money in.
- `Account(id, name, currency="EUR", kind="checking", opening_balance=Decimal("0"))`
- `Transaction(id, account_id, date, amount, currency="EUR", payee="", category="", memo="", tags=(), imported_id="", cleared=False)` with methods `with_category(c)` and `with_tags(*tags)` (returns a copy with tags appended, de-duplicated, order kept).
- `Budget(category, limit, period="monthly", rollover=False, rollover_cap=None)`
- Each has `to_dict()` returning JSON-safe values (dates as ISO strings, Decimals as strings, tags as a list, `rollover_cap` as a string or `None`) and a classmethod `from_dict(d)` that round-trips exactly.

**`homeledger/validation.py`**
- `validate_currency(code) -> str` — must be exactly three uppercase letters, else `ValidationError`.
- `validate_transaction(data: dict) -> Transaction` — `account_id` required; `amount` parsed with `parse_amount` (a `Decimal` is used as is) and must not be zero; `date` parsed with `parse_date`; `currency` validated (default `"EUR"`); `payee`, `memo` stripped; `category` stripped and lower-cased; `tags` de-duplicated. Problems raise `ValidationError`.
