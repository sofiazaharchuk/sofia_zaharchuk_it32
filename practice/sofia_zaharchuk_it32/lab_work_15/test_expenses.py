from pathlib import Path

import pytest

from expenses import load_expenses, parse_line, total_by_category

# Замінюється командою з інструкції на 5 рядків з вашого data/expenses.csv
CASES = [
    ('2026-09-21;coffee;45.00;coffee before lecture', 'coffee', 45.0),
    ('2026-09-21;food;38.00;bread and cheese', 'food', 38.0),
    ('2026-09-21;transport;16.00;bus to college', 'transport', 16.0),
    ('2026-09-22;food;52.00;lunch at canteen', 'food', 52.0),
    ('2026-09-22;coffee;45.00;coffee before lecture', 'coffee', 45.0),
]


# Завдання 2
def test_parse_line_valid():
    record = parse_line("2026-09-21;food;85.50;lunch")
    assert record["category"] == "food"
    assert record["amount"] == 85.5


def test_parse_line_all_fields():
    record = parse_line("2026-09-21;food;85.50;lunch")
    assert record == {"date": "2026-09-21", "category": "food", "amount": 85.5, "comment": "lunch"}


def test_parse_line_amount_is_float():
    assert isinstance(parse_line("2026-09-22;transport;30;bus")["amount"], float)


# Завдання 3
def test_parse_line_bad_amount():
    with pytest.raises(ValueError, match="not a number"):
        parse_line("2026-09-21;food;abc;lunch")


def test_parse_line_too_few_fields():
    with pytest.raises(ValueError, match="expected 4 fields"):
        parse_line("2026-09-21;food")


def test_parse_line_too_many_fields():
    with pytest.raises(ValueError, match="expected 4 fields"):
        parse_line("2026-09-21;food;85.50;lunch;extra")


# Завдання 4
@pytest.mark.parametrize(("line", "category", "amount"), CASES)
def test_parse_line_from_my_file(line, category, amount):
    record = parse_line(line)
    assert record["category"] == category
    assert record["amount"] == pytest.approx(amount)


# Завдання 5
def test_total_by_category(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text(
        "# date;category;amount;comment\n"
        "2026-09-21;food;85.50;lunch\n"
        "\n"
        "2026-09-22;food;14.50;coffee\n",
        encoding="utf-8",
    )
    totals = total_by_category(load_expenses(path))
    assert totals == {"food": 100.0}


def test_total_by_category_real_file():
    path = Path(__file__).resolve().parent / "data" / "expenses.csv"
    totals = total_by_category(load_expenses(path))
    assert totals == {
        "coffee": 180.00,
        "food": 198.00,
        "transport": 48.00,
        "snacks": 49.00,
        "stationery": 35.00,
    }
