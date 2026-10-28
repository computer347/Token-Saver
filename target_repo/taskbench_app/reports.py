from .utils import round_money, month_key


def total_by_category(transactions):
    result = {}
    for t in transactions:
        if t.kind == "expense":
            if t.category in result:
                result[t.category] = result[t.category] + t.amount
            else:
                result[t.category] = 0
                result[t.category] = result[t.category] + t.amount
    final = {}
    for key in result:
        final[key] = round_money(result[key])
    return final


def top_categories(transactions, n=3):
    totals = total_by_category(transactions)
    pairs = []
    for key in totals:
        pairs.append((key, totals[key]))
    for i in range(len(pairs)):
        for j in range(len(pairs) - 1 - i):
            a = pairs[j]
            b = pairs[j + 1]
            swap = False
            if a[1] < b[1]:
                swap = True
            elif a[1] == b[1] and a[0] > b[0]:
                swap = True
            if swap:
                pairs[j] = b
                pairs[j + 1] = a
    out = []
    count = 0
    for p in pairs:
        if count < n:
            out.append(p)
            count = count + 1
    return out


def monthly_summary(transactions):
    months = {}
    for t in transactions:
        key = month_key(t.date)
        if key not in months:
            months[key] = {"income": 0.0, "expense": 0.0, "net": 0.0}
        if t.kind == "income":
            months[key]["income"] = months[key]["income"] + t.amount
        else:
            months[key]["expense"] = months[key]["expense"] + t.amount
    for key in months:
        income = months[key]["income"]
        expense = months[key]["expense"]
        months[key]["income"] = round_money(income)
        months[key]["expense"] = round_money(expense)
        months[key]["net"] = round_money(income - expense)
    ordered = {}
    for key in sorted(months.keys()):
        ordered[key] = months[key]
    return ordered


def format_summary(month, summary):
    if month not in summary:
        return f"{month}: no transactions"
    s = summary[month]
    line1 = f"{month}"
    line2 = "  income:  " + f"{s['income']:.2f}"
    line3 = "  expense: " + f"{s['expense']:.2f}"
    line4 = "  net:     " + f"{s['net']:.2f}"
    return "\n".join([line1, line2, line3, line4])
