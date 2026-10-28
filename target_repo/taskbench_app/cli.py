import argparse
import sys

from .reports import format_summary, monthly_summary, top_categories
from .storage import Ledger
from .validation import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskbench")
    parser.add_argument("--ledger", default="ledger.json", help="path to the ledger file")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add a transaction")
    add.add_argument("date")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("description", nargs="?", default="")
    add.add_argument("--kind", default="expense", choices=["income", "expense"])

    summary = commands.add_parser("summary", help="show a monthly summary")
    summary.add_argument("--month", required=True, help="YYYY-MM")

    top = commands.add_parser("top", help="show top expense categories")
    top.add_argument("-n", type=int, default=3)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    ledger = Ledger(args.ledger)
    try:
        if args.command == "add":
            ledger.add({"date": args.date, "amount": args.amount, "category": args.category,
                        "kind": args.kind, "description": args.description})
            ledger.save()
            print("added")
        elif args.command == "summary":
            print(format_summary(args.month, monthly_summary(ledger.transactions)))
        elif args.command == "top":
            for category, total in top_categories(ledger.transactions, args.n):
                print(f"{category}: {total:.2f}")
    except ValidationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
