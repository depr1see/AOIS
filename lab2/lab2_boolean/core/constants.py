from __future__ import annotations

VALID_VARIABLES = ('a', 'b', 'c', 'd', 'e')

# Higher number means higher priority.
PRECEDENCE = {
    '!': 5,
    '&': 4,
    '|': 3,
    '->': 2,
    '~': 1,
}

# Unary operator is right associative by convention.
ASSOCIATIVITY = {
    '!': 'right',
    '&': 'left',
    '|': 'left',
    '->': 'right',
    '~': 'left',
}

OPERATORS = set(PRECEDENCE)
UNARY_OPERATORS = {'!'}
BINARY_OPERATORS = {'&', '|', '->', '~'}
