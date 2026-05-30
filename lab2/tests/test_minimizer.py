import unittest

from lab2_boolean.algorithms.minimizer import Minimizer


class TestMinimizer(unittest.TestCase):
    def setUp(self):
        # Function from the statement example: !(!a→!b)∨c
        self.minimizer = Minimizer([0, 1, 1, 1], ["a", "b"])

    def test_calculation_dnf(self):
        result = self.minimizer.calculation_method("DNF")
        self.assertIn("result", result)
        self.assertEqual(result["result"], "a ∨ b")

    def test_calculation_knf(self):
        result = self.minimizer.calculation_method("KNF")
        self.assertIn("result", result)
        self.assertEqual(result["result"], "(a ∨ b)")

    def test_table_method(self):
        result = self.minimizer.table_method("DNF")
        self.assertIn("coverage_table", result)
        self.assertGreaterEqual(len(result["coverage_table"]), 1)

    def test_karnaugh(self):
        result = self.minimizer.karnaugh_method()
        self.assertIn("dnf", result)
        self.assertIn("knf", result)
        self.assertGreaterEqual(len(result["dnf"]["layers"]), 1)

    def test_combine_and_covers(self):
        self.assertEqual(Minimizer._combine("10-", "11-"), "1--")
        self.assertIsNone(Minimizer._combine("10-", "1-0"))
        self.assertTrue(Minimizer._covers("1-0", "110"))
