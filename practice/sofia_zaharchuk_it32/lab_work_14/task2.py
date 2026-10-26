import sys
from pathlib import Path

from tabulate import tabulate

NAME, SURNAME, GROUP = "Sofiia", "Zakharchuk", "IT-32"

FILE = Path(__file__).resolve().parent / "data" / "expenses.csv"


def load(path: Path) -> dict[str, list[float]]:
    """Read expenses and group amounts by category."""
    groups: dict[str, list[float]] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        sys.exit(f"error: cannot read {path}: {e}")
    for n, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(";")
        try:
            category = parts[1].strip()
            amount = float(parts[2].replace(",", "."))
        except (ValueError, IndexError):
            print(f"warning: line {n} skipped: {line!r}", file=sys.stderr)
            continue
        groups.setdefault(category, []).append(amount)
    return groups


def main() -> None:
    print(f"{NAME} {SURNAME}, {GROUP}")
    groups = load(FILE)
    rows = [[cat, len(v), sum(v)] for cat, v in groups.items()]
    rows.append(["TOTAL", sum(r[1] for r in rows), sum(r[2] for r in rows)])
    print(tabulate(rows, headers=["category", "count", "total"],
                   tablefmt="github", floatfmt=".2f"))


if __name__ == "__main__":
    main()
