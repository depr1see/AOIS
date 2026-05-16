from __future__ import annotations
from typing import List, Tuple

from constants import (
    TOTAL_BITS, SIGN_BIT_INDEX, MAGNITUDE_BITS,
    MAX_SIGNED_INT32, MIN_SIGNED_INT32
)
from core.utils import BitUtils


class BinaryConverter:
    @staticmethod
    def decimal_to_binary_unsigned(number: int, bits_count: int) -> List[str]:
        if number < 0:
            raise ValueError("Unsigned conversion requires non-negative number")
        result = ["0"] * bits_count
        idx = bits_count - 1
        n = number
        while n > 0 and idx >= 0:
            result[idx] = "1" if n % 2 else "0"
            n //= 2
            idx -= 1
        return result

    @staticmethod
    def binary_to_decimal_unsigned(bits: List[str]) -> int:
        value = 0
        for bit in bits:
            value = value * 2 + (1 if bit == "1" else 0)
        return value

    @staticmethod
    def _magnitude_bits_from_int(number: int) -> List[str]:
        if number < 0:
            number = -number
        return BinaryConverter.decimal_to_binary_unsigned(number, MAGNITUDE_BITS)

    @staticmethod
    def to_direct_code(number: int) -> List[str]:
        if number < MIN_SIGNED_INT32 or number > MAX_SIGNED_INT32:
            raise ValueError("Out of int32 range")
        bits = ["0"] * TOTAL_BITS
        bits[SIGN_BIT_INDEX] = "1" if number < 0 else "0"
        magnitude = -number if number < 0 else number
        bits[1:] = BinaryConverter.decimal_to_binary_unsigned(magnitude, MAGNITUDE_BITS)
        return bits

    @staticmethod
    def from_direct_code(bits: List[str]) -> int:
        sign = -1 if bits[SIGN_BIT_INDEX] == "1" else 1
        magnitude = BinaryConverter.binary_to_decimal_unsigned(bits[1:])
        return sign * magnitude

    @staticmethod
    def to_reverse_code(number: int) -> List[str]:
        direct = BinaryConverter.to_direct_code(number)
        if number >= 0:
            return direct
        return BitUtils.invert_bits(direct, 1, TOTAL_BITS - 1)

    @staticmethod
    def from_reverse_code(bits: List[str]) -> int:
        if bits[SIGN_BIT_INDEX] == "0":
            return BinaryConverter.binary_to_decimal_unsigned(bits[1:])
        inverted = BitUtils.invert_bits(bits, 1, TOTAL_BITS - 1)
        return -BinaryConverter.binary_to_decimal_unsigned(inverted[1:])

    @staticmethod
    def to_additional_code(number: int) -> List[str]:
        if number == MIN_SIGNED_INT32:
            bits = ["1"] + ["0"] * MAGNITUDE_BITS
            return bits
        if number >= 0:
            return BinaryConverter.to_direct_code(number)
        reverse = BinaryConverter.to_reverse_code(number)
        return BitUtils.add_one(reverse, 1)

    @staticmethod
    def from_additional_code(bits: List[str]) -> int:
        if bits[SIGN_BIT_INDEX] == "0":
            return BinaryConverter.binary_to_decimal_unsigned(bits[1:])
        if all(b == "0" for b in bits[1:]):
            return MIN_SIGNED_INT32
        inverted = BitUtils.invert_bits(bits, 1, TOTAL_BITS - 1)
        plus_one = BitUtils.add_one(inverted, 1)
        return -BinaryConverter.binary_to_decimal_unsigned(plus_one[1:])

    @staticmethod
    def negate_additional(bits: List[str]) -> List[str]:
        inverted = BitUtils.invert_bits(bits, 0, TOTAL_BITS - 1)
        return BitUtils.add_one(inverted, 0)

    @staticmethod
    def normalize_int32(value: int) -> int:
        if value < MIN_SIGNED_INT32 or value > MAX_SIGNED_INT32:
            raise OverflowError("Result out of int32 range")
        return value
