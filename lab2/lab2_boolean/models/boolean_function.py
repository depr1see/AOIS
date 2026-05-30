from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, List, Sequence

from ..core.constants import VALID_VARIABLES
from ..core.parser import ExpressionParser, ExpressionError


@dataclass(frozen=True)
class TruthTableRow:
    assignment: Dict[str, int]
    result: int


class BooleanFunction:
    """Truth-table based representation of a boolean function."""

    def __init__(self, expression: str | ExpressionParser):
        if isinstance(expression, ExpressionParser):
            self.parser = expression
        else:
            self.parser = ExpressionParser(expression)

        self.variables: List[str] = self.parser.variables()
        if len(self.variables) > len(VALID_VARIABLES):
            raise ValueError("Поддерживается не более 5 переменных")

        self.table: List[TruthTableRow] = []
        self.vector: List[int] = []
        self._build_truth_table()

    @property
    def size(self) -> int:
        return len(self.vector)

    def _build_truth_table(self) -> None:
        self.table.clear()
        self.vector.clear()
        for bits in product([0, 1], repeat=len(self.variables)):
            assignment = dict(zip(self.variables, bits))
            result = self.parser.evaluate(assignment)
            self.table.append(TruthTableRow(assignment=assignment, result=result))
            self.vector.append(result)

    def vector_string(self) -> str:
        return "".join(str(v) for v in self.vector)

    def index_form(self) -> int:
        return int(self.vector_string() or "0", 2)

    def numeric_sdnf(self) -> str:
        ones = [str(i) for i, value in enumerate(self.vector) if value == 1]
        return f"Σm({', '.join(ones)})" if ones else "Σm()"

    def numeric_sknf(self) -> str:
        zeros = [str(i) for i, value in enumerate(self.vector) if value == 0]
        return f"ΠM({', '.join(zeros)})" if zeros else "ΠM()"

    def _term_to_sdnf_clause(self, assignment: Dict[str, int]) -> str:
        parts = [var if assignment[var] == 1 else f"¬{var}" for var in self.variables]
        return "(" + " ∧ ".join(parts) + ")"

    def _term_to_sknf_clause(self, assignment: Dict[str, int]) -> str:
        parts = [var if assignment[var] == 0 else f"¬{var}" for var in self.variables]
        return "(" + " ∨ ".join(parts) + ")"

    def sdnf(self) -> str:
        clauses = [
            self._term_to_sdnf_clause(row.assignment)
            for row in self.table
            if row.result == 1
        ]
        return " ∨ ".join(clauses) if clauses else "0"

    def sknf(self) -> str:
        clauses = [
            self._term_to_sknf_clause(row.assignment)
            for row in self.table
            if row.result == 0
        ]
        return " ∧ ".join(clauses) if clauses else "1"

    def truth_table_rows(self) -> List[TruthTableRow]:
        return list(self.table)

    def truth_table(self) -> str:
        header = " | ".join(self.variables + ["F"])
        lines = [header, "-" * len(header)]
        for row in self.table:
            values = [str(row.assignment[var]) for var in self.variables]
            lines.append(" | ".join(values + [str(row.result)]))
        return "\n".join(lines)

    def assignment_at(self, index: int) -> Dict[str, int]:
        bits = f"{index:0{len(self.variables)}b}"
        return {var: int(bit) for var, bit in zip(self.variables, bits)}
