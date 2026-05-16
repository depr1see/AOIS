"""Таблица истинности."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from core.ast_nodes import FormulaNode


@dataclass(frozen=True)
class TruthTableRow:
    assignment: Tuple[int, ...]
    value: int


@dataclass(frozen=True)
class TruthTable:
    variables: Tuple[str, ...]
    rows: Tuple[TruthTableRow, ...]

    def values(self) -> List[int]:
        return [row.value for row in self.rows]

    def true_indices(self) -> List[int]:
        return [index for index, row in enumerate(self.rows) if row.value == 1]

    def false_indices(self) -> List[int]:
        return [index for index, row in enumerate(self.rows) if row.value == 0]


def generate_assignments(variables: Sequence[str]) -> List[Tuple[int, ...]]:
    """Генерирует наборы значений переменных в порядке 0..2^n-1."""
    n = len(variables)
    assignments = []
    for number in range(2 ** n):
        row = []
        for position in range(n):
            shift = n - 1 - position
            row.append((number >> shift) & 1)
        assignments.append(tuple(row))
    return assignments


def build_truth_table(node: FormulaNode, variables: Sequence[str]) -> TruthTable:
    """Строит таблицу истинности для AST."""
    rows = []
    for assignment in generate_assignments(variables):
        env = {var: bool(value) for var, value in zip(variables, assignment)}
        result = int(node.evaluate(env))
        rows.append(TruthTableRow(assignment=assignment, value=result))
    return TruthTable(variables=tuple(variables), rows=tuple(rows))


def assignment_to_env(variables: Sequence[str], assignment: Sequence[int]) -> Dict[str, bool]:
    return {var: bool(value) for var, value in zip(variables, assignment)}
