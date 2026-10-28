---
name: repo-recipes
description: Use for any change in this repository. Conventions and step-by-step recipes for taskbench_app, so you don't need to rediscover them.
---
# taskbench_app conventions

**Layout:** `models.py` (Transaction dataclass, to_dict/from_dict) · `validation.py` (validate_* functions, raise ValidationError) · `parsing.py` (parse_amount, parse_csv_line) · `storage.py` (Ledger: load/save JSON, add validates) · `reports.py` (totals, monthly_summary, format_summary) · `utils.py` (round_money, month_key) · `cli.py` (argparse in build_parser, dispatch in main).

**Add a CLI command:** in `build_parser()` add `commands.add_parser("name")` with its arguments; in `main()` add an `elif args.command == "name":` branch inside the existing `try`. Print results with `print`, errors go to stderr, return an int exit code. A ValidationError raised inside the `try` is already turned into exit code 2.

**Validation:** reuse the functions in `validation.py`; raise `ValidationError` with a clear message. `Ledger.add()` already validates a dict.

**Money:** round with `utils.round_money`.

**Tests:** pytest files in `tests/`. Use `tmp_path` for ledger files and call `cli.main([...])` directly with `capsys` to capture output. Run everything with `python3 -m pytest -q`.
