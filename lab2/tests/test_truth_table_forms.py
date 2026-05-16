import unittest

from core.normal_forms import build_index_form, build_numeric_form, build_sdnf, build_sknf
from core.parser import FormulaParser
from core.truth_table import build_truth_table, generate_assignments


class TestTruthTableForms(unittest.TestCase):
    def setUp(self):
        self.ast = FormulaParser("!(!a->!b)|c").parse()
        self.vars = sorted(self.ast.variables(), key=lambda x: "abcde".index(x))
        self.table = build_truth_table(self.ast, self.vars)

    def test_generate_assignments(self):
        self.assertEqual(generate_assignments(["a", "b", "c"]), [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)])

    def test_truth_table_size(self):
        self.assertEqual(len(self.table.rows), 8)

    def test_sdnf_contains_terms(self):
        sdnf, indices = build_sdnf(self.table)
        self.assertIn("a", sdnf)
        self.assertGreater(len(indices), 0)

    def test_sknf_contains_terms(self):
        sknf, indices = build_sknf(self.table)
        self.assertIsInstance(sknf, str)
        self.assertGreater(len(indices), 0)

    def test_numeric_forms(self):
        sdnf, sdnf_idx = build_sdnf(self.table)
        sknf, sknf_idx = build_sknf(self.table)
        self.assertTrue(build_numeric_form(sdnf_idx, "DNF").startswith("Σ("))
        self.assertTrue(build_numeric_form(sknf_idx, "CNF").startswith("Π("))

    def test_index_form(self):
        index_value, bits = build_index_form(self.table)
        self.assertEqual(len(bits), 8)
        self.assertIsInstance(index_value, int)
