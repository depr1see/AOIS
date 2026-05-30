"""Tests for the CLI."""

from __future__ import annotations

import unittest

from src.cli import run_cli
from src.hash_table import HashTable


class _FakeIO:
    def __init__(self, inputs: list[str]) -> None:
        self._inputs = iter(inputs)
        self.outputs: list[str] = []

    def input(self, prompt: str) -> str:
        self.outputs.append(prompt)
        return next(self._inputs)

    def output(self, message: str) -> None:
        self.outputs.append(str(message))


class CliTestCase(unittest.TestCase):
    def test_full_crud_flow(self) -> None:
        table = HashTable(size=20)
        io = _FakeIO(
            [
                "1", "Азия", "Материк Евразии",
                "2", "Азия",
                "3", "Азия", "Самый большой материк Земли",
                "2", "Азия",
                "4", "Азия",
                "2", "Азия",
                "6",
                "0",
            ]
        )

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Запись добавлена.", log)
        self.assertIn("Запись обновлена.", log)
        self.assertIn("Удалено:", log)
        self.assertIn("Ключ не найден.", log)
        self.assertIn("Количество записей:", log)
        self.assertIn("Выход из программы.", log)

    def test_fill_demo_data_and_show_table(self) -> None:
        table = HashTable(size=20)
        io = _FakeIO(["7", "5", "0"])

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Таблица заполнена демонстрационными данными.", log)
        self.assertIn("Содержимое таблицы:", log)

    def test_unknown_choice(self) -> None:
        table = HashTable(size=20)
        io = _FakeIO(["9", "0"])

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Неизвестный пункт меню.", log)

    def test_empty_fields_are_rejected(self) -> None:
        table = HashTable(size=20)
        io = _FakeIO(["1", "", "Азия", "", "Материк", "0"])

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Ошибка: поле не должно быть пустым.", log)


if __name__ == "__main__":
    unittest.main()
