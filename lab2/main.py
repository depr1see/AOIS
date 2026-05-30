from __future__ import annotations

from lab2_boolean.algorithms.minimizer import Minimizer
from lab2_boolean.models.boolean_function import BooleanFunction
from lab2_boolean.models.post_analyzer import PostAnalyzer


def print_truth_table(func: BooleanFunction) -> None:
    print("Таблица истинности:")
    print(func.truth_table())


def print_post_analysis(func: BooleanFunction) -> None:
    analyzer = PostAnalyzer(func.vector, func.variables)
    print("\nКлассы Поста:")
    print(f"T0: {'+' if analyzer.check_t0() else '-'}")
    print(f"T1: {'+' if analyzer.check_t1() else '-'}")
    print(f"S:  {'+' if analyzer.check_s() else '-'}")
    print(f"M:  {'+' if analyzer.check_m() else '-'}")
    print(f"L:  {'+' if analyzer.check_l() else '-'}")
    print(f"Полином Жегалкина: {analyzer.zhegalkin_polynomial()}")
    essentials = analyzer.essential_variables()
    print("Фиктивные переменные:", ", ".join(v for v, ok in essentials.items() if not ok) or "нет")


def print_derivatives(func: BooleanFunction) -> None:
    analyzer = PostAnalyzer(func.vector, func.variables)
    if not func.variables:
        return
    target = func.variables[: min(4, len(func.variables))]
    result = analyzer.mixed_derivative(target)
    print("\nБулева дифференциация:")
    print(f"∂/{','.join(target)} = {PostAnalyzer.vector_to_sdnf(result.vector, result.variables)}")


def print_minimization(func: BooleanFunction) -> None:
    minimizer = Minimizer(func.vector, func.variables)
    for mode in ("DNF", "KNF"):
        calc = minimizer.calculation_method(mode)
        table = minimizer.table_method(mode)
        print(f"\nРасчетный метод ({mode}):")
        print("Этапы склеивания:")
        for stage in calc["stages"]:
            print(f"  {stage.stage_number}: {', '.join(stage.terms)}")
        print(f"Результат: {calc['result']}")
        print(f"Расчетно-табличный метод ({mode}):")
        for row in table["coverage_table"]:
            print(f"  {row['expression']}: {row['coverage']}")
        print(f"Результат: {table['result']}")

    if len(func.variables) >= 2:
        carno = minimizer.karnaugh_method()
        print("\nКарта Карно (ДНФ):")
        for layer in carno["dnf"]["layers"]:
            if layer["extra_value"] is not None:
                extra_var = func.variables[4] if len(func.variables) == 5 else ""
                print(f"Слой {extra_var} = {layer['extra_value']}")
            print("    " + "  ".join(layer["col_codes"]))
            for code, row in layer["rows"]:
                print(f"{code} | " + "  ".join(str(v) for v in row))
        print("Минимизированная ДНФ:", carno["dnf"]["result"])

        print("\nКарта Карно (КНФ):")
        for layer in carno["knf"]["layers"]:
            if layer["extra_value"] is not None:
                extra_var = func.variables[4] if len(func.variables) == 5 else ""
                print(f"Слой {extra_var} = {layer['extra_value']}")
            print("    " + "  ".join(layer["col_codes"]))
            for code, row in layer["rows"]:
                print(f"{code} | " + "  ".join(str(v) for v in row))
        print("Минимизированная КНФ:", carno["knf"]["result"])


def main() -> None:
    expression = input("Введите логическую функцию: ").strip()
    func = BooleanFunction(expression)

    print_truth_table(func)
    print("\nСДНФ:", func.sdnf())
    print("СКНФ:", func.sknf())
    print("Числовая форма СДНФ:", func.numeric_sdnf())
    print("Числовая форма СКНФ:", func.numeric_sknf())
    print("Индексная форма:", func.vector_string(), f"(dec={func.index_form()})")
    print_post_analysis(func)
    print_derivatives(func)
    print_minimization(func)


if __name__ == "__main__":
    main()
