import unittest

from lab2_boolean.models.boolean_function import BooleanFunction


class TestBooleanFunction(unittest.TestCase):
    def setUp(self):
        self.func = BooleanFunction("!(!a→!b)∨c")

    def test_truth_table_size(self):
        self.assertEqual(self.func.size, 8)
        self.assertEqual(len(self.func.table), 8)

    def test_sdnf_and_sknf(self):
        sdnf = self.func.sdnf()
        sknf = self.func.sknf()
        self.assertIn("∨", sdnf)
        self.assertIn("∧", sknf)
        self.assertTrue(sdnf)

    def test_numeric_forms(self):
        self.assertEqual(self.func.numeric_sdnf(), "Σm(1, 2, 3, 5, 7)")
        self.assertEqual(self.func.numeric_sknf(), "ΠM(0, 4, 6)")

    def test_index_form(self):
        self.assertEqual(self.func.vector_string(), "01110101")
        self.assertEqual(self.func.index_form(), int("01110101", 2))

    def test_truth_table_text(self):
        text = self.func.truth_table()
        self.assertIn("F", text)
        self.assertIn("a", text)

    def test_assignment_at(self):
        self.assertEqual(self.func.assignment_at(5), {"a": 1, "b": 0, "c": 1})
