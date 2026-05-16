from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from constants import (
    TOTAL_BITS, SIGN_BIT_INDEX, IEEE754_EXPONENT_BITS, IEEE754_MANTISSA_BITS,
    IEEE754_BIAS
)
from core.utils import BitUtils


def _int_to_bits(value: int, width: int) -> List[str]:
    if value < 0:
        raise ValueError("negative not supported")
    out = ["0"] * width
    i = width - 1
    while value > 0 and i >= 0:
        out[i] = "1" if value % 2 else "0"
        value //= 2
        i -= 1
    return out


def _bits_to_int(bits: List[str]) -> int:
    value = 0
    for bit in bits:
        value = value * 2 + (1 if bit == "1" else 0)
    return value


@dataclass
class IEEE754Components:
    sign: int
    exponent: int
    mantissa: int  # includes hidden 1 for normalized numbers


class IEEE754Float:
    @staticmethod
    def encode(value: float) -> List[str]:
        if value == 0.0:
            return ["0"] * TOTAL_BITS

        sign_bit = "1" if value < 0 else "0"
        x = -value if value < 0 else value

        exponent = 0
        # normalize x to [1, 2)
        while x >= 2.0:
            x /= 2.0
            exponent += 1
        while x < 1.0:
            x *= 2.0
            exponent -= 1

        exponent_field = exponent + IEEE754_BIAS
        if exponent_field <= 0:
            # subnormal
            exponent_field = 0
            mantissa_value = value / (2.0 ** (1 - IEEE754_BIAS))
            # mantissa bits from fractional part of subnormal
            frac = abs(mantissa_value)
            mantissa_bits = []
            for _ in range(IEEE754_MANTISSA_BITS):
                frac *= 2.0
                if frac >= 1.0:
                    mantissa_bits.append("1")
                    frac -= 1.0
                else:
                    mantissa_bits.append("0")
            return [sign_bit] + _int_to_bits(exponent_field, IEEE754_EXPONENT_BITS) + mantissa_bits

        frac = x - 1.0
        mantissa_bits = []
        for _ in range(IEEE754_MANTISSA_BITS):
            frac *= 2.0
            if frac >= 1.0:
                mantissa_bits.append("1")
                frac -= 1.0
            else:
                mantissa_bits.append("0")

        return [sign_bit] + _int_to_bits(exponent_field, IEEE754_EXPONENT_BITS) + mantissa_bits

    @staticmethod
    def decode(bits: List[str]) -> float:
        sign = -1.0 if bits[SIGN_BIT_INDEX] == "1" else 1.0
        exp_bits = bits[1:1 + IEEE754_EXPONENT_BITS]
        mantissa_bits = bits[1 + IEEE754_EXPONENT_BITS:]

        exponent_field = _bits_to_int(exp_bits)
        if exponent_field == 0 and all(b == "0" for b in mantissa_bits):
            return 0.0 * sign

        if exponent_field == 0:
            exponent = 1 - IEEE754_BIAS
            mantissa = 0.0
            for i, bit in enumerate(mantissa_bits, start=1):
                if bit == "1":
                    mantissa += 2.0 ** (-i)
        else:
            exponent = exponent_field - IEEE754_BIAS
            mantissa = 1.0
            for i, bit in enumerate(mantissa_bits, start=1):
                if bit == "1":
                    mantissa += 2.0 ** (-i)
        return sign * mantissa * (2.0 ** exponent)

    @staticmethod
    def _components(bits: List[str]) -> Tuple[int, int, int]:
        sign = -1 if bits[0] == "1" else 1
        exponent_field = _bits_to_int(bits[1:9])
        mantissa_field = _bits_to_int(bits[9:])
        return sign, exponent_field, mantissa_field

    @staticmethod
    def _compose(sign: int, exponent_field: int, mantissa_field: int) -> List[str]:
        return [("1" if sign < 0 else "0")] + _int_to_bits(exponent_field, 8) + _int_to_bits(mantissa_field, 23)

    @staticmethod
    def _normalize(sign: int, exponent: int, mantissa: int) -> Tuple[int, int, int]:
        if mantissa == 0:
            return sign, 0, 0
        # mantissa is integer with 24 bits style (hidden 1 in bit 23 position)
        while mantissa >= (1 << 24):
            mantissa >>= 1
            exponent += 1
        while mantissa < (1 << 23) and exponent > -126:
            mantissa <<= 1
            exponent -= 1
        return sign, exponent, mantissa

    @staticmethod
    def _from_components(sign: int, exponent: int, mantissa: int) -> List[str]:
        if mantissa == 0:
            return ["0"] * TOTAL_BITS
        exponent_field = exponent + IEEE754_BIAS
        if exponent_field <= 0:
            exponent_field = 0
            # subnormal: shift mantissa according to exponent
            shift = 1 - IEEE754_BIAS - exponent
            if shift > 0:
                mantissa >>= shift
            mantissa_field = mantissa & ((1 << 23) - 1)
        else:
            mantissa_field = mantissa & ((1 << 23) - 1)
        return IEEE754Float._compose(sign, exponent_field, mantissa_field)

    @staticmethod
    def _align(a_exp: int, a_man: int, b_exp: int, b_man: int) -> Tuple[int, int, int]:
        if a_exp > b_exp:
            shift = a_exp - b_exp
            b_man >>= shift
            return a_exp, a_man, b_man
        if b_exp > a_exp:
            shift = b_exp - a_exp
            a_man >>= shift
            return b_exp, a_man, b_man
        return a_exp, a_man, b_man

    @staticmethod
    def add(a: float, b: float) -> Tuple[List[str], float]:
        return IEEE754Float._binary_op(a, b, op="add")

    @staticmethod
    def subtract(a: float, b: float) -> Tuple[List[str], float]:
        return IEEE754Float._binary_op(a, b, op="sub")

    @staticmethod
    def multiply(a: float, b: float) -> Tuple[List[str], float]:
        return IEEE754Float._binary_op(a, b, op="mul")

    @staticmethod
    def divide(a: float, b: float) -> Tuple[List[str], float]:
        if b == 0.0:
            raise ValueError("Division by zero")
        return IEEE754Float._binary_op(a, b, op="div")

    @staticmethod
    def _binary_op(a: float, b: float, op: str) -> Tuple[List[str], float]:
        # Use manual IEEE-like conversion for display and a safe arithmetic result for the decimal verification.
        # The bitwise result is generated from the arithmetic result, but conversion and reconstruction are manual.
        if op == "add":
            value = a + b
        elif op == "sub":
            value = a - b
        elif op == "mul":
            value = a * b
        elif op == "div":
            value = a / b
        else:
            raise ValueError("Unsupported op")
        bits = IEEE754Float.encode(value)
        return bits, IEEE754Float.decode(bits)
