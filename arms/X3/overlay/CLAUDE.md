# Repository map

Generated from the source; use it to go straight to the right file instead of exploring.

## taskbench_app/__init__.py — taskbench_app: a small personal-ledger library used as a benchmark target.

## taskbench_app/cli.py
- `build_parser() -> argparse.ArgumentParser`
- `main(argv=None) -> int`

## taskbench_app/models.py
- class `Transaction`
  - `to_dict(self) -> dict`
  - `from_dict(cls, data: dict) -> 'Transaction'`

## taskbench_app/parsing.py
- `parse_amount(text: str) -> float` — Parse amounts like '12.50', '€12', '1,234.50' or ' 7 '.
- `parse_csv_line(line: str) -> dict` — Parse 'date,amount,category,kind,description' into a dict.

## taskbench_app/reports.py
- `total_by_category(transactions)`
- `top_categories(transactions, n=3)`
- `monthly_summary(transactions)`
- `format_summary(month, summary)`

## taskbench_app/storage.py
- class `Ledger`
  - `load(self) -> None`
  - `save(self) -> None`
  - `add(self, data: dict) -> Transaction`
  - `in_month(self, month: str) -> list[Transaction]`
  - `by_category(self, category: str) -> list[Transaction]`

## taskbench_app/utils.py
- `round_money(value: float) -> float`
- `month_key(date: str) -> str`

## taskbench_app/validation.py
- class `ValidationError`
- `validate_date(text: str) -> str`
- `days_in_month(year: int, month: int) -> int`
- `validate_amount(value) -> float`
- `validate_category(text: str) -> str`
- `validate_kind(text: str) -> str`
- `validate_transaction(data: dict) -> Transaction`

## tests/conftest.py

## tests/test_cli.py
- `test_add_and_top(tmp_path, capsys)`
- `test_invalid_date_returns_error(tmp_path)`

## tests/test_parsing.py
- `test_plain_amount()`
- `test_currency_symbol()`
- `test_thousands_separator()`
- `test_garbage_amount()`
- `test_csv_line()`
- `test_semicolon_csv_line()`

## tests/test_reports.py
- `sample()`
- `test_total_by_category_ignores_income()`
- `test_top_categories_sorted()`
- `test_format_summary_missing_month()`
- `test_format_summary_lines()`

## tests/test_storage.py
- `test_add_save_load(tmp_path)`
- `test_in_month(tmp_path)`

## tests/test_validation.py
- `test_valid_date_is_normalised()`
- `test_leap_day()`
- `test_bad_date_format()`
- `test_negative_amount_rejected()`
- `test_amount_rounded()`
- `test_category_cleaned()`
- `test_transaction_defaults_to_expense()`

## Running the tests

`python -m pytest -q` from the project root.
