from .validation import ValidationError

CURRENCY_SYMBOLS = "€$£"


def parse_amount(text: str) -> float:
    """Parse amounts like '12.50', '€12', '1,234.50' or ' 7 '."""
    cleaned = text.strip()
    for symbol in CURRENCY_SYMBOLS:
        cleaned = cleaned.replace(symbol, "")
    cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        raise ValidationError(f"cannot parse amount: {text!r}")


def parse_csv_line(line: str) -> dict:
    """Parse 'date,amount,category,kind,description' into a dict."""
    fields = [f.strip() for f in line.split(";")] if ";" in line else [f.strip() for f in line.split(",", 4)]
    if len(fields) < 3:
        raise ValidationError(f"expected at least date, amount, category: {line!r}")
    data = {"date": fields[0], "amount": parse_amount(fields[1]), "category": fields[2]}
    if len(fields) > 3 and fields[3]:
        data["kind"] = fields[3]
    if len(fields) > 4:
        data["description"] = fields[4]
    return data
