import unittest

from core.karnaugh import build_karnaugh_map, karnaugh_to_text
from core.minimizer import minimize_cnf, minimize_dnf
from core.parser import FormulaParser
from core.truth_table import build_truth_table


class TestMinimizerKarnaugh(unittest.TestCase):
    def setUp(self):
        self.ast = FormulaParser("!(!a->!b)|c").parse()
        self.vars = sorted(self.ast.variables(), key=lambda x: "abcde".index(x))
        self.table = build_truth_table(self.ast, self.vars)

    def test_minimize_dnf(self):
        result = minimize_dnf(self.table.values(), self.vars)
        self.assertIsInstance(result.reduced_expression, str)
        self.assertGreaterEqual(len(result.prime_implicants), len(result.selected_implicants))

    def test_minimize_cnf(self):
        result = minimize_cnf(self.table.values(), self.vars)
        self.assertIsInstance(result.reduced_expression, str)

    def test_karnaugh_map_dimensions(self):
        km = build_karnaugh_map(self.table.values(), self.vars)
        self.assertEqual(len(km.grid), 2)
        self.assertEqual(len(km.grid[0]), 4)

    def test_karnaugh_text(self):
        km = build_karnaugh_map(self.table.values(), self.vars)
        text = karnaugh_to_text(km)
        self.assertIsInstance(text, str)
        self.assertIn("00", text)
