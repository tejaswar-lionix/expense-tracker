import unittest

from expenses import add_expense, by_category, total


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


if __name__ == "__main__":
    unittest.main()
