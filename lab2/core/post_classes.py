"""Классы Поста."""

from __future__ import annotations

from typing import Dict

from core.truth_table import TruthTable


def check_t0(table: TruthTable) -> bool:
    return table.rows[0].value == 0


def check_t1(table: TruthTable) -> bool:
    return table.rows[-1].value == 1


def check_s(table: TruthTable) -> bool:
    values = table.values()
    size = len(values)
    for index in range(size):
        if values[index] == values[size - 1 - index]:
            return False
    return True


def check_m(table: TruthTable) -> bool:
    n = len(table.variables)
    values = table.values()
    for x in range(2 ** n):
        for y in range(2 ** n):
            if (x & y) == x and values[x] > values[y]:
                return False
    return True


def _bit_count(number: int) -> int:
    count = 0
    while number:
        count += number & 1
        number >>= 1
    return count


def check_l(table: TruthTable) -> bool:
    coeffs = list(table.values())
    n = len(table.variables)
    for bit in range(n):
        step = 1 << bit
        for mask in range(len(coeffs)):
            if mask & step:
                coeffs[mask] ^= coeffs[mask ^ step]
    for mask, coeff in enumerate(coeffs):
        if coeff and _bit_count(mask) > 1:
            return False
    return True


def post_classes(table: TruthTable) -> Dict[str, bool]:
    return {"T0": check_t0(table), "T1": check_t1(table), "S": check_s(table), "M": check_m(table), "L": check_l(table)}
