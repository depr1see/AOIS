from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class DerivativeResult:
    vector: List[int]
    variables: List[str]


class PostAnalyzer:
    """Performs analysis in the Post classes and Zhegalkin polynomial."""

    def __init__(self, vector: Sequence[int], variables: Sequence[str]):
        self.vector = list(vector)
        self.variables = list(variables)
        self.size = len(self.vector)
        self.n = len(self.variables)
        if self.size != 2 ** self.n:
            raise ValueError("Размер вектора должен быть равен 2^n")

    @staticmethod
    def _mobius_transform(values: List[int]) -> List[int]:
        coeffs = values[:]
        n = len(coeffs)
        step = 1
        while step < n:
            for i in range(n):
                if i & step:
                    coeffs[i] ^= coeffs[i ^ step]
            step <<= 1
        return coeffs

    def check_t0(self) -> bool:
        return self.vector[0] == 0

    def check_t1(self) -> bool:
        return self.vector[-1] == 1

    def check_s(self) -> bool:
        for i in range(self.size):
            if self.vector[i] == self.vector[self.size - 1 - i]:
                return False
        return True

    def check_m(self) -> bool:
        for x in range(self.size):
            for y in range(self.size):
                if (x & y) == x and self.vector[x] > self.vector[y]:
                    return False
        return True

    def zhegalkin_coefficients(self) -> List[int]:
        return self._mobius_transform(self.vector)

    def check_l(self) -> bool:
        coeffs = self.zhegalkin_coefficients()
        for index, coeff in enumerate(coeffs):
            if coeff == 1 and bin(index).count("1") > 1:
                return False
        return True

    def zhegalkin_polynomial(self) -> str:
        coeffs = self.zhegalkin_coefficients()
        terms: List[str] = []
        for index, coeff in enumerate(coeffs):
            if coeff != 1:
                continue
            if index == 0:
                terms.append("1")
                continue
            bits = f"{index:0{self.n}b}"
            monomial = "".join(
                var for var, bit in zip(self.variables, bits) if bit == "1"
            )
            terms.append(monomial)
        return " ⊕ ".join(terms) if terms else "0"

    def essential_variables(self) -> Dict[str, bool]:
        result: Dict[str, bool] = {}
        for pos, var in enumerate(self.variables):
            step = 1 << (self.n - 1 - pos)
            essential = False
            for index in range(self.size):
                if index & step:
                    continue
                if self.vector[index] != self.vector[index | step]:
                    essential = True
                    break
            result[var] = essential
        return result

    @staticmethod
    def _derivative_vector(vector: Sequence[int], var_index: int, n: int) -> List[int]:
        step = 1 << (n - 1 - var_index)
        result = []
        for index in range(len(vector)):
            if index & step:
                continue
            result.append(vector[index] ^ vector[index | step])
        return result

    def partial_derivative(self, target_var: str, vector: Sequence[int] | None = None,
                           variables: Sequence[str] | None = None) -> DerivativeResult:
        vector = list(vector) if vector is not None else self.vector
        variables = list(variables) if variables is not None else self.variables
        if target_var not in variables:
            return DerivativeResult(vector=vector, variables=variables)
        idx = variables.index(target_var)
        new_vector = self._derivative_vector(vector, idx, len(variables))
        new_vars = [var for var in variables if var != target_var]
        return DerivativeResult(vector=new_vector, variables=new_vars)

    def mixed_derivative(self, target_vars: Sequence[str]) -> DerivativeResult:
        current_vector = list(self.vector)
        current_vars = list(self.variables)
        for var in target_vars:
            if var not in current_vars:
                raise ValueError(f"Переменная {var!r} отсутствует в функции")
            result = self.partial_derivative(var, current_vector, current_vars)
            current_vector, current_vars = result.vector, result.variables
        return DerivativeResult(vector=current_vector, variables=current_vars)

    @staticmethod
    def vector_to_sdnf(vector: Sequence[int], variables: Sequence[str]) -> str:
        if not vector or not any(vector):
            return "0"
        n = len(variables)
        clauses = []
        for index, value in enumerate(vector):
            if value != 1:
                continue
            bits = f"{index:0{n}b}"
            parts = [
                var if bit == "1" else f"¬{var}"
                for var, bit in zip(variables, bits)
            ]
            clauses.append("(" + " ∧ ".join(parts) + ")")
        return " ∨ ".join(clauses) if clauses else "0"

    @staticmethod
    def vector_to_sknf(vector: Sequence[int], variables: Sequence[str]) -> str:
        if not vector:
            return "1"
        n = len(variables)
        clauses = []
        for index, value in enumerate(vector):
            if value != 0:
                continue
            bits = f"{index:0{n}b}"
            parts = [
                var if bit == "0" else f"¬{var}"
                for var, bit in zip(variables, bits)
            ]
            clauses.append("(" + " ∨ ".join(parts) + ")")
        return " ∧ ".join(clauses) if clauses else "1"
