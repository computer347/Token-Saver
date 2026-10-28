import pytest

from taskbench_app.parsing import parse_amount, parse_csv_line
from taskbench_app.validation import ValidationError


def test_plain_amount():
    assert parse_amount("12.50") == 12.5


def test_currency_symbol():
    assert parse_amount("€12") == 12.0


def test_thousands_separator():
    assert parse_amount("1,234.50") == 1234.5


def test_garbage_amount():
    with pytest.raises(ValidationError):
        parse_amount("twelve")


def test_csv_line():
    data = parse_csv_line("2026-01-05, 12.50 , food")
    assert data["date"] == "2026-01-05" and data["category"] == "food"


def test_semicolon_csv_line():
    data = parse_csv_line("2026-01-05;12;salary;income;january")
    assert data["kind"] == "income" and data["description"] == "january"
