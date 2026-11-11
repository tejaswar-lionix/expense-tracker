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


if __name__ == "__main__":
    unittest.main()
