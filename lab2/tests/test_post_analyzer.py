import unittest

from lab2_boolean.models.post_analyzer import PostAnalyzer


class TestPostAnalyzer(unittest.TestCase):
    def test_post_classes_and_polynomial(self):
        vector = [0, 0, 0, 0]
        analyzer = PostAnalyzer(vector, ["a", "b"])
        self.assertTrue(analyzer.check_t0())
        self.assertFalse(analyzer.check_t1())
        self.assertFalse(analyzer.check_s())
        self.assertTrue(analyzer.check_m())
        self.assertTrue(analyzer.check_l())
        self.assertEqual(analyzer.zhegalkin_polynomial(), "0")
        self.assertEqual(analyzer.essential_variables(), {"a": False, "b": False})

    def test_derivative(self):
        vector = [0, 1, 1, 0]  # XOR
        analyzer = PostAnalyzer(vector, ["a", "b"])
        d_a = analyzer.partial_derivative("a")
        self.assertEqual(d_a.vector, [1, 1])
        self.assertEqual(d_a.variables, ["b"])

        d_ab = analyzer.mixed_derivative(["a", "b"])
        self.assertEqual(d_ab.vector, [0])
        self.assertEqual(d_ab.variables, [])

    def test_vector_to_forms(self):
        vector = [0, 0, 1, 1]
        self.assertIn("a", PostAnalyzer.vector_to_sdnf(vector, ["a", "b"]))
        self.assertIn("¬a", PostAnalyzer.vector_to_sknf([1, 1, 0, 0], ["a", "b"]))
