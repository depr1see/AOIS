import unittest

from core.derivatives import boolean_derivative, derivative_form, derivative_summary, fictive_variables
from core.parser import FormulaParser
from core.post_classes import post_classes
from core.truth_table import build_truth_table
from core.zhegalkin import zhegalkin_polynomial


class TestPostZhegalkinDerivatives(unittest.TestCase):
    def setUp(self):
        self.ast = FormulaParser("!(!a->!b)|c").parse()
        self.vars = sorted(self.ast.variables(), key=lambda x: "abcde".index(x))
        self.table = build_truth_table(self.ast, self.vars)

    def test_post_classes_keys(self):
        result = post_classes(self.table)
        self.assertEqual(set(result.keys()), {"T0", "T1", "S", "M", "L"})

    def test_zhegalkin_polynomial(self):
        poly, masks = zhegalkin_polynomial(self.table)
        self.assertIsInstance(poly, str)
        self.assertIsInstance(masks, list)

    def test_fictive_variables(self):
        self.assertEqual(fictive_variables(self.table), [])

    def test_boolean_derivative(self):
        derivative = boolean_derivative(self.table, [0])
        self.assertEqual(len(derivative), len(self.table.rows))

    def test_derivative_form(self):
        form = derivative_form(self.table, [0, 1])
        self.assertEqual(len(form), len(self.table.rows))

    def test_derivative_summary(self):
        summary = derivative_summary(self.table, max_order=3)
        self.assertIn("a", summary)
        self.assertIn("a,b", summary)
