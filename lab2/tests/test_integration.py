import unittest

from lab2_boolean.models.boolean_function import BooleanFunction
from lab2_boolean.models.post_analyzer import PostAnalyzer
from lab2_boolean.algorithms.minimizer import Minimizer


class TestIntegration(unittest.TestCase):
    def test_full_pipeline(self):
        func = BooleanFunction("!(!a→!b)∨c")
        analyzer = PostAnalyzer(func.vector, func.variables)
        minimizer = Minimizer(func.vector, func.variables)

        self.assertEqual(func.variables, ["a", "b", "c"])
        self.assertEqual(func.vector_string(), "01110101")
        self.assertTrue(analyzer.check_t0())
        self.assertFalse(analyzer.check_l())
        self.assertIn("⊕", analyzer.zhegalkin_polynomial())

        dnf = minimizer.calculation_method("DNF")["result"]
        knf = minimizer.calculation_method("KNF")["result"]
        self.assertTrue(dnf)
        self.assertTrue(knf)
