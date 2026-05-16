"""Узлы абстрактного синтаксического дерева."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set


class FormulaNode:
    """Базовый узел формулы."""

    def evaluate(self, values: Dict[str, bool]) -> bool:
        raise NotImplementedError

    def variables(self) -> Set[str]:
        raise NotImplementedError

    def to_infix(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class ConstantNode(FormulaNode):
    value: bool

    def evaluate(self, values: Dict[str, bool]) -> bool:
        return self.value

    def variables(self) -> Set[str]:
        return set()

    def to_infix(self) -> str:
        return "1" if self.value else "0"


@dataclass(frozen=True)
class VariableNode(FormulaNode):
    name: str

    def evaluate(self, values: Dict[str, bool]) -> bool:
        return bool(values[self.name])

    def variables(self) -> Set[str]:
        return {self.name}

    def to_infix(self) -> str:
        return self.name


@dataclass(frozen=True)
class NotNode(FormulaNode):
    child: FormulaNode

    def evaluate(self, values: Dict[str, bool]) -> bool:
        return not self.child.evaluate(values)

    def variables(self) -> Set[str]:
        return self.child.variables()

    def to_infix(self) -> str:
        inner = self.child.to_infix()
        if isinstance(self.child, (VariableNode, ConstantNode, NotNode)):
            return f"!{inner}"
        return f"!({inner})"


@dataclass(frozen=True)
class BinaryNode(FormulaNode):
    left: FormulaNode
    right: FormulaNode
    operator: str = "?"
    priority: int = 0

    def variables(self) -> Set[str]:
        return self.left.variables() | self.right.variables()

    def _wrap_left(self, node: FormulaNode) -> str:
        if isinstance(node, (VariableNode, ConstantNode, NotNode)):
            return node.to_infix()
        if getattr(node, "priority", 0) < self.priority:
            return f"({node.to_infix()})"
        return node.to_infix()

    def _wrap_right(self, node: FormulaNode) -> str:
        if isinstance(node, (VariableNode, ConstantNode, NotNode)):
            return node.to_infix()
        if getattr(node, "priority", 0) <= self.priority:
            return f"({node.to_infix()})"
        return node.to_infix()

    def to_infix(self) -> str:
        return f"{self._wrap_left(self.left)}{self.operator}{self._wrap_right(self.right)}"


@dataclass(frozen=True)
class AndNode(BinaryNode):
    operator: str = "&"
    priority: int = 4

    def evaluate(self, values: Dict[str, bool]) -> bool:
        return self.left.evaluate(values) and self.right.evaluate(values)


@dataclass(frozen=True)
class OrNode(BinaryNode):
    operator: str = "|"
    priority: int = 3

    def evaluate(self, values: Dict[str, bool]) -> bool:
        return self.left.evaluate(values) or self.right.evaluate(values)


@dataclass(frozen=True)
class ImplicationNode(BinaryNode):
    operator: str = "->"
    priority: int = 2

    def evaluate(self, values: Dict[str, bool]) -> bool:
        return (not self.left.evaluate(values)) or self.right.evaluate(values)


@dataclass(frozen=True)
class EquivalenceNode(BinaryNode):
    operator: str = "~"
    priority: int = 1

    def evaluate(self, values: Dict[str, bool]) -> bool:
        return self.left.evaluate(values) == self.right.evaluate(values)
