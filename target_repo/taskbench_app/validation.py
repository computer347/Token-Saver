import math

from .models import Transaction

KINDS = ("income", "expense")


class ValidationError(ValueError):
    pass


def validate_date(text: str) -> str:
    parts = text.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValidationError(f"date must be YYYY-MM-DD: {text!r}")
    year, month, day = (int(p) for p in parts)
    if not 1900 <= year <= 2100:
        raise ValidationError(f"year out of range: {year}")
    if not 1 <= month <= 12:
        raise ValidationError(f"month out of range: {month}")
    if not 1 <= day <= days_in_month(year, month):
        raise ValidationError(f"day out of range: {day}")
    return f"{year:04d}-{month:02d}-{day:02d}"


def days_in_month(year: int, month: int) -> int:
    if month == 2:
        leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        return 29 if leap else 28
    return 30 if month in (4, 6, 9, 11) else 31


def validate_amount(value) -> float:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"amount is not a number: {value!r}")
    if not math.isfinite(amount):
        raise ValidationError("amount must be finite")
    if amount < 0:
        raise ValidationError("amount must not be negative; use kind='income' or 'expense'")
    return round(amount, 2)


def validate_category(text: str) -> str:
    cleaned = (text or "").strip().lower()
    if not cleaned:
        raise ValidationError("category must not be empty")
    return cleaned


def validate_kind(text: str) -> str:
    if text not in KINDS:
        raise ValidationError(f"kind must be one of {KINDS}: {text!r}")
    return text


def validate_transaction(data: dict) -> Transaction:
    return Transaction(
        date=validate_date(data["date"]),
        amount=validate_amount(data["amount"]),
        category=validate_category(data["category"]),
        kind=validate_kind(data.get("kind", "expense")),
        description=(data.get("description") or "").strip(),
    )
