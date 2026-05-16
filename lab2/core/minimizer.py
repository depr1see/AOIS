"""Минимизация ДНФ и КНФ расчетными и табличными методами."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

from constants import UNICODE_AND, UNICODE_NOT, UNICODE_OR


@dataclass(frozen=True)
class Implicant:
    pattern: Tuple[Optional[int], ...]
    covers: FrozenSet[int]

    def combine(self, other: "Implicant") -> Optional["Implicant"]:
        diff = 0
        new_pattern = []
        for a, b in zip(self.pattern, other.pattern):
            if a == b:
                new_pattern.append(a)
                continue
            if a is None or b is None:
                return None
            diff += 1
            new_pattern.append(None)
            if diff > 1:
                return None
        if diff != 1:
            return None
        return Implicant(tuple(new_pattern), self.covers | other.covers)

    def literal_count(self) -> int:
        return sum(1 for bit in self.pattern if bit is not None)

    def to_term(self, variables: Sequence[str], mode: str) -> str:
        if mode == "dnf":
            items = []
            for variable, bit in zip(variables, self.pattern):
                if bit is None:
                    continue
                items.append(variable if bit == 1 else f"{UNICODE_NOT}{variable}")
            return "(" + UNICODE_AND.join(items) + ")" if items else "1"
        items = []
        for variable, bit in zip(variables, self.pattern):
            if bit is None:
                continue
            items.append(variable if bit == 0 else f"{UNICODE_NOT}{variable}")
        return "(" + UNICODE_OR.join(items) + ")" if items else "0"


@dataclass
class MinimizationResult:
    method: str
    mode: str
    initial_terms: List[str]
    stages: List[List[str]]
    prime_implicants: List[str]
    selected_implicants: List[str]
    reduced_expression: str
    cover_table: List[List[str]]


def _target_indices(values: Sequence[int], mode: str) -> List[int]:
    if mode == "dnf":
        return [index for index, value in enumerate(values) if value == 1]
    return [index for index, value in enumerate(values) if value == 0]


def _pattern_from_index(index: int, n: int) -> Tuple[int, ...]:
    bits = []
    for position in range(n):
        shift = n - 1 - position
        bits.append((index >> shift) & 1)
    return tuple(bits)


def _combine_round(implicants: List[Implicant]) -> Tuple[List[Implicant], List[Implicant]]:
    used = set()
    next_round: Dict[Tuple[Optional[int], ...], Implicant] = {}
    for i, left in enumerate(implicants):
        for j in range(i + 1, len(implicants)):
            right = implicants[j]
            combined = left.combine(right)
            if combined is None:
                continue
            used.add(i)
            used.add(j)
            next_round[combined.pattern] = combined
    primes = [imp for index, imp in enumerate(implicants) if index not in used]
    return list(next_round.values()), primes


def _prime_implicants(target_indices: List[int], n: int) -> Tuple[List[List[Implicant]], List[Implicant]]:
    current = [Implicant(pattern=_pattern_from_index(index, n), covers=frozenset({index})) for index in target_indices]
    all_stages: List[List[Implicant]] = [current]
    primes: List[Implicant] = []
    while current:
        next_round, stage_primes = _combine_round(current)
        primes.extend(stage_primes)
        if not next_round:
            break
        all_stages.append(next_round)
        current = next_round
    unique_primes: Dict[Tuple[Optional[int], ...], Implicant] = {}
    for imp in primes:
        unique_primes[imp.pattern] = imp
    return all_stages, list(unique_primes.values())


def _covers(implicant: Implicant, index: int, n: int) -> bool:
    bits = _pattern_from_index(index, n)
    for pat, bit in zip(implicant.pattern, bits):
        if pat is None:
            continue
        if pat != bit:
            return False
    return True


def _cover_matrix(primes: List[Implicant], targets: List[int], n: int) -> List[List[str]]:
    matrix = []
    for prime in primes:
        row = []
        for target in targets:
            row.append("X" if _covers(prime, target, n) else "")
        matrix.append(row)
    return matrix


def _select_minimal_cover(primes: List[Implicant], targets: List[int], n: int) -> List[Implicant]:
    if not targets:
        return []
    best: Optional[List[Implicant]] = None
    target_set = set(targets)

    def better(candidate: List[Implicant], current_best: Optional[List[Implicant]]) -> bool:
        if current_best is None:
            return True
        if len(candidate) != len(current_best):
            return len(candidate) < len(current_best)
        candidate_cost = sum(imp.literal_count() for imp in candidate)
        best_cost = sum(imp.literal_count() for imp in current_best)
        if candidate_cost != best_cost:
            return candidate_cost < best_cost
        return [imp.pattern for imp in candidate] < [imp.pattern for imp in current_best]

    coverage = {index: {i for i, prime in enumerate(primes) if _covers(prime, index, n)} for index in targets}

    def backtrack(chosen: List[int], covered: Set[int]) -> None:
        nonlocal best
        if best is not None and len(chosen) > len(best):
            return
        if covered == target_set:
            candidate = [primes[i] for i in chosen]
            if better(candidate, best):
                best = candidate
            return
        remaining = [idx for idx in targets if idx not in covered]
        target = min(remaining, key=lambda idx: len(coverage[idx]))
        for prime_index in sorted(coverage[target]):
            if prime_index in chosen:
                continue
            new_covered = covered | {idx for idx in targets if _covers(primes[prime_index], idx, n)}
            backtrack(chosen + [prime_index], new_covered)

    backtrack([], set())
    return best or []


def _render_expression(implicants: List[Implicant], variables: Sequence[str], mode: str) -> str:
    if not implicants:
        return "0" if mode == "dnf" else "1"
    parts = [imp.to_term(variables, mode) for imp in implicants]
    separator = f" {UNICODE_OR} " if mode == "dnf" else f" {UNICODE_AND} "
    return separator.join(parts)


def minimize(values: Sequence[int], variables: Sequence[str], mode: str, method: str) -> MinimizationResult:
    mode = mode.lower()
    targets = _target_indices(values, mode)
    initial_implicants = [Implicant(pattern=_pattern_from_index(index, len(variables)), covers=frozenset({index})) for index in targets]
    stages_data, primes = _prime_implicants(targets, len(variables))
    selected = _select_minimal_cover(primes, targets, len(variables))
    cover_table = _cover_matrix(primes, targets, len(variables))
    stage_strings = [[imp.to_term(variables, mode) for imp in stage] for stage in stages_data]
    return MinimizationResult(
        method=method,
        mode=mode,
        initial_terms=[imp.to_term(variables, mode) for imp in initial_implicants],
        stages=stage_strings,
        prime_implicants=[imp.to_term(variables, mode) for imp in primes],
        selected_implicants=[imp.to_term(variables, mode) for imp in selected],
        reduced_expression=_render_expression(selected, variables, mode),
        cover_table=cover_table,
    )


def minimize_dnf(values: Sequence[int], variables: Sequence[str], method: str = "calculation") -> MinimizationResult:
    return minimize(values, variables, "dnf", method)


def minimize_cnf(values: Sequence[int], variables: Sequence[str], method: str = "calculation") -> MinimizationResult:
    return minimize(values, variables, "cnf", method)
