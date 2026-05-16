import unittest

from core.parser import FormulaParser
from core.tokenizer import FormulaSyntaxError, normalize_formula, tokenize


class TestTokenizerParser(unittest.TestCase):
    def test_normalize_formula(self):
        self.assertEqual(normalize_formula("!(!a→!b)∨c"), "!(!a->!b)|c")

    def test_tokenize_unicode(self):
        tokens = tokenize("!(!a→!b)∨c")
        self.assertEqual([t.type for t in tokens], ["NOT", "LPAREN", "NOT", "VAR", "IMP", "NOT", "VAR", "RPAREN", "OR", "VAR"])

    def test_parse_to_infix(self):
        ast = FormulaParser("!(!a->!b)|c").parse()
        self.assertTrue(ast.to_infix())

    def test_parse_invalid_variable(self):
        with self.assertRaises(FormulaSyntaxError):
            tokenize("x1&y")

    def test_parse_invalid_syntax(self):
        with self.assertRaises(FormulaSyntaxError):
            FormulaParser("!(a|b").parse()
