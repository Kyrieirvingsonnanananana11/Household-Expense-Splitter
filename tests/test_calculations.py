import unittest
from calculations import calculate_split, calculate_balances

class CalculationTests(unittest.TestCase):
    def test_equal_split(self):
        self.assertEqual(calculate_split(900, 3), 300.00)

    def test_zero_members_rejected(self):
        with self.assertRaises(ValueError):
            calculate_split(100, 0)

    def test_rounding_balances_sum_to_zero(self):
        rows = [
            {"name": "Asha", "paid": 10.00},
            {"name": "Pema", "paid": 0.00},
            {"name": "Karma", "paid": 0.00},
        ]
        balances = calculate_balances(rows, 10.00)
        self.assertEqual(round(sum(row[3] for row in balances), 2), 0.00)
        self.assertEqual([row[2] for row in balances], [3.34, 3.33, 3.33])

if __name__ == "__main__":
    unittest.main()
