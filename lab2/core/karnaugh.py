"""Карта Карно."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple


def _gray_sequence(bits: int) -> List[int]:
    return [index ^ (index >> 1) for index in range(2 ** bits)]


def _gray_to_bits(value: int, bits: int) -> Tuple[int, ...]:
    result = []
    for shift in range(bits - 1, -1, -1):
        result.append((value >> shift) & 1)
    return tuple(result)


@dataclass(frozen=True)
class KarnaughMap:
    row_vars: Tuple[str, ...]
    col_vars: Tuple[str, ...]
    row_headers: Tuple[str, ...]
    col_headers: Tuple[str, ...]
    grid: Tuple[Tuple[int, ...], ...]


def build_karnaugh_map(values: Sequence[int], variables: Sequence[str]) -> KarnaughMap:
    n = len(variables)
    row_var_count = n // 2
    col_var_count = n - row_var_count
    row_gray = _gray_sequence(row_var_count)
    col_gray = _gray_sequence(col_var_count)

    row_headers = tuple(f"{value:0{row_var_count}b}" for value in row_gray) if row_var_count else ("",)
    col_headers = tuple(f"{value:0{col_var_count}b}" for value in col_gray) if col_var_count else ("",)

    grid: List[List[int]] = []
    for row_value in row_gray:
        row_bits = _gray_to_bits(row_value, row_var_count)
        row_list = []
        for col_value in col_gray:
            col_bits = _gray_to_bits(col_value, col_var_count)
            assignment = row_bits + col_bits
            index = 0
            for bit in assignment:
                index = (index << 1) | bit
            row_list.append(values[index])
        grid.append(row_list)

    return KarnaughMap(
        row_vars=tuple(variables[:row_var_count]),
        col_vars=tuple(variables[row_var_count:]),
        row_headers=row_headers,
        col_headers=col_headers,
        grid=tuple(tuple(row) for row in grid),
    )


def karnaugh_to_text(map_: KarnaughMap) -> str:
    header = ["    "] + [f"{label:>3}" for label in map_.col_headers]
    lines = ["".join(header)]
    for label, row in zip(map_.row_headers, map_.grid):
        lines.append(f"{label:>3} " + "".join(f"{value:>3}" for value in row))
    return "\n".join(lines)
