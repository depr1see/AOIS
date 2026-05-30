"""Hash table with linear probing collision resolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.constants import DEFAULT_BASE_ADDRESS, DEFAULT_TABLE_SIZE, MIN_TABLE_SIZE
from src.hash_utils import keyword_to_value, normalize_keyword
from src.models import CellView, GeographyRecord


@dataclass(slots=True)
class _Cell:
    keyword: str | None = None
    info: str | None = None
    value: int | None = None
    home_address: int | None = None
    occupied: bool = False
    deleted: bool = False
    collision: bool = False


class HashTable:
    """Hash table for geography terms with CRUD operations."""

    def __init__(
        self,
        size: int = DEFAULT_TABLE_SIZE,
        base_address: int = DEFAULT_BASE_ADDRESS,
    ) -> None:
        if size < MIN_TABLE_SIZE:
            raise ValueError("table size must be at least 20")
        if base_address < 0:
            raise ValueError("base address must be non-negative")

        self._size = size
        self._base_address = base_address
        self._cells: list[_Cell] = [_Cell() for _ in range(size)]
        self._count = 0
        self._collisions = 0

    @property
    def size(self) -> int:
        return self._size

    @property
    def base_address(self) -> int:
        return self._base_address

    @property
    def collision_count(self) -> int:
        return self._collisions

    def __len__(self) -> int:
        return self._count

    def calculate_v(self, keyword: str) -> int:
        return keyword_to_value(keyword)

    def hash_address(self, value: int) -> int:
        return self._base_address + (value % self._size)

    def create(self, keyword: str, info: str) -> None:
        normalized = normalize_keyword(keyword)

        if self._find_index(normalized) is not None:
            raise KeyError(f'keyword "{keyword}" already exists')

        value = keyword_to_value(normalized)
        home_address = self.hash_address(value)
        index, skipped = self._find_free_slot(home_address)

        if index is None:
            raise OverflowError("hash table is full")

        self._cells[index] = _Cell(
            keyword=normalized,
            info=info,
            value=value,
            home_address=home_address,
            occupied=True,
            deleted=False,
            collision=skipped > 0,
        )
        self._count += 1
        self._collisions += skipped

    def read(self, keyword: str) -> str | None:
        index = self._find_index(normalize_keyword(keyword))
        if index is None:
            return None
        return self._cells[index].info

    def inspect(self, keyword: str) -> CellView | None:
        index = self._find_index(normalize_keyword(keyword))
        if index is None:
            return None
        return self._cell_view(index)

    def update(self, keyword: str, info: str) -> None:
        index = self._find_index(normalize_keyword(keyword))
        if index is None:
            raise KeyError(f'keyword "{keyword}" does not exist')
        self._cells[index].info = info

    def delete(self, keyword: str) -> str:
        normalized = normalize_keyword(keyword)
        index = self._find_index(normalized)
        if index is None:
            raise KeyError(f'keyword "{keyword}" does not exist')

        removed_info = self._cells[index].info or ""
        self._cells[index] = _Cell(deleted=True)
        self._count -= 1
        return removed_info

    def fill(self, records: Iterable[GeographyRecord]) -> None:
        for record in records:
            self.create(record.keyword, record.info)

    def load_factor(self) -> float:
        return round(self._count / self._size, 3)

    def dump(self) -> list[CellView]:
        return [self._cell_view(index) for index in range(self._size)]

    def stats(self) -> dict[str, float | int]:
        return {
            "count": self._count,
            "collisions": self._collisions,
            "load_factor": self.load_factor(),
        }

    def _find_index(self, normalized_keyword: str) -> int | None:
        value = keyword_to_value(normalized_keyword)
        start = self.hash_address(value) - self._base_address
        index = start

        for _ in range(self._size):
            cell = self._cells[index]

            if not cell.occupied and not cell.deleted:
                return None

            if cell.occupied and cell.keyword == normalized_keyword:
                return index

            index = (index + 1) % self._size

        return None

    def _find_free_slot(self, home_address: int) -> tuple[int | None, int]:
        start = home_address - self._base_address
        index = start
        first_deleted: int | None = None
        skipped_occupied = 0

        for _ in range(self._size):
            cell = self._cells[index]

            if not cell.occupied and not cell.deleted:
                return (first_deleted if first_deleted is not None else index, skipped_occupied)

            if cell.deleted:
                if first_deleted is None:
                    first_deleted = index
            else:
                skipped_occupied += 1

            index = (index + 1) % self._size

        if first_deleted is not None:
            return first_deleted, skipped_occupied

        return None, skipped_occupied

    def _cell_view(self, index: int) -> CellView:
        cell = self._cells[index]
        address = self._base_address + index

        if not cell.occupied and not cell.deleted:
            return CellView(
                address=address,
                keyword=None,
                info=None,
                value=None,
                home_address=None,
                collision=False,
                occupied=False,
                deleted=False,
                terminal=True,
                linked=False,
                overflow_pointer=None,
            )

        if cell.deleted:
            return CellView(
                address=address,
                keyword=None,
                info=None,
                value=None,
                home_address=None,
                collision=False,
                occupied=False,
                deleted=True,
                terminal=True,
                linked=False,
                overflow_pointer=None,
            )

        successor = self._next_occupied_index(index)

        return CellView(
            address=address,
            keyword=cell.keyword,
            info=cell.info,
            value=cell.value,
            home_address=cell.home_address,
            collision=cell.collision,
            occupied=True,
            deleted=False,
            terminal=successor is None,
            linked=successor is not None,
            overflow_pointer=self._base_address + successor if successor is not None else None,
        )

    def _next_occupied_index(self, index: int) -> int | None:
        for step in range(1, self._size):
            candidate = (index + step) % self._size
            cell = self._cells[candidate]

            if cell.occupied:
                return candidate

            if not cell.deleted:
                return None

        return None
