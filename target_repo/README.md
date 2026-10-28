# taskbench-app

A small personal-ledger library with a command-line interface. Transactions
are validated, stored in a JSON ledger file and summarised in reports.

    python -m taskbench_app.cli --ledger ledger.json add 2026-01-05 12.50 food "lunch"
    python -m taskbench_app.cli --ledger ledger.json summary --month 2026-01

Run the tests with `python -m pytest -q`.
