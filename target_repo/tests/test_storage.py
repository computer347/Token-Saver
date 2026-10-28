from taskbench_app.storage import Ledger


def test_add_save_load(tmp_path):
    path = tmp_path / "ledger.json"
    ledger = Ledger(path)
    ledger.add({"date": "2026-01-05", "amount": 10, "category": "Food"})
    ledger.save()
    again = Ledger(path)
    assert len(again.transactions) == 1
    assert again.transactions[0].category == "food"


def test_in_month(tmp_path):
    ledger = Ledger(tmp_path / "l.json")
    ledger.add({"date": "2026-01-05", "amount": 1, "category": "a"})
    ledger.add({"date": "2026-02-05", "amount": 1, "category": "a"})
    assert len(ledger.in_month("2026-01")) == 1
