from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    date: str          # YYYY-MM-DD
    amount: float      # always positive; kind says which way it goes
    category: str
    kind: str = "expense"   # "income" or "expense"
    description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            date=data["date"],
            amount=float(data["amount"]),
            category=data["category"],
            kind=data.get("kind", "expense"),
            description=data.get("description", ""),
        )
