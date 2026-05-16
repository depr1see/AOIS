from __future__ import annotations
from typing import List, Tuple

from constants import TOTAL_BITS, SIGN_BIT_INDEX


class BitUtils:
    @staticmethod
    def create_bit_array(size: int = TOTAL_BITS) -> List[str]:
        return ["0"] * size

    @staticmethod
    def bit_array_to_string(bit_array: List[str]) -> str:
        return "".join(bit_array)

    @staticmethod
    def invert_bits(bit_array: List[str], start_index: int = 0, end_index: int | None = None) -> List[str]:
        if end_index is None:
            end_index = len(bit_array) - 1
        result = bit_array[:]
        for i in range(start_index, end_index + 1):
            result[i] = "1" if result[i] == "0" else "0"
        return result

    @staticmethod
    def add_one(bit_array: List[str], start_index: int = 0) -> List[str]:
        result = bit_array[:]
        carry = 1
        for i in range(len(result) - 1, start_index - 1, -1):
            if carry == 0:
                break
            if result[i] == "0":
                result[i] = "1"
                carry = 0
            else:
                result[i] = "0"
        return result

    @staticmethod
    def trim_leading_zeros(bits: List[str]) -> List[str]:
        i = 0
        while i < len(bits) - 1 and bits[i] == "0":
            i += 1
        return bits[i:]

    @staticmethod
    def compare_unsigned(a: List[str], b: List[str]) -> int:
        aa = BitUtils.trim_leading_zeros(a[:])
        bb = BitUtils.trim_leading_zeros(b[:])
        if len(aa) != len(bb):
            return 1 if len(aa) > len(bb) else -1
        for x, y in zip(aa, bb):
            if x != y:
                return 1 if x == "1" else -1
        return 0

    @staticmethod
    def add_unsigned(a: List[str], b: List[str]) -> Tuple[List[str], str]:
        max_len = max(len(a), len(b))
        aa = ["0"] * (max_len - len(a)) + a
        bb = ["0"] * (max_len - len(b)) + b
        result = ["0"] * max_len
        carry = 0
        for i in range(max_len - 1, -1, -1):
            total = (1 if aa[i] == "1" else 0) + (1 if bb[i] == "1" else 0) + carry
            result[i] = "1" if total % 2 else "0"
            carry = 1 if total >= 2 else 0
        return result, "1" if carry else "0"

    @staticmethod
    def subtract_unsigned(a: List[str], b: List[str]) -> List[str]:
        # assumes a >= b
        max_len = max(len(a), len(b))
        aa = ["0"] * (max_len - len(a)) + a
        bb = ["0"] * (max_len - len(b)) + b
        result = ["0"] * max_len
        borrow = 0
        for i in range(max_len - 1, -1, -1):
            av = 1 if aa[i] == "1" else 0
            bv = 1 if bb[i] == "1" else 0
            diff = av - bv - borrow
            if diff >= 0:
                result[i] = "1" if diff == 1 else "0"
                borrow = 0
            else:
                result[i] = "1"
                borrow = 1
        return result
