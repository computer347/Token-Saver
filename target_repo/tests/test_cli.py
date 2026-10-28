from taskbench_app.cli import main


def test_add_and_top(tmp_path, capsys):
    ledger = str(tmp_path / "l.json")
    assert main(["--ledger", ledger, "add", "2026-01-05", "12.50", "food"]) == 0
    assert main(["--ledger", ledger, "add", "2026-01-06", "3", "coffee"]) == 0
    capsys.readouterr()
    assert main(["--ledger", ledger, "top", "-n", "1"]) == 0
    assert capsys.readouterr().out.strip() == "food: 12.50"


def test_invalid_date_returns_error(tmp_path):
    assert main(["--ledger", str(tmp_path / "l.json"), "add", "2026-02-30", "1", "x"]) == 2
