from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Set, Tuple


@dataclass(frozen=True)
class Implicant:
    pattern: str
    covered: frozenset[int]

    @property
    def literal_count(self) -> int:
        return sum(1 for ch in self.pattern if ch != "-")


@dataclass(frozen=True)
class MergeStage:
    stage_number: int
    terms: Tuple[str, ...]


class Minimizer:
    """Quine-McCluskey style minimizer with traceable stages."""

    def __init__(self, vector: Sequence[int], variables: Sequence[str]):
        self.vector = list(vector)
        self.variables = list(variables)
        self.n = len(self.variables)
        if len(self.vector) != 2 ** self.n:
            raise ValueError("Размер вектора должен быть равен 2^n")

    def _target_indices(self, mode: str) -> List[int]:
        target = 1 if mode.upper() == "DNF" else 0
        return [index for index, value in enumerate(self.vector) if value == target]

    @staticmethod
    def _bits(index: int, n: int) -> str:
        return f"{index:0{n}b}"

    @staticmethod
    def _combine(a: str, b: str) -> str | None:
        diff = 0
        merged = []
        for x, y in zip(a, b):
            if x == y:
                merged.append(x)
                continue
            if x == "-" or y == "-":
                return None
            diff += 1
            merged.append("-")
            if diff > 1:
                return None
        return "".join(merged) if diff == 1 else None

    @staticmethod
    def _covers(pattern: str, bits: str) -> bool:
        return all(p == "-" or p == b for p, b in zip(pattern, bits))

    def _initial_terms(self, mode: str) -> List[str]:
        return [self._bits(index, self.n) for index in self._target_indices(mode)]

    def _prime_implicants_with_stages(self, initial_terms: Sequence[str]) -> Tuple[List[MergeStage], List[str]]:
        current = sorted(set(initial_terms))
        stages: List[MergeStage] = []
        prime_implicants: Set[str] = set()

        stage_no = 1
        while current:
            stages.append(MergeStage(stage_number=stage_no, terms=tuple(current)))
            next_terms: Set[str] = set()
            used: Set[str] = set()

            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    merged = self._combine(current[i], current[j])
                    if merged is not None:
                        next_terms.add(merged)
                        used.add(current[i])
                        used.add(current[j])

            prime_implicants.update(term for term in current if term not in used)
            if not next_terms:
                break
            current = sorted(next_terms)
            stage_no += 1

        return stages, sorted(prime_implicants)

    def _build_implicants(self, prime_patterns: Sequence[str], mode: str) -> List[Implicant]:
        target_indices = set(self._target_indices(mode))
        implicants = []
        for pattern in prime_patterns:
            covered = frozenset(
                index for index in target_indices
                if self._covers(pattern, self._bits(index, self.n))
            )
            implicants.append(Implicant(pattern=pattern, covered=covered))
        return implicants

    def _choose_min_cover(self, implicants: Sequence[Implicant], universe: Set[int]) -> List[Implicant]:
        if not universe:
            return []

        best: List[Implicant] | None = None
        best_cost: Tuple[int, int] | None = None

        imp_list = list(implicants)
        for r in range(1, len(imp_list) + 1):
            for combo in combinations(imp_list, r):
                covered = set().union(*(imp.covered for imp in combo))
                if not universe.issubset(covered):
                    continue
                cost = (sum(imp.literal_count for imp in combo), len(combo))
                if best is None or cost < best_cost:
                    best = list(combo)
                    best_cost = cost
        return best or []

    def _select_cover(self, prime_patterns: Sequence[str], mode: str) -> List[str]:
        implicants = self._build_implicants(prime_patterns, mode)
        universe = set(self._target_indices(mode))

        if not universe:
            return []

        # Essential implicants first.
        selected: List[Implicant] = []
        remaining_universe = set(universe)
        coverage: Dict[int, List[Implicant]] = {idx: [] for idx in universe}
        for implicant in implicants:
            for idx in implicant.covered:
                coverage[idx].append(implicant)

        essential = []
        for idx, items in coverage.items():
            if len(items) == 1:
                essential.append(items[0])

        for imp in dict.fromkeys(essential):
            if imp not in selected:
                selected.append(imp)
                remaining_universe -= set(imp.covered)

        remaining_implicants = [
            imp for imp in implicants if imp not in selected
        ]
        selected.extend(self._choose_min_cover(remaining_implicants, remaining_universe))
        # Keep output deterministic.
        unique = []
        seen = set()
        for imp in selected:
            if imp.pattern not in seen:
                unique.append(imp)
                seen.add(imp.pattern)
        return [imp.pattern for imp in unique]

    def _term_to_expression(self, pattern: str, mode: str) -> str:
        parts: List[str] = []
        for var, bit in zip(self.variables, pattern):
            if bit == "-":
                continue
            if mode == "DNF":
                parts.append(var if bit == "1" else f"¬{var}")
            else:
                parts.append(var if bit == "0" else f"¬{var}")

        if not parts:
            return "1" if mode == "DNF" else "0"

        if mode == "DNF":
            return parts[0] if len(parts) == 1 else "(" + " ∧ ".join(parts) + ")"
        return parts[0] if len(parts) == 1 else "(" + " ∨ ".join(parts) + ")"

    def _format_result(self, patterns: Sequence[str], mode: str) -> str:
        if not patterns:
            return "0" if mode == "DNF" else "1"
        terms = sorted(self._term_to_expression(pattern, mode) for pattern in patterns)
        separator = " ∨ " if mode == "DNF" else " ∧ "
        return separator.join(terms)

    def calculation_method(self, mode: str = "DNF") -> Dict[str, object]:
        mode = mode.upper()
        initial = self._initial_terms(mode)
        stages, primes = self._prime_implicants_with_stages(initial)
        selected = self._select_cover(primes, mode)
        return {
            "mode": mode,
            "initial_terms": initial,
            "stages": stages,
            "prime_implicants": primes,
            "selected_patterns": selected,
            "result": self._format_result(selected, mode),
        }

    def table_method(self, mode: str = "DNF") -> Dict[str, object]:
        mode = mode.upper()
        initial = self._initial_terms(mode)
        stages, primes = self._prime_implicants_with_stages(initial)
        implicants = self._build_implicants(primes, mode)

        table: List[Dict[str, object]] = []
        for imp in implicants:
            row = {
                "pattern": imp.pattern,
                "expression": self._term_to_expression(imp.pattern, mode),
                "coverage": [1 if index in imp.covered else 0 for index in self._target_indices(mode)],
            }
            table.append(row)

        selected = self._select_cover(primes, mode)
        return {
            "mode": mode,
            "initial_terms": initial,
            "stages": stages,
            "prime_implicants": primes,
            "coverage_table": table,
            "selected_patterns": selected,
            "result": self._format_result(selected, mode),
        }

    @staticmethod
    def _gray_code(bits: int) -> List[str]:
        if bits == 0:
            return [""]
        prev = Minimizer._gray_code(bits - 1)
        return ["0" + code for code in prev] + ["1" + code for code in reversed(prev)]

    def _karnaugh_layout(self) -> Tuple[List[str], List[str], List[str] | None]:
        if self.n == 2:
            return ["a"], ["b"], None
        if self.n == 3:
            return [self.variables[0]], self.variables[1:], None
        if self.n in (4, 5):
            row_vars = self.variables[:2]
            col_vars = self.variables[2:4]
            extra = [self.variables[4]] if self.n == 5 else None
            return row_vars, col_vars, extra
        raise ValueError("Карта Карно поддерживается для 2–5 переменных")

    def _karnaugh_grid(self, mode: str) -> Dict[str, object]:
        row_vars, col_vars, extra = self._karnaugh_layout()
        row_codes = self._gray_code(len(row_vars))
        col_codes = self._gray_code(len(col_vars))

        def value_for(bits: str) -> int:
            return self.vector[int(bits, 2)]

        layers = []
        if extra is None:
            layer = {
                "extra_value": None,
                "rows": [],
                "row_codes": row_codes,
                "col_codes": col_codes,
            }
            for r in row_codes:
                row = [value_for(r + c) for c in col_codes]
                layer["rows"].append((r, row))
            layers.append(layer)
        else:
            for extra_bit in ("0", "1"):
                layer = {
                    "extra_value": extra_bit,
                    "rows": [],
                    "row_codes": row_codes,
                    "col_codes": col_codes,
                }
                for r in row_codes:
                    row = [value_for(r + c + extra_bit) for c in col_codes]
                    layer["rows"].append((r, row))
                layers.append(layer)

        minimized = self.calculation_method(mode)
        return {
            "layers": layers,
            "result": minimized["result"],
        }

    def karnaugh_method(self) -> Dict[str, object]:
        return {
            "dnf": self._karnaugh_grid("DNF"),
            "knf": self._karnaugh_grid("KNF"),
        }
