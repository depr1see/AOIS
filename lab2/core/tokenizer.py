"""Токенизация логических формул."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from constants import (
    ASCII_AND,
    ASCII_EQ,
    ASCII_IMP,
    ASCII_NOT,
    ASCII_OR,
    UNICODE_AND,
    UNICODE_EQ,
    UNICODE_IMP,
    UNICODE_NOT,
    UNICODE_OR,
)


class FormulaSyntaxError(ValueError):
    """Ошибка синтаксиса формулы."""


@dataclass(frozen=True)
class Token:
    type: str
    value: str


_NORMALIZATION_MAP = {
    UNICODE_NOT: ASCII_NOT,
    UNICODE_AND: ASCII_AND,
    UNICODE_OR: ASCII_OR,
    UNICODE_IMP: ASCII_IMP,
    UNICODE_EQ: ASCII_EQ,
    "⋀": ASCII_AND,
    "⋁": ASCII_OR,
    "⇒": ASCII_IMP,
    "≡": ASCII_EQ,
}


def normalize_formula(expression: str) -> str:
    """Приводит формулу к ASCII-виду."""
    result = expression
    for source, target in _NORMALIZATION_MAP.items():
        result = result.replace(source, target)
    return result.replace(" ", "")


def tokenize(expression: str) -> List[Token]:
    """Разбивает строку на токены."""
    normalized = normalize_formula(expression)
    tokens: List[Token] = []
    i = 0
    while i < len(normalized):
        ch = normalized[i]
        if ch.isalpha():
            if ch not in "abcde":
                raise FormulaSyntaxError(f"Недопустимая переменная: {ch}")
            tokens.append(Token("VAR", ch))
            i += 1
            continue
        if ch == "0" or ch == "1":
            tokens.append(Token("CONST", ch))
            i += 1
            continue
        if ch == ASCII_NOT:
            tokens.append(Token("NOT", ch))
            i += 1
            continue
        if ch == ASCII_AND:
            tokens.append(Token("AND", ch))
            i += 1
            continue
        if ch == ASCII_OR:
            tokens.append(Token("OR", ch))
            i += 1
            continue
        if ch == "(":
            tokens.append(Token("LPAREN", ch))
            i += 1
            continue
        if ch == ")":
            tokens.append(Token("RPAREN", ch))
            i += 1
            continue
        if ch == "-" and i + 1 < len(normalized) and normalized[i + 1] == ">":
            tokens.append(Token("IMP", ASCII_IMP))
            i += 2
            continue
        if ch == ASCII_EQ:
            tokens.append(Token("EQ", ch))
            i += 1
            continue
        raise FormulaSyntaxError(f"Недопустимый символ: {ch}")
    return tokens
