import unittest

from expenses import (
    add_expense,
    budget_report,
    budget_warnings,
    by_category,
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


if __name__ == "__main__":
    unittest.main()
