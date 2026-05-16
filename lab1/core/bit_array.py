from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List

from constants import TOTAL_BITS


def _normalize_bit(bit: str | int) -> str:
    if bit in (0, "0"):
        return "0"
    if bit in (1, "1"):
        return "1"
    raise ValueError("Bit must be 0/1")


@dataclass
class BitArray:
    bits: List[str]

    def __init__(self, size: int = TOTAL_BITS, bits: Iterable[str | int] | None = None):
        if bits is None:
            self.bits = ["0"] * size
        else:
            normalized = [_normalize_bit(b) for b in bits]
            self.bits = normalized[:] if len(normalized) == size else normalized

    @classmethod
    def zeros(cls, size: int = TOTAL_BITS) -> "BitArray":
        return cls(size=size)

    @classmethod
    def from_string(cls, value: str) -> "BitArray":
        return cls(bits=list(value))

    def copy(self) -> "BitArray":
        return BitArray(bits=self.bits[:])

    def to_string(self) -> str:
        return "".join(self.bits)

    def __len__(self) -> int:
        return len(self.bits)

    def __getitem__(self, index):
        return self.bits[index]

    def __setitem__(self, index, value):
        self.bits[index] = _normalize_bit(value)

    def __iter__(self):
        return iter(self.bits)

    def slice(self, start: int, end: int) -> "BitArray":
        return BitArray(bits=self.bits[start:end])

    def extend_left(self, count: int) -> "BitArray":
        return BitArray(bits=(["0"] * count) + self.bits)
