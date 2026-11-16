# expense-tracker

Track expenses and summarise spending by category.

## Usage

```bash
python3 -c "from expenses import *; e=[]; add_expense(e, 12.5, 'food', 'lunch'); print(total(e), by_category(e))"
python3 -c "from expenses import *; e=import_csv('expenses.csv'); print(total(e))"
python3 -c "from expenses import *; export_csv(import_csv('expenses.csv'), 'copy.csv')"
```

## Features

- Validated expense entry with categories and dates
- Totals overall and per category
- Monthly filtering with monthly(expenses, 'YYYY-MM')
- Per-category monthly budgets with spent, remaining, and over-budget warnings
- CSV import and export with import_csv(path) and export_csv(expenses, path)

```python
budgets = set_budget({}, "food", 300)
report = budget_report(expenses, budgets, "2026-11")
warnings = budget_warnings(expenses, budgets, "2026-11")
```

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
