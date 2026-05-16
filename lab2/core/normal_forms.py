"""Построение СДНФ, СКНФ и числовых форм."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from constants import UNICODE_AND, UNICODE_NOT, UNICODE_OR
from core.truth_table import TruthTable


def _literal(variable: str, value: int, dnf: bool) -> str:
    if dnf:
        return variable if value == 1 else f"{UNICODE_NOT}{variable}"
    return variable if value == 0 else f"{UNICODE_NOT}{variable}"


def build_sdnf(table: TruthTable) -> Tuple[str, List[int]]:
    terms = []
    indices = []
    for idx, row in enumerate(table.rows):
        if row.value == 1:
            indices.append(idx)
            literals = [_literal(var, bit, True) for var, bit in zip(table.variables, row.assignment)]
            terms.append("(" + UNICODE_AND.join(literals) + ")")
    if not terms:
        return "0", []
    if len(terms) == 2 ** len(table.variables):
        return "1", indices
    return UNICODE_OR.join(terms), indices


def build_sknf(table: TruthTable) -> Tuple[str, List[int]]:
    clauses = []
    indices = []
    for idx, row in enumerate(table.rows):
        if row.value == 0:
            indices.append(idx)
            literals = [_literal(var, bit, False) for var, bit in zip(table.variables, row.assignment)]
            clauses.append("(" + UNICODE_OR.join(literals) + ")")
    if not clauses:
        return "1", []
    if len(clauses) == 2 ** len(table.variables):
        return "0", indices
    return UNICODE_AND.join(clauses), indices


def build_numeric_form(indices: Sequence[int], form: str) -> str:
    joined = ",".join(str(index) for index in indices)
    if form.upper() == "DNF":
        return f"Σ({joined})"
    return f"Π({joined})"


def build_index_form(table: TruthTable) -> Tuple[int, str]:
    bits = "".join(str(row.value) for row in table.rows)
    index_value = 0
    total = len(bits)
    for position, bit in enumerate(bits):
        if bit == "1":
            index_value += 2 ** (total - 1 - position)
    return index_value, bits
