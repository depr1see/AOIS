"""Главный сервис анализа логических функций."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from core.derivatives import derivative_summary, fictive_variables
from core.karnaugh import KarnaughMap, build_karnaugh_map, karnaugh_to_text
from core.minimizer import MinimizationResult, minimize_cnf, minimize_dnf
from core.normal_forms import build_index_form, build_numeric_form, build_sdnf, build_sknf
from core.parser import FormulaParser
from core.post_classes import post_classes
from core.truth_table import TruthTable, build_truth_table
from core.zhegalkin import zhegalkin_polynomial


@dataclass
class AnalysisResult:
    expression: str
    parsed_expression: str
    variables: List[str]
    truth_table: TruthTable
    sdnf: str
    sknf: str
    sdnf_numeric: str
    sknf_numeric: str
    index_value: int
    index_bits: str
    post: Dict[str, bool]
    zhegalkin: str
    zhegalkin_masks: List[int]
    fictive_variables: List[str]
    derivatives: Dict[str, str]
    minimized_dnf_calculation: MinimizationResult
    minimized_cnf_calculation: MinimizationResult
    minimized_dnf_table: MinimizationResult
    minimized_cnf_table: MinimizationResult
    kmap: KarnaughMap
    kmap_text: str


class LogicFunctionAnalyzer:
    """Оркестратор анализа логической функции."""

    def analyze(self, expression: str) -> AnalysisResult:
        ast = FormulaParser(expression).parse()
        variables = sorted(ast.variables(), key=self._var_sort_key)
        truth_table = build_truth_table(ast, variables)
        sdnf, sdnf_indices = build_sdnf(truth_table)
        sknf, sknf_indices = build_sknf(truth_table)
        index_value, index_bits = build_index_form(truth_table)
        post = post_classes(truth_table)
        zhegalkin, masks = zhegalkin_polynomial(truth_table)
        fictive = fictive_variables(truth_table)
        derivatives = derivative_summary(truth_table, max_order=min(4, len(variables)))
        minimized_dnf_calculation = minimize_dnf(truth_table.values(), variables, method="calculation")
        minimized_cnf_calculation = minimize_cnf(truth_table.values(), variables, method="calculation")
        minimized_dnf_table = minimize_dnf(truth_table.values(), variables, method="calculation-table")
        minimized_cnf_table = minimize_cnf(truth_table.values(), variables, method="calculation-table")
        kmap = build_karnaugh_map(truth_table.values(), variables)
        return AnalysisResult(
            expression=expression,
            parsed_expression=ast.to_infix(),
            variables=variables,
            truth_table=truth_table,
            sdnf=sdnf,
            sknf=sknf,
            sdnf_numeric=build_numeric_form(sdnf_indices, "DNF"),
            sknf_numeric=build_numeric_form(sknf_indices, "CNF"),
            index_value=index_value,
            index_bits=index_bits,
            post=post,
            zhegalkin=zhegalkin,
            zhegalkin_masks=masks,
            fictive_variables=fictive,
            derivatives=derivatives,
            minimized_dnf_calculation=minimized_dnf_calculation,
            minimized_cnf_calculation=minimized_cnf_calculation,
            minimized_dnf_table=minimized_dnf_table,
            minimized_cnf_table=minimized_cnf_table,
            kmap=kmap,
            kmap_text=karnaugh_to_text(kmap),
        )

    @staticmethod
    def _var_sort_key(name: str) -> int:
        order = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
        return order[name]
