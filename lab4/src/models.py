"""Data models used by the hash table."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GeographyRecord:
    """A thematic record for the geography table."""

    keyword: str
    info: str


@dataclass(slots=True)
class CellView:
    """Readonly view of one table cell."""

    address: int
    keyword: str | None
    info: str | None
    value: int | None
    home_address: int | None
    collision: bool
    occupied: bool
    deleted: bool
    terminal: bool
    linked: bool
    overflow_pointer: int | None
