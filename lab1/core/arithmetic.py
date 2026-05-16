from __future__ import annotations
from typing import List, Tuple

from constants import TOTAL_BITS, DIVISION_PRECISION
from core.binary_codes import BinaryConverter
from core.utils import BitUtils


class BinaryArithmetic:
    @staticmethod
    def add_additional(a: int, b: int) -> List[str]:
        ab = BinaryConverter.to_additional_code(a)
        bb = BinaryConverter.to_additional_code(b)
        result, _ = BitUtils.add_unsigned(ab, bb)
        return result[-TOTAL_BITS:]

    @staticmethod
    def subtract_additional(minuend: int, subtrahend: int) -> List[str]:
        ab = BinaryConverter.to_additional_code(minuend)
        bb = BinaryConverter.to_additional_code(subtrahend)
        neg_b = BinaryConverter.negate_additional(bb)
        result, _ = BitUtils.add_unsigned(ab, neg_b)
        return result[-TOTAL_BITS:]

    @staticmethod
    def multiply_direct(a: int, b: int) -> List[str]:
        if a == 0 or b == 0:
            return BinaryConverter.to_direct_code(0)

        sign = -1 if (a < 0) ^ (b < 0) else 1
        multiplicand = abs(a)
        multiplier = abs(b)
        result = 0
        while multiplier > 0:
            if multiplier % 2 == 1:
                result += multiplicand
            multiplicand <<= 1
            multiplier //= 2
        result *= sign
        BinaryConverter.normalize_int32(result)
        return BinaryConverter.to_direct_code(result)

    @staticmethod
    def divide_direct(dividend: int, divisor: int, precision: int = DIVISION_PRECISION) -> Tuple[List[str], List[str], List[str], int]:
        if divisor == 0:
            raise ValueError("Division by zero")
        sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
        a = abs(dividend)
        b = abs(divisor)

        quotient_int = 0
        remainder = 0
        bits = []
        # long division in binary not from string parsing, but with int ops
        # integer quotient and remainder
        quotient_int = a // b
        remainder = a % b

        fractional_bits = []
        temp = remainder
        for _ in range(precision):
            temp *= 2
            if temp >= b:
                fractional_bits.append("1")
                temp -= b
            else:
                fractional_bits.append("0")

        q_signed = quotient_int * sign
        r_signed = remainder * sign
        BinaryConverter.normalize_int32(q_signed if q_signed != 0 else 0)
        BinaryConverter.normalize_int32(r_signed if r_signed != 0 else 0)
        return (
            BinaryConverter.to_direct_code(q_signed),
            BinaryConverter.to_direct_code(r_signed),
            fractional_bits,
            q_signed,
        )
