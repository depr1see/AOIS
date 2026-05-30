"""Console interface for the geography hash table."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.geography_data import demo_records
from src.hash_table import HashTable


InputFn = Callable[[str], str]
OutputFn = Callable[[str], Any]


def _menu(output_fn: OutputFn) -> None:
    output_fn("")
    output_fn("1 - Добавить запись")
    output_fn("2 - Найти запись")
    output_fn("3 - Обновить запись")
    output_fn("4 - Удалить запись")
    output_fn("5 - Показать таблицу")
    output_fn("6 - Показать статистику")
    output_fn("7 - Заполнить примерами")
    output_fn("0 - Выход")


def _format_cell(row) -> str:
    if not row.occupied and not row.deleted:
        return f"[{row.address}] EMPTY"

    if row.deleted:
        return f"[{row.address}] DELETED"

    return (
        f"[{row.address}] "
        f"ID={row.keyword} | "
        f"V={row.value} | "
        f"h={row.home_address} | "
        f"C={int(row.collision)} U={int(row.occupied)} T={int(row.terminal)} "
        f"L={int(row.linked)} D={int(row.deleted)} | "
        f"Po={row.overflow_pointer} | "
        f"Pi={row.info}"
    )


def _ask_non_empty(prompt: str, input_fn: InputFn, output_fn: OutputFn) -> str:
    while True:
        raw = input_fn(prompt).strip()
        if raw:
            return raw
        output_fn("Ошибка: поле не должно быть пустым.")


def run_cli(
    table: HashTable | None = None,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    if table is None:
        table = HashTable()

    output_fn("Хеш-таблица по теме «География»")
    output_fn("Вариант: линейное разрешение коллизий (линейный probing).")

    while True:
        _menu(output_fn)
        choice = input_fn("Выберите пункт: ").strip()

        if choice == "1":
            keyword = _ask_non_empty("Ключевое слово: ", input_fn, output_fn)
            info = _ask_non_empty("Описание: ", input_fn, output_fn)
            try:
                table.create(keyword, info)
                output_fn("Запись добавлена.")
            except (KeyError, ValueError, OverflowError) as error:
                output_fn(f"Ошибка: {error}")

        elif choice == "2":
            keyword = _ask_non_empty("Ключевое слово: ", input_fn, output_fn)
            record = table.inspect(keyword)
            if record is None:
                output_fn("Ключ не найден.")
            else:
                output_fn(_format_cell(record))

        elif choice == "3":
            keyword = _ask_non_empty("Ключевое слово: ", input_fn, output_fn)
            info = _ask_non_empty("Новое описание: ", input_fn, output_fn)
            try:
                table.update(keyword, info)
                output_fn("Запись обновлена.")
            except (KeyError, ValueError) as error:
                output_fn(f"Ошибка: {error}")

        elif choice == "4":
            keyword = _ask_non_empty("Ключевое слово: ", input_fn, output_fn)
            try:
                removed = table.delete(keyword)
                output_fn(f"Удалено: {removed}")
            except (KeyError, ValueError) as error:
                output_fn(f"Ошибка: {error}")

        elif choice == "5":
            output_fn("Содержимое таблицы:")
            for row in table.dump():
                output_fn(_format_cell(row))

        elif choice == "6":
            stats = table.stats()
            output_fn(f"Количество записей: {stats['count']}")
            output_fn(f"Количество коллизий: {stats['collisions']}")
            output_fn(f"Коэффициент заполнения: {stats['load_factor']}")

        elif choice == "7":
            try:
                table.fill(demo_records())
                output_fn("Таблица заполнена демонстрационными данными.")
            except (KeyError, OverflowError, ValueError) as error:
                output_fn(f"Ошибка: {error}")

        elif choice == "0":
            output_fn("Выход из программы.")
            break

        else:
            output_fn("Неизвестный пункт меню.")


def main() -> None:
    run_cli()


if __name__ == "__main__":  # pragma: no cover
    main()
