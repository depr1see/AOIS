import unittest
from constants import TOTAL_BITS, MAX_SIGNED_INT32, MIN_SIGNED_INT32
from core.binary_codes import BinaryConverter


class TestBinaryCodes(unittest.TestCase):
    def test_direct_roundtrip(self):
        for n in [0, 1, -1, 42, -42, MAX_SIGNED_INT32]:
            bits = BinaryConverter.to_direct_code(n)
            self.assertEqual(BinaryConverter.from_direct_code(bits), n)

    def test_reverse_roundtrip(self):
        for n in [0, 1, -1, 123, -123]:
            bits = BinaryConverter.to_reverse_code(n)
            self.assertEqual(BinaryConverter.from_reverse_code(bits), n)

    def test_additional_roundtrip(self):
        for n in [0, 1, -1, 123, -123, MIN_SIGNED_INT32]:
            bits = BinaryConverter.to_additional_code(n)
            self.assertEqual(BinaryConverter.from_additional_code(bits), n)

    def test_negative_min_int32(self):
        bits = BinaryConverter.to_additional_code(MIN_SIGNED_INT32)
        self.assertEqual(len(bits), TOTAL_BITS)

    def test_unsigned_convert(self):
        bits = BinaryConverter.decimal_to_binary_unsigned(42, 8)
        self.assertEqual(bits, ["0", "0", "1", "0", "1", "0", "1", "0"])
        self.assertEqual(BinaryConverter.binary_to_decimal_unsigned(bits), 42)


class TestBitUtils(unittest.TestCase):
    def test_create_and_string(self):
        from core.utils import BitUtils
        self.assertEqual(BitUtils.create_bit_array(4), ["0", "0", "0", "0"])
        self.assertEqual(BitUtils.bit_array_to_string(["1", "0", "1"]), "101")

    def test_invert_and_add_one(self):
        from core.utils import BitUtils
        self.assertEqual(BitUtils.invert_bits(["0", "1", "0"], 0, 2), ["1", "0", "1"])
        self.assertEqual(BitUtils.add_one(["0", "0", "1"], 0), ["0", "1", "0"])

    def test_trim_compare_add_sub(self):
        from core.utils import BitUtils
        self.assertEqual(BitUtils.trim_leading_zeros(["0", "0", "1", "0"]), ["1", "0"])
        self.assertEqual(BitUtils.compare_unsigned(["0", "1"], ["1"]), 0)
        self.assertEqual(BitUtils.compare_unsigned(["1", "0"], ["1"]), 1)
        self.assertEqual(BitUtils.compare_unsigned(["0", "1"], ["1", "0"]), -1)
        s, c = BitUtils.add_unsigned(["1", "1"], ["1"])
        self.assertEqual((s, c), (["0", "0"], "1"))
        self.assertEqual(BitUtils.subtract_unsigned(["1", "0", "0"], ["1"]), ["0", "1", "1"])


if __name__ == "__main__":
    unittest.main()
