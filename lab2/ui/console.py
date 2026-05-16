"""Консольный интерфейс."""

from __future__ import annotations

from core.analyzer import LogicFunctionAnalyzer


class ConsoleApp:
    def __init__(self):
        self.analyzer = LogicFunctionAnalyzer()

    def run(self) -> None:
        print("Лабораторная работа 2")
        print("Построение СКНФ и СДНФ на основании таблиц истинности")
        expression = input("Введите логическую функцию: ").strip()
        result = self.analyzer.analyze(expression)
        self._print_result(result)

    def _print_result(self, result) -> None:
        print("\nИсходная формула:")
        print(result.expression)
        print("\nНормализованная запись:")
        print(result.parsed_expression)
        print("\nПеременные:")
        print(", ".join(result.variables))
        print("\nТаблица истинности:")
        for row in result.truth_table.rows:
            print(row.assignment, "->", row.value)
        print("\nСДНФ:")
        print(result.sdnf)
        print("Числовая форма СДНФ:", result.sdnf_numeric)
        print("\nСКНФ:")
        print(result.sknf)
        print("Числовая форма СКНФ:", result.sknf_numeric)
        print("\nИндексная форма:")
        print(result.index_bits, "=", result.index_value)
        print("\nКлассы Поста:")
        for key, value in result.post.items():
            print(f"{key}: {'да' if value else 'нет'}")
        print("\nПолином Жегалкина:")
        print(result.zhegalkin)
        print("\nФиктивные переменные:")
        print(", ".join(result.fictive_variables) if result.fictive_variables else "нет")
        print("\nБулевы производные:")
        for name, value in result.derivatives.items():
            print(f"d/d{name}: {value}")
        print("\nМинимизация расчетным методом (ДНФ):")
        print(result.minimized_dnf_calculation.reduced_expression)
        print("\nМинимизация расчетным методом (КНФ):")
        print(result.minimized_cnf_calculation.reduced_expression)
        print("\nМинимизация расчетно-табличным методом (ДНФ):")
        print(result.minimized_dnf_table.reduced_expression)
        print("\nМинимизация расчетно-табличным методом (КНФ):")
        print(result.minimized_cnf_table.reduced_expression)
        print("\nКарта Карно:")
        print(result.kmap_text)
