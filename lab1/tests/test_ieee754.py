import unittest
from core.ieee754 import IEEE754Float
from constants import TOTAL_BITS


class TestIEEE754(unittest.TestCase):
    def test_encode_decode_zero(self):
        bits = IEEE754Float.encode(0.0)
        self.assertEqual(bits, ["0"] * TOTAL_BITS)
        self.assertEqual(IEEE754Float.decode(bits), 0.0)

    def test_encode_decode_positive(self):
        bits = IEEE754Float.encode(3.5)
        self.assertAlmostEqual(IEEE754Float.decode(bits), 3.5, places=6)

    def test_encode_decode_negative(self):
        bits = IEEE754Float.encode(-2.25)
        self.assertAlmostEqual(IEEE754Float.decode(bits), -2.25, places=6)

    def test_add(self):
        bits, value = IEEE754Float.add(1.5, 2.25)
        self.assertAlmostEqual(value, 3.75, places=6)

    def test_subtract(self):
        bits, value = IEEE754Float.subtract(5.5, 2.0)
        self.assertAlmostEqual(value, 3.5, places=6)

    def test_multiply(self):
        bits, value = IEEE754Float.multiply(2.5, 4.0)
        self.assertAlmostEqual(value, 10.0, places=6)

    def test_divide(self):
        bits, value = IEEE754Float.divide(7.5, 2.5)
        self.assertAlmostEqual(value, 3.0, places=6)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            IEEE754Float.divide(1.0, 0.0)


    def test_private_helpers(self):
        self.assertEqual(IEEE754Float._components(["0"] + ["0"] * 31), (1, 0, 0))
        self.assertEqual(
            IEEE754Float._compose(1, 127, 0)[:9],
            ["0", "0", "1", "1", "1", "1", "1", "1", "1"]
        )
        self.assertEqual(IEEE754Float._normalize(1, 0, 1 << 22), (1, -1, 1 << 23))
        self.assertEqual(IEEE754Float._from_components(1, 0, 0), ["0"] * TOTAL_BITS)
        self.assertEqual(IEEE754Float._align(5, 8, 3, 2), (5, 8, 0))

    def test_subnormal_encoding(self):
        bits = IEEE754Float.encode(1e-40)
        self.assertEqual(len(bits), TOTAL_BITS)
        self.assertEqual(bits[0], "0")

    def test_invalid_binary_op(self):
        with self.assertRaises(ValueError):
            IEEE754Float._binary_op(1.0, 2.0, op="x")


if __name__ == "__main__":
    unittest.main()
