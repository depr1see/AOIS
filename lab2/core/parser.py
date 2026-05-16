"""Рекурсивный спуск для логических формул."""

from __future__ import annotations

from typing import Optional

from core.ast_nodes import (
    AndNode,
    ConstantNode,
    EquivalenceNode,
    FormulaNode,
    ImplicationNode,
    NotNode,
    OrNode,
    VariableNode,
)
from core.tokenizer import FormulaSyntaxError, Token, tokenize


class FormulaParser:
    """Парсер логической формулы."""

    def __init__(self, expression: str):
        self._tokens = tokenize(expression)
        self._index = 0

    def parse(self) -> FormulaNode:
        node = self._parse_equivalence()
        if self._current() is not None:
            raise FormulaSyntaxError("Лишние токены в конце выражения")
        return node

    def _current(self) -> Optional[Token]:
        if self._index >= len(self._tokens):
            return None
        return self._tokens[self._index]

    def _consume(self, token_type: str) -> Token:
        token = self._current()
        if token is None or token.type != token_type:
            raise FormulaSyntaxError(f"Ожидался токен {token_type}")
        self._index += 1
        return token

    def _match(self, *types: str) -> bool:
        token = self._current()
        if token is not None and token.type in types:
            self._index += 1
            return True
        return False

    def _parse_equivalence(self) -> FormulaNode:
        node = self._parse_implication()
        while self._match("EQ"):
            right = self._parse_implication()
            node = EquivalenceNode(node, right)
        return node

    def _parse_implication(self) -> FormulaNode:
        node = self._parse_or()
        if self._match("IMP"):
            right = self._parse_implication()
            return ImplicationNode(node, right)
        return node

    def _parse_or(self) -> FormulaNode:
        node = self._parse_and()
        while self._match("OR"):
            right = self._parse_and()
            node = OrNode(node, right)
        return node

    def _parse_and(self) -> FormulaNode:
        node = self._parse_unary()
        while self._match("AND"):
            right = self._parse_unary()
            node = AndNode(node, right)
        return node

    def _parse_unary(self) -> FormulaNode:
        if self._match("NOT"):
            return NotNode(self._parse_unary())
        return self._parse_primary()

    def _parse_primary(self) -> FormulaNode:
        token = self._current()
        if token is None:
            raise FormulaSyntaxError("Неожиданный конец выражения")
        if token.type == "VAR":
            self._index += 1
            return VariableNode(token.value)
        if token.type == "CONST":
            self._index += 1
            return ConstantNode(token.value == "1")
        if token.type == "LPAREN":
            self._index += 1
            node = self._parse_equivalence()
            self._consume("RPAREN")
            return node
        raise FormulaSyntaxError(f"Недопустимый токен: {token.type}")
