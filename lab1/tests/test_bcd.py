import unittest
from core.bcd_5421 import BCD5421


class TestBCD5421(unittest.TestCase):
    def test_encode_decode_zero(self):
        bits = BCD5421.encode(0)
        self.assertEqual(BCD5421.decode(bits), 0)

    def test_encode_decode_positive(self):
        bits = BCD5421.encode(42)
        self.assertEqual(BCD5421.decode(bits), 42)

    def test_encode_decode_negative(self):
        bits = BCD5421.encode(-42)
        self.assertEqual(BCD5421.decode(bits), -42)

    def test_add(self):
        bits = BCD5421.add(25, 17)
        self.assertEqual(BCD5421.decode(bits), 42)

    def test_add_negative(self):
        bits = BCD5421.add(-25, -17)
        self.assertEqual(BCD5421.decode(bits), -42)

    def test_invalid_digit_encoding(self):
        with self.assertRaises(ValueError):
            BCD5421.encode_digit(10)


if __name__ == "__main__":
    unittest.main()
