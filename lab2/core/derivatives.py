"""Булевы производные."""

from __future__ import annotations

from itertools import combinations
from typing import Dict, List, Sequence, Tuple

from core.truth_table import TruthTable


def _toggle_assignment(assignment: Tuple[int, ...], positions: Sequence[int]) -> Tuple[int, ...]:
    result = list(assignment)
    for position in positions:
        result[position] = 1 - result[position]
    return tuple(result)


def boolean_derivative(table: TruthTable, positions: Sequence[int]) -> List[int]:
    """Производная по заданным переменным.

    positions задаются как индексы переменных в таблице (0..n-1).
    """
    values_by_assignment = {row.assignment: row.value for row in table.rows}
    derivative = []
    for row in table.rows:
        toggled = _toggle_assignment(row.assignment, positions)
        derivative.append(row.value ^ values_by_assignment[toggled])
    return derivative


def derivative_form(table: TruthTable, positions: Sequence[int]) -> str:
    values = boolean_derivative(table, positions)
    return "".join(str(v) for v in values)


def derivative_summary(table: TruthTable, max_order: int = 4) -> Dict[str, str]:
    variables = table.variables
    summary: Dict[str, str] = {}
    n = len(variables)
    limit = min(max_order, n)
    for order in range(1, limit + 1):
        for combo in combinations(range(n), order):
            name = ",".join(variables[index] for index in combo)
            summary[name] = derivative_form(table, combo)
    return summary


def fictive_variables(table: TruthTable) -> List[str]:
    """Переменная фиктивна, если при её смене значение функции не меняется."""
    result = []
    for index, var in enumerate(table.variables):
        if all(value == 0 for value in boolean_derivative(table, [index])):
            result.append(var)
    return result
