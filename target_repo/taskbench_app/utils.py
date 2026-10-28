def round_money(value: float) -> float:
    return round(value + 0.0, 2)


def month_key(date: str) -> str:
    return date[:7]
