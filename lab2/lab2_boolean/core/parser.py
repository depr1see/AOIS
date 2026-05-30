from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .constants import ASSOCIATIVITY, OPERATORS, PRECEDENCE, VALID_VARIABLES


class ExpressionError(ValueError):
    """Raised when an expression cannot be parsed or evaluated."""


@dataclass(frozen=True)
class TokenStream:
    tokens: List[str]


class ExpressionParser:
    """Parses and evaluates boolean expressions without using eval."""

    _NORMALIZATION = {
        "¬": "!",
        "∧": "&",
        "∨": "|",
        "→": "->",
        "↔": "~",
    }

    def __init__(self, raw_expression: str):
        self.raw_expression = self._normalize(raw_expression)
        self.tokens = self._tokenize(self.raw_expression)
        self.postfix = self._to_postfix(self.tokens)

    @classmethod
    def _normalize(cls, expr: str) -> str:
        text = expr.replace(" ", "")
        for old, new in cls._NORMALIZATION.items():
            text = text.replace(old, new)
        return text

    def _tokenize(self, expr: str) -> List[str]:
        tokens: List[str] = []
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch in VALID_VARIABLES or ch in "()":
                tokens.append(ch)
                i += 1
                continue
            if ch == "-" and i + 1 < len(expr) and expr[i + 1] == ">":
                tokens.append("->")
                i += 2
                continue
            if ch in OPERATORS:
                tokens.append(ch)
                i += 1
                continue
            raise ExpressionError(f"Недопустимый символ: {ch!r}")
        if not tokens:
            raise ExpressionError("Пустое выражение")
        return tokens

    def _to_postfix(self, tokens: List[str]) -> List[str]:
        output: List[str] = []
        stack: List[str] = []
        prev_kind = "start"

        for token in tokens:
            if token in VALID_VARIABLES:
                if prev_kind in {"operand", "close"}:
                    raise ExpressionError("Отсутствует оператор между операндами")
                output.append(token)
                prev_kind = "operand"
                continue

            if token == "(":
                if prev_kind in {"operand", "close"}:
                    raise ExpressionError("Отсутствует оператор перед '('")
                stack.append(token)
                prev_kind = "open"
                continue

            if token == ")":
                if prev_kind in {"start", "operator", "open"}:
                    raise ExpressionError("Пустые скобки или неверная позиция ')'")
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                if not stack:
                    raise ExpressionError("Несогласованные скобки")
                stack.pop()
                prev_kind = "close"
                continue

            if token in OPERATORS:
                if token == "!":
                    if prev_kind in {"operand", "close"}:
                        raise ExpressionError("Логическое НЕ должно стоять перед операндом")
                    while stack and stack[-1] != "(" and (
                        PRECEDENCE[stack[-1]] > PRECEDENCE[token]
                        or (PRECEDENCE[stack[-1]] == PRECEDENCE[token]
                            and ASSOCIATIVITY.get(token) == "left")
                    ):
                        output.append(stack.pop())
                    stack.append(token)
                    prev_kind = "operator"
                    continue

                if prev_kind not in {"operand", "close"}:
                    raise ExpressionError(f"Бинарный оператор {token!r} стоит не на месте")
                while stack and stack[-1] != "(" and (
                    PRECEDENCE[stack[-1]] > PRECEDENCE[token]
                    or (PRECEDENCE[stack[-1]] == PRECEDENCE[token]
                        and ASSOCIATIVITY.get(token) == "left")
                ):
                    output.append(stack.pop())
                stack.append(token)
                prev_kind = "operator"
                continue

            raise ExpressionError(f"Неизвестный токен: {token!r}")

        if prev_kind in {"start", "operator", "open"}:
            raise ExpressionError("Выражение завершено некорректно")

        while stack:
            op = stack.pop()
            if op == "(":
                raise ExpressionError("Несогласованные скобки")
            output.append(op)
        return output

    @staticmethod
    def _coerce_bool(value: int | bool) -> bool:
        return bool(value)

    def evaluate(self, var_values: Dict[str, int | bool]) -> int:
        stack: List[bool] = []
        for token in self.postfix:
            if token in VALID_VARIABLES:
                if token not in var_values:
                    raise ExpressionError(f"Не задано значение переменной {token!r}")
                stack.append(self._coerce_bool(var_values[token]))
            elif token == "!":
                if not stack:
                    raise ExpressionError("Недостаточно операндов для '!'")
                stack.append(not stack.pop())
            else:
                if len(stack) < 2:
                    raise ExpressionError(f"Недостаточно операндов для {token!r}")
                right = stack.pop()
                left = stack.pop()
                if token == "&":
                    stack.append(left and right)
                elif token == "|":
                    stack.append(left or right)
                elif token == "->":
                    stack.append((not left) or right)
                elif token == "~":
                    stack.append(left == right)
                else:
                    raise ExpressionError(f"Неизвестный оператор {token!r}")

        if len(stack) != 1:
            raise ExpressionError("Некорректное выражение")
        return int(stack[0])

    def variables(self) -> List[str]:
        seen = []
        for token in self.tokens:
            if token in VALID_VARIABLES and token not in seen:
                seen.append(token)
        return sorted(seen, key=VALID_VARIABLES.index)
