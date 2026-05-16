from __future__ import annotations
from typing import List

from constants import (
    TOTAL_BITS, BCD_TETRAD_BITS, BCD_DIGITS_COUNT,
    BCD_5421_ENCODING, BCD_5421_DECODING
)


def _int_to_bits(value: int, width: int) -> List[str]:
    out = ["0"] * width
    i = width - 1
    while value > 0 and i >= 0:
        out[i] = "1" if value % 2 else "0"
        value //= 2
        i -= 1
    return out


class BCD5421:
    @staticmethod
    def encode_digit(digit: int) -> List[str]:
        if digit not in BCD_5421_ENCODING:
            raise ValueError("digit must be 0..9")
        return list(BCD_5421_ENCODING[digit])

    @staticmethod
    def decode_digit(bits: List[str]) -> int:
        key = "".join(bits)
        if key not in BCD_5421_DECODING:
            raise ValueError("invalid 5421 tetrad")
        return BCD_5421_DECODING[key]

    @staticmethod
    def encode(number: int) -> List[str]:
        sign = "0001" if number < 0 else "0000"
        n = -number if number < 0 else number
        digits = [0] if n == 0 else []
        while n > 0:
            digits.append(n % 10)
            n //= 10
        digits = digits[::-1]
        if len(digits) > BCD_DIGITS_COUNT:
            raise OverflowError("too many digits for 32-bit 5421 BCD layout")
        result = list(sign)
        padding = BCD_DIGITS_COUNT - len(digits)
        result.extend(list("0000") * padding)
        for d in digits:
            result.extend(BCD5421.encode_digit(d))
        return result

    @staticmethod
    def decode(bits: List[str]) -> int:
        sign = -1 if "".join(bits[:4]) == "0001" else 1
        value = 0
        for i in range(4, TOTAL_BITS, 4):
            digit = BCD5421.decode_digit(bits[i:i+4])
            value = value * 10 + digit
        return sign * value

    @staticmethod
    def add(a: int, b: int) -> List[str]:
        result = a + b
        return BCD5421.encode(result)
