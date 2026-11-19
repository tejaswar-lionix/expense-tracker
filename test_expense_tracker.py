import csv
import os
import tempfile
import unittest

from expenses import (
    add_expense,
    average_expense,
    budget_report,
    budget_warnings,
    by_category,
    export_csv,
    import_csv,
    remove,
    set_budget,
    total,
)


class ExpenseTests(unittest.TestCase):
    def test_total_and_categories(self):
        expenses = []
        add_expense(expenses, 10, "food", day="2026-11-01")
        add_expense(expenses, 5.5, "fun", day="2026-11-02")
        add_expense(expenses, 2.5, "food", day="2026-11-03")
        self.assertEqual(total(expenses), 18.0)
        self.assertEqual(by_category(expenses), {"food": 12.5, "fun": 5.5})

    def test_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            add_expense([], -1, "food")

    def test_rejects_unknown_category(self):
        with self.assertRaises(ValueError):
            add_expense([], 5, "pets")


class AverageTests(unittest.TestCase):
    def test_average_of_multiple_expenses(self):
        expenses = []
        add_expense(expenses, 10, "food", day="2026-11-01")
        add_expense(expenses, 5.5, "fun", day="2026-11-02")
        add_expense(expenses, 2.5, "home", day="2026-11-03")
        self.assertEqual(average_expense(expenses), 6.0)

    def test_average_of_single_expense(self):
        expenses = []
        add_expense(expenses, 12.5, "food", day="2026-11-01")
        self.assertEqual(average_expense(expenses), 12.5)

    def test_average_of_empty_list_is_zero(self):
        self.assertEqual(average_expense([]), 0.0)


class RemoveTests(unittest.TestCase):
    def test_remove_middle_item(self):
        expenses = []
        add_expense(expenses, 10, "food", day="2026-11-01")
        add_expense(expenses, 5, "fun", day="2026-11-02")
        add_expense(expenses, 2, "home", day="2026-11-03")
        self.assertEqual(
            [item["amount"] for item in remove(expenses, 1)],
            [10.0, 2.0],
        )

    def test_remove_only_item(self):
        expenses = []
        add_expense(expenses, 10, "food", day="2026-11-01")
        self.assertEqual(remove(expenses, 0), [])

    def test_remove_does_not_mutate_input(self):
        expenses = []
        add_expense(expenses, 10, "food", day="2026-11-01")
        add_expense(expenses, 5, "fun", day="2026-11-02")
        remove(expenses, 0)
        self.assertEqual(len(expenses), 2)

    def test_remove_out_of_range_raises(self):
        with self.assertRaises(IndexError):
            remove([], 0)


class CsvTests(unittest.TestCase):
    def test_export_import_roundtrip(self):
        expenses = []
        add_expense(expenses, 12.5, "food", "lunch, with tea", day="2026-11-01")
        add_expense(expenses, 3, "transport", day="2026-11-02")
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "expenses.csv")
            export_csv(expenses, path)
            self.assertEqual(import_csv(path), expenses)

    def test_import_rejects_unknown_category(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "expenses.csv")
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["amount", "category", "note", "date"])
                writer.writerow([5, "pets", "", "2026-11-01"])
            with self.assertRaises(ValueError):
                import_csv(path)

    def test_import_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            import_csv("/nonexistent/expenses.csv")


class MonthlyTests(unittest.TestCase):
    def test_monthly_filters_by_prefix(self):
        from expenses import monthly

        expenses = []
        add_expense(expenses, 10, "food", day="2026-11-01")
        add_expense(expenses, 20, "food", day="2026-10-01")
        self.assertEqual(total(monthly(expenses, "2026-11")), 10.0)

    def test_monthly_rejects_bad_format(self):
        from expenses import monthly

        with self.assertRaises(ValueError):
            monthly([], "November")


class BudgetTests(unittest.TestCase):
    def test_set_budget_rejects_unknown_category(self):
        with self.assertRaises(ValueError):
            set_budget({}, "pets", 100)

    def test_set_budget_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            set_budget({}, "food", -1)

    def test_report_tracks_spent_remaining_and_over(self):
        expenses = []
        add_expense(expenses, 120, "food", day="2026-11-01")
        add_expense(expenses, 30, "fun", day="2026-11-02")
        budgets = set_budget(set_budget({}, "food", 300), "fun", 20)
        report = budget_report(expenses, budgets, "2026-11")
        self.assertEqual(report["food"]["spent"], 120.0)
        self.assertEqual(report["food"]["remaining"], 180.0)
        self.assertFalse(report["food"]["over"])
        self.assertEqual(report["fun"]["remaining"], -10.0)
        self.assertTrue(report["fun"]["over"])

    def test_report_ignores_other_months(self):
        expenses = []
        add_expense(expenses, 500, "food", day="2026-10-01")
        budgets = set_budget({}, "food", 100)
        report = budget_report(expenses, budgets, "2026-11")
        self.assertEqual(report["food"]["spent"], 0.0)

    def test_warnings_only_for_over_budget_categories(self):
        expenses = []
        add_expense(expenses, 120, "food", day="2026-11-01")
        add_expense(expenses, 10, "fun", day="2026-11-02")
        budgets = set_budget(set_budget({}, "food", 100), "fun", 20)
        self.assertEqual(
            budget_warnings(expenses, budgets, "2026-11"),
            ["food is over budget by 20.00"],
        )


class MonthlyTotalsTests(unittest.TestCase):
    def test_sums_by_month(self):
        from expenses import monthly_totals

        expenses = [
            {"amount": 10.0, "date": "2026-11-01"},
            {"amount": 2.5, "date": "2026-11-15"},
            {"amount": 7.0, "date": "2026-10-31"},
        ]
        self.assertEqual(
            monthly_totals(expenses), {"2026-11": 12.5, "2026-10": 7.0}
        )

    def test_empty(self):
        from expenses import monthly_totals

        self.assertEqual(monthly_totals([]), {})


if __name__ == "__main__":
    unittest.main()
