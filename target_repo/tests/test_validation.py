import pytest

from taskbench_app.validation import (
    ValidationError, validate_amount, validate_category, validate_date, validate_transaction,
)


def test_valid_date_is_normalised():
    assert validate_date("2026-1-5") == "2026-01-05"


def test_leap_day():
    assert validate_date("2024-02-29") == "2024-02-29"
    with pytest.raises(ValidationError):
        validate_date("2023-02-29")


def test_bad_date_format():
    with pytest.raises(ValidationError):
        validate_date("05/01/2026")


def test_negative_amount_rejected():
    with pytest.raises(ValidationError):
        validate_amount(-5)


def test_amount_rounded():
    assert validate_amount("12.345") == 12.35 or validate_amount("12.345") == 12.34


def test_category_cleaned():
    assert validate_category("  Food ") == "food"


def test_transaction_defaults_to_expense():
    t = validate_transaction({"date": "2026-03-01", "amount": 3, "category": "Coffee"})
    assert t.kind == "expense" and t.category == "coffee"
