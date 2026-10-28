import json
from pathlib import Path

from .models import Transaction
from .validation import validate_transaction


class Ledger:
    def __init__(self, path):
        self.path = Path(path)
        self.transactions: list[Transaction] = []
        if self.path.exists():
            self.load()

    def load(self) -> None:
        raw = json.loads(self.path.read_text(encoding="utf-8") or "[]")
        self.transactions = [Transaction.from_dict(item) for item in raw]

    def save(self) -> None:
        payload = [t.to_dict() for t in self.transactions]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add(self, data: dict) -> Transaction:
        transaction = validate_transaction(data)
        self.transactions.append(transaction)
        return transaction

    def in_month(self, month: str) -> list[Transaction]:
        return [t for t in self.transactions if t.date.startswith(month + "-")]

    def by_category(self, category: str) -> list[Transaction]:
        wanted = category.strip().lower()
        return [t for t in self.transactions if t.category == wanted]
