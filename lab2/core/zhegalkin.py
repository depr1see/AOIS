"""Полином Жегалкина."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from constants import UNICODE_AND
from core.truth_table import TruthTable


def _mask_to_term(mask: int, variables: Sequence[str]) -> str:
    if mask == 0:
        return "1"
    n = len(variables)
    factors = []
    for position in range(n):
        bit_index = n - 1 - position
        if mask & (1 << bit_index):
            factors.append(variables[position])
    return UNICODE_AND.join(factors)


def zhegalkin_polynomial(table: TruthTable) -> Tuple[str, List[int]]:
    coeffs = list(table.values())
    n = len(table.variables)
    for bit in range(n):
        step = 1 << bit
        for mask in range(len(coeffs)):
            if mask & step:
                coeffs[mask] ^= coeffs[mask ^ step]

    masks = [mask for mask, coeff in enumerate(coeffs) if coeff == 1]
    terms = [_mask_to_term(mask, table.variables) for mask in masks]
    if not terms:
        return "0", []
    return " ⊕ ".join(terms), masks
