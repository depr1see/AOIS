import unittest
from core.arithmetic import BinaryArithmetic
from core.binary_codes import BinaryConverter


class TestArithmetic(unittest.TestCase):
    def test_add(self):
        r = BinaryArithmetic.add_additional(100, 50)
        self.assertEqual(BinaryConverter.from_additional_code(r), 150)

    def test_add_negative(self):
        r = BinaryArithmetic.add_additional(-100, -50)
        self.assertEqual(BinaryConverter.from_additional_code(r), -150)

    def test_subtract(self):
        r = BinaryArithmetic.subtract_additional(100, 50)
        self.assertEqual(BinaryConverter.from_additional_code(r), 50)

    def test_multiply(self):
        r = BinaryArithmetic.multiply_direct(-12, 5)
        self.assertEqual(BinaryConverter.from_direct_code(r), -60)

    def test_multiply_zero(self):
        r = BinaryArithmetic.multiply_direct(0, 999)
        self.assertEqual(BinaryConverter.from_direct_code(r), 0)

    def test_divide(self):
        q, rem, frac, qdec = BinaryArithmetic.divide_direct(10, 3)
        self.assertEqual(BinaryConverter.from_direct_code(q), 3)
        self.assertEqual(BinaryConverter.from_direct_code(rem), 1)
        self.assertEqual(len(frac), 5)

    def test_divide_negative(self):
        q, rem, frac, qdec = BinaryArithmetic.divide_direct(-10, 3)
        self.assertEqual(BinaryConverter.from_direct_code(q), -3)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            BinaryArithmetic.divide_direct(1, 0)


if __name__ == "__main__":
    unittest.main()
