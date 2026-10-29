from pathlib import Path


def parse_line(line: str) -> dict:
    """Parse 'date;category;amount;comment' into a dict. Raise ValueError if bad."""
    parts = line.strip().split(";")
    if len(parts) != 4:
        raise ValueError(f"expected 4 fields, got {len(parts)}: {line!r}")
    date, category, amount, comment = (p.strip() for p in parts)
    try:
        amount = float(amount.replace(",", "."))
    except ValueError:
        raise ValueError(f"amount is not a number: {amount!r}") from None
    return {"date": date, "category": category, "amount": amount, "comment": comment}


def total_by_category(records: list[dict]) -> dict[str, float]:
    """Return {category: total}, totals rounded to 2 decimals."""
    totals: dict[str, float] = {}
    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0.0) + record["amount"]
    return {category: round(total, 2) for category, total in totals.items()}


def load_expenses(path) -> list[dict]:
    """Read a file, skip comments and empty lines, return a list of records."""
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        records.append(parse_line(line))
    return records
