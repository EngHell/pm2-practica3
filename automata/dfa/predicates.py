from __future__ import annotations

from collections import Callable
from typing import Any

PredicateType = Callable[[Any], bool]


def predicate_is_number(value: str) -> bool:
    return value.isdigit()


def predicate_is_alpha(value: str) -> bool:
    return value.isalpha()


def negate(predicate) -> PredicateType:
    def negated_predicate_function(value):
        return not predicate(value)

    return negated_predicate_function


def predicate_g_union(predicate1: PredicateType, predicate2: PredicateType) -> PredicateType:
    def new_disjoint_predicate(value):
        return predicate1(value) or predicate2(value)

    return new_disjoint_predicate


def predicate_generator_is_specific_character(char: str):
    return lambda value: value == char


def predicate_g_is_dot():
    return lambda value: value == '.'
