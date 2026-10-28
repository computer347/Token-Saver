"""Reference solutions used only by the self-test, to prove every checker can pass."""
from pathlib import Path


def _sub(path: Path, old: str, new: str):
    text = path.read_text()
    assert old in text, f"anchor missing in {path}: {old!r}"
    path.write_text(text.replace(old, new))


def apply(task: str, step: int, work: Path):
    if task == "B1":
        if step == 0:  # drop in the full reference build; later steps have nothing left to do
            import shutil
            ref = Path(__file__).resolve().parents[1] / "build_suite" / "reference" / "B1" / "homeledger"
            shutil.copytree(ref, work / "homeledger", ignore=shutil.ignore_patterns("__pycache__"))
            (work / "tests").mkdir(exist_ok=True)
            (work / "tests" / "test_basic.py").write_text(
                "from decimal import Decimal\nfrom homeledger.money import parse_amount\n\n\n"
                "def test_parse():\n    assert parse_amount('1,50') == Decimal('1.50')\n")
        return
    app = work / "taskbench_app"
    if task == "T1":
        _sub(app / "parsing.py", 'cleaned.replace(",", ".")', 'cleaned.replace(",", "")')
    elif task == "T2":
        (app / "holidays.py").write_text(
            "import json\nimport urllib.request\n\nURL = 'https://date.nager.at/api/v3/PublicHolidays/{}/{}'\n\n\n"
            "def get_public_holidays(year: int, country_code: str) -> list[dict]:\n"
            "    if len(country_code) != 2 or not country_code.isalpha():\n"
            "        raise ValueError(f'country code must be two letters: {country_code!r}')\n"
            "    with urllib.request.urlopen(URL.format(year, country_code.upper())) as response:\n"
            "        data = json.loads(response.read().decode('utf-8'))\n"
            "    return [{'date': h['date'], 'name': h['name']} for h in data]\n")
        (work / "tests" / "test_holidays.py").write_text(
            "import io, json, urllib.request\nfrom taskbench_app.holidays import get_public_holidays\n\n\n"
            "class R(io.BytesIO):\n    def __enter__(self): return self\n    def __exit__(self, *a): return False\n\n\n"
            "def test_holidays(monkeypatch):\n"
            "    monkeypatch.setattr(urllib.request, 'urlopen', lambda url: R(json.dumps([{'date': '2026-01-01', 'name': 'NY'}]).encode()))\n"
            "    assert get_public_holidays(2026, 'FI') == [{'date': '2026-01-01', 'name': 'NY'}]\n")
    elif task == "T3":
        (app / "reports.py").write_text(
            "from .utils import month_key, round_money\n\n\n"
            "def total_by_category(transactions):\n    totals = {}\n    for t in transactions:\n"
            "        if t.kind == 'expense':\n            totals[t.category] = totals.get(t.category, 0) + t.amount\n"
            "    return {category: round_money(amount) for category, amount in totals.items()}\n\n\n"
            "def top_categories(transactions, n=3):\n    totals = total_by_category(transactions)\n"
            "    return sorted(totals.items(), key=lambda item: (-item[1], item[0]))[:n]\n\n\n"
            "def monthly_summary(transactions):\n    months = {}\n    for t in transactions:\n"
            "        month = months.setdefault(month_key(t.date), {'income': 0.0, 'expense': 0.0})\n"
            "        month['income' if t.kind == 'income' else 'expense'] += t.amount\n"
            "    return {key: {'income': round_money(m['income']), 'expense': round_money(m['expense']),\n"
            "                  'net': round_money(m['income'] - m['expense'])} for key, m in sorted(months.items())}\n\n\n"
            "def format_summary(month, summary):\n    if month not in summary:\n        return f'{month}: no transactions'\n"
            "    s = summary[month]\n    return '\\n'.join([month, f\"  income:  {s['income']:.2f}\", f\"  expense: {s['expense']:.2f}\",\n"
            "                      f\"  net:     {s['net']:.2f}\"])\n")
    elif task == "T4":
        (work / "ANSWER.md").write_text("`validate_amount` in `taskbench_app/validation.py`\n")
    elif task == "T5":
        (work / "tests" / "test_monthly_summary.py").write_text(
            "from taskbench_app.models import Transaction\nfrom taskbench_app.reports import monthly_summary\n\n\n"
            "def test_net():\n    s = monthly_summary([Transaction('2026-01-01', 100, 'pay', kind='income'), Transaction('2026-01-02', 30, 'food')])\n"
            "    assert s['2026-01'] == {'income': 100.0, 'expense': 30.0, 'net': 70.0}\n\n\n"
            "def test_sorted():\n    s = monthly_summary([Transaction('2026-02-01', 1, 'a'), Transaction('2026-01-01', 1, 'a')])\n"
            "    assert list(s) == ['2026-01', '2026-02']\n\n\n"
            "def test_empty():\n    assert monthly_summary([]) == {}\n")
    elif task == "T6" and step == 0:
        _sub(app / "validation.py", "if not 1 <= month <= 13:", "if not 1 <= month <= 12:")
        (work / "tests" / "test_month_regression.py").write_text(
            "import pytest\nfrom taskbench_app.validation import ValidationError, validate_date\n\n\n"
            "def test_month_13():\n    with pytest.raises(ValidationError):\n        validate_date('2026-13-01')\n")
    elif task == "T6" and step == 1:
        cli = app / "cli.py"
        _sub(cli, "import argparse\n", "import argparse\nimport json\n")
        _sub(cli, 'summary.add_argument("--month", required=True, help="YYYY-MM")',
             'summary.add_argument("--month", required=True, help="YYYY-MM")\n    summary.add_argument("--json", action="store_true")')
        _sub(cli, "            print(format_summary(args.month, monthly_summary(ledger.transactions)))",
             "            summary = monthly_summary(ledger.transactions)\n"
             "            if args.json:\n"
             "                print(json.dumps(summary.get(args.month, {'income': 0.0, 'expense': 0.0, 'net': 0.0})))\n"
             "            else:\n"
             "                print(format_summary(args.month, summary))")
    elif task == "T7":
        cli = app / "cli.py"
        _sub(cli, "import argparse\nimport sys\n", "import argparse\nimport sys\nfrom pathlib import Path\n")
        _sub(cli, "from .reports import", "from .parsing import parse_csv_line\nfrom .reports import")
        _sub(cli, '    top = commands.add_parser("top", help="show top expense categories")',
             '    imp = commands.add_parser("import", help="import transactions from a CSV file")\n'
             '    imp.add_argument("file")\n\n'
             '    top = commands.add_parser("top", help="show top expense categories")')
        _sub(cli, '        elif args.command == "top":',
             '        elif args.command == "import":\n'
             '            count, bad = 0, False\n'
             '            for number, line in enumerate(Path(args.file).read_text().splitlines(), 1):\n'
             '                if not line.strip() or (number == 1 and line.lower().startswith("date")):\n'
             '                    continue\n'
             '                try:\n'
             '                    ledger.add(parse_csv_line(line))\n'
             '                    count += 1\n'
             '                except ValidationError as error:\n'
             '                    print(f"line {number}: {error}", file=sys.stderr)\n'
             '                    bad = True\n'
             '            ledger.save()\n'
             '            print(f"imported {count}")\n'
             '            return 1 if bad else 0\n'
             '        elif args.command == "top":')
        (work / "tests" / "test_import_cmd.py").write_text(
            "from taskbench_app.cli import main\n\n\n"
            "def test_import(tmp_path, capsys):\n"
            "    f = tmp_path / 'a.csv'\n    f.write_text('2026-01-01,1,a\\n')\n"
            "    assert main(['--ledger', str(tmp_path / 'l.json'), 'import', str(f)]) == 0\n")
    elif task == "T8":
        _sub(app / "models.py", 'kind=data["kind"],', 'kind=data.get("kind", "expense"),')
        (work / "tests" / "test_old_ledger.py").write_text(
            "import json\nfrom taskbench_app.storage import Ledger\n\n\n"
            "def test_old(tmp_path):\n    p = tmp_path / 'o.json'\n"
            "    p.write_text(json.dumps([{'date': '2025-01-01', 'amount': 1, 'category': 'a'}]))\n"
            "    assert Ledger(p).transactions[0].kind == 'expense'\n")

