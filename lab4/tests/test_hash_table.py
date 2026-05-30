"""Tests for the hash table."""

from __future__ import annotations

import unittest

from src.geography_data import demo_records
from src.hash_table import HashTable
from src.hash_utils import keyword_to_value, normalize_keyword


class HashTableTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.table = HashTable(size=20)

    def test_normalize_keyword(self) -> None:
        self.assertEqual(normalize_keyword("  Берингово море  "), "БЕРИНГОВОМОРЕ")

    def test_keyword_to_value_uses_first_two_letters(self) -> None:
        self.assertEqual(keyword_to_value("Байкал"), 33)

    def test_hash_address_with_base(self) -> None:
        table = HashTable(size=20, base_address=7)
        self.assertEqual(table.hash_address(42), 7 + (42 % 20))

    def test_create_and_read(self) -> None:
        self.table.create("Байкал", "Крупнейшее пресноводное озеро.")
        self.assertEqual(self.table.read("Байкал"), "Крупнейшее пресноводное озеро.")

    def test_inspect_returns_full_view(self) -> None:
        self.table.create("Волга", "Крупнейшая река Европы.")
        view = self.table.inspect("Волга")
        self.assertIsNotNone(view)
        self.assertTrue(view.occupied)
        self.assertEqual(view.keyword, "ВОЛГА")
        self.assertEqual(view.value, keyword_to_value("Волга"))

    def test_missing_read_returns_none(self) -> None:
        self.assertIsNone(self.table.read("Гоби"))

    def test_duplicate_insert_raises(self) -> None:
        self.table.create("Азия", "Материк.")
        with self.assertRaises(KeyError):
            self.table.create("Азия", "Дубликат.")

    def test_update_existing(self) -> None:
        self.table.create("Африка", "Материк.")
        self.table.update("Африка", "Второй по площади материк.")
        self.assertEqual(self.table.read("Африка"), "Второй по площади материк.")

    def test_update_missing_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.table.update("Гималаи", "Горная система.")

    def test_delete_existing(self) -> None:
        self.table.create("Гоби", "Пустыня.")
        removed = self.table.delete("Гоби")
        self.assertEqual(removed, "Пустыня.")
        self.assertIsNone(self.table.read("Гоби"))

    def test_delete_missing_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.table.delete("Гоби")

    def test_collision_chain_linear_probing(self) -> None:
        self.table.create("Байкал", "Озеро")
        self.table.create("Балтика", "Море")
        self.table.create("Бархан", "Форма рельефа")
        self.table.create("Бассейн", "Территория стока")

        self.assertGreaterEqual(self.table.collision_count, 3)
        self.assertEqual(self.table.read("Байкал"), "Озеро")
        self.assertEqual(self.table.read("Балтика"), "Море")
        self.assertEqual(self.table.read("Бархан"), "Форма рельефа")
        self.assertEqual(self.table.read("Бассейн"), "Территория стока")

    def test_deleted_slot_keeps_search_chain(self) -> None:
        self.table.create("Байкал", "Озеро")
        self.table.create("Балтика", "Море")
        self.table.delete("Байкал")
        self.assertEqual(self.table.read("Балтика"), "Море")

    def test_load_factor(self) -> None:
        self.table.create("Азия", "Материк")
        self.assertAlmostEqual(self.table.load_factor(), 0.05, places=2)

    def test_dump_contains_empty_deleted_and_occupied(self) -> None:
        self.table.create("Азия", "Материк")
        self.table.delete("Азия")
        dump = self.table.dump()

        self.assertEqual(len(dump), 20)
        self.assertTrue(any(cell.deleted for cell in dump))
        self.assertTrue(any(not cell.occupied and not cell.deleted for cell in dump))

    def test_invalid_table_size_raises(self) -> None:
        with self.assertRaises(ValueError):
            HashTable(size=10)

    def test_invalid_keyword_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.table.create("А", "bad")

    def test_non_string_keyword_raises(self) -> None:
        with self.assertRaises(TypeError):
            self.table.create(123, "bad")  # type: ignore[arg-type]

    def test_stats(self) -> None:
        self.table.create("Азия", "Материк")
        stats = self.table.stats()
        self.assertEqual(stats["count"], 1)
        self.assertIn("collisions", stats)
        self.assertIn("load_factor", stats)

    def test_fill_from_records(self) -> None:
        self.table.fill(demo_records())
        self.assertGreaterEqual(len(self.table), 10)
        self.assertIsNotNone(self.table.read("Байкал"))


if __name__ == "__main__":
    unittest.main()
