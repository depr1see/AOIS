import unittest

from core.analyzer import LogicFunctionAnalyzer


class TestIntegration(unittest.TestCase):
    def test_analyze_expression(self):
        result = LogicFunctionAnalyzer().analyze("!(!a->!b)|c")
        self.assertEqual(result.variables, ["a", "b", "c"])
        self.assertTrue(result.sdnf)
        self.assertTrue(result.sknf)
        self.assertIsInstance(result.index_value, int)
        self.assertTrue(result.kmap_text)

    def test_constant_expression(self):
        result = LogicFunctionAnalyzer().analyze("1")
        self.assertEqual(result.sdnf, "1")
        self.assertEqual(result.sknf, "1")
        self.assertEqual(result.post["T1"], True)
