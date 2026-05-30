"""Helpers for keyword normalization and hashing."""

from __future__ import annotations

from src.constants import ALPHABET_BASE, RUSSIAN_ALPHABET


def normalize_keyword(raw_keyword: str) -> str:
    """Keep only letters and convert to uppercase."""
    if not isinstance(raw_keyword, str):
        raise TypeError("keyword must be a string")

    letters = [ch.upper() for ch in raw_keyword.strip() if ch.isalpha()]
    normalized = "".join(letters)

    if len(normalized) < 2:
        raise ValueError("keyword must contain at least two letters")

    return normalized


def keyword_to_value(raw_keyword: str) -> int:
    """Convert the first two letters of a keyword into V."""
    normalized = normalize_keyword(raw_keyword)

    try:
        first = RUSSIAN_ALPHABET[normalized[0]]
        second = RUSSIAN_ALPHABET[normalized[1]]
    except KeyError as error:
        raise ValueError(f"unsupported letter: {error.args[0]}") from None

    return first * ALPHABET_BASE + second
