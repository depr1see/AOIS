import unittest

from lab2_boolean.core.parser import ExpressionParser, ExpressionError


class TestExpressionParser(unittest.TestCase):
    def test_unicode_normalization_and_evaluation(self):
        parser = ExpressionParser("!(!a→!b)∨c")
        self.assertEqual(parser.evaluate({"a": 1, "b": 0, "c": 0}), 0)
        self.assertEqual(parser.evaluate({"a": 0, "b": 0, "c": 0}), 0)
        self.assertEqual(parser.evaluate({"a": 1, "b": 1, "c": 1}), 1)
        self.assertIn("->", parser.postfix)

    def test_equivalence_operator(self):
        parser = ExpressionParser("a~b")
        self.assertEqual(parser.evaluate({"a": 0, "b": 0}), 1)
        self.assertEqual(parser.evaluate({"a": 0, "b": 1}), 0)

    def test_invalid_symbol(self):
        with self.assertRaises(ExpressionError):
            ExpressionParser("a#b")

    def test_unbalanced_parentheses(self):
        with self.assertRaises(ExpressionError):
            ExpressionParser("(a&b")

    def test_missing_operand(self):
        with self.assertRaises(ExpressionError):
            ExpressionParser("!")

    def test_variables_order(self):
        parser = ExpressionParser("e|a|c")
        self.assertEqual(parser.variables(), ["a", "c", "e"])
