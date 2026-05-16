from __future__ import annotations
from constants import TOTAL_BITS, DIVISION_PRECISION
from core.binary_codes import BinaryConverter
from core.arithmetic import BinaryArithmetic
from core.ieee754 import IEEE754Float
from core.bcd_5421 import BCD5421
from core.utils import BitUtils
from ui.menu import Menu


class ConsoleUI:
    @staticmethod
    def _print_bits(title: str, bits, decimal_value=None) -> None:
        print(f"{title}:")
        print(f"  2-ой формат: {BitUtils.bit_array_to_string(bits)}")
        if decimal_value is not None:
            print(f"  10-ый формат: {decimal_value}")

    @staticmethod
    def _read_int(prompt: str) -> int | None:
        try:
            return int(input(prompt))
        except ValueError:
            return None

    @staticmethod
    def _read_float(prompt: str) -> float | None:
        try:
            return float(input(prompt))
        except ValueError:
            return None

    def run(self) -> None:
        while True:
            print("\nЛабораторная работа: представление чисел")
            Menu.show()
            choice = input("Выбор: ").strip()
            if choice == "0":
                print("Выход.")
                return
            actions = {
                "1": self._conversion,
                "2": self._addition,
                "3": self._subtraction,
                "4": self._multiplication,
                "5": self._division,
                "6": self._ieee_add,
                "7": self._ieee_sub,
                "8": self._ieee_mul,
                "9": self._ieee_div,
                "10": self._bcd_add,
            }
            action = actions.get(choice)
            if action is None:
                print("Некорректный выбор.")
                continue
            try:
                action()
            except Exception as exc:
                print(f"Ошибка: {exc}")

    def _conversion(self) -> None:
        number = self._read_int("Введите целое число: ")
        if number is None:
            print("Нужно целое число.")
            return
        direct = BinaryConverter.to_direct_code(number)
        reverse = BinaryConverter.to_reverse_code(number)
        additional = BinaryConverter.to_additional_code(number)
        self._print_bits("Прямой код", direct, BinaryConverter.from_direct_code(direct))
        self._print_bits("Обратный код", reverse, BinaryConverter.from_reverse_code(reverse))
        self._print_bits("Дополнительный код", additional, BinaryConverter.from_additional_code(additional))

    def _addition(self) -> None:
        a = self._read_int("Первое число: ")
        b = self._read_int("Второе число: ")
        if a is None or b is None:
            print("Нужно два целых числа.")
            return
        res = BinaryArithmetic.add_additional(a, b)
        self._print_bits("Сумма в доп. коде", res, BinaryConverter.from_additional_code(res))

    def _subtraction(self) -> None:
        a = self._read_int("Уменьшаемое: ")
        b = self._read_int("Вычитаемое: ")
        if a is None or b is None:
            print("Нужно два целых числа.")
            return
        res = BinaryArithmetic.subtract_additional(a, b)
        self._print_bits("Разность в доп. коде", res, BinaryConverter.from_additional_code(res))

    def _multiplication(self) -> None:
        a = self._read_int("Первое число: ")
        b = self._read_int("Второе число: ")
        if a is None or b is None:
            print("Нужно два целых числа.")
            return
        res = BinaryArithmetic.multiply_direct(a, b)
        self._print_bits("Произведение в прямом коде", res, BinaryConverter.from_direct_code(res))

    def _division(self) -> None:
        a = self._read_int("Делимое: ")
        b = self._read_int("Делитель: ")
        if a is None or b is None:
            print("Нужно два целых числа.")
            return
        q, r, frac, qdec = BinaryArithmetic.divide_direct(a, b, DIVISION_PRECISION)
        self._print_bits("Частное в прямом коде", q, BinaryConverter.from_direct_code(q))
        self._print_bits("Остаток", r, BinaryConverter.from_direct_code(r))
        print(f"Дробная часть (5 бит): {''.join(frac)}")

    def _ieee_add(self) -> None:
        a = self._read_float("Первое число: ")
        b = self._read_float("Второе число: ")
        if a is None or b is None:
            print("Нужно два числа.")
            return
        bits, value = IEEE754Float.add(a, b)
        self._print_bits("IEEE-754 сумма", bits, value)

    def _ieee_sub(self) -> None:
        a = self._read_float("Первое число: ")
        b = self._read_float("Второе число: ")
        if a is None or b is None:
            print("Нужно два числа.")
            return
        bits, value = IEEE754Float.subtract(a, b)
        self._print_bits("IEEE-754 разность", bits, value)

    def _ieee_mul(self) -> None:
        a = self._read_float("Первое число: ")
        b = self._read_float("Второе число: ")
        if a is None or b is None:
            print("Нужно два числа.")
            return
        bits, value = IEEE754Float.multiply(a, b)
        self._print_bits("IEEE-754 произведение", bits, value)

    def _ieee_div(self) -> None:
        a = self._read_float("Первое число: ")
        b = self._read_float("Второе число: ")
        if a is None or b is None:
            print("Нужно два числа.")
            return
        bits, value = IEEE754Float.divide(a, b)
        self._print_bits("IEEE-754 деление", bits, value)

    def _bcd_add(self) -> None:
        a = self._read_int("Первое число: ")
        b = self._read_int("Второе число: ")
        if a is None or b is None:
            print("Нужно два целых числа.")
            return
        bits = BCD5421.add(a, b)
        self._print_bits("5421 BCD сумма", bits, BCD5421.decode(bits))
