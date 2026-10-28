from taskbench_app.models import Transaction
from taskbench_app.reports import format_summary, top_categories, total_by_category


def sample():
    return [
        Transaction("2026-01-02", 10.0, "food"),
        Transaction("2026-01-03", 5.5, "food"),
        Transaction("2026-01-04", 30.0, "rent"),
        Transaction("2026-01-05", 2.0, "coffee"),
        Transaction("2026-01-06", 100.0, "salary", kind="income"),
    ]


def test_total_by_category_ignores_income():
    assert total_by_category(sample()) == {"food": 15.5, "rent": 30.0, "coffee": 2.0}


def test_top_categories_sorted():
    assert top_categories(sample(), 2) == [("rent", 30.0), ("food", 15.5)]


def test_format_summary_missing_month():
    assert format_summary("2026-05", {}) == "2026-05: no transactions"


def test_format_summary_lines():
    text = format_summary("2026-01", {"2026-01": {"income": 1.0, "expense": 2.0, "net": -1.0}})
    assert "net:     -1.00" in text
