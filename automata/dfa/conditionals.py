from typing import Tuple, Any

from .predicates import PredicateType, predicate_g_is_dot, predicate_generator_is_specific_character, \
    predicate_is_number, predicate_is_alpha, predicate_g_union


def cond(predicate: PredicateType) -> Tuple[Any, bool]:
    def guess(value):
        should = predicate(value) if hasattr(predicate, '__call__') else predicate
        if should:
            return value, True
        return value, False

    return guess


def cond_g_is_dot():
    return cond(predicate_g_is_dot())


def cond_g_is_i():
    return cond(predicate_generator_is_specific_character('i'))


def cond_is_specific_character(char: str):
    return cond(predicate_generator_is_specific_character(char))


def cond_g_is_digit():
    return cond(predicate_is_number)


def cond_g_is_alpha():
    return cond(predicate_is_alpha)


def cond_g_is_plus_or_minus():
    return cond(
        predicate_g_union(
            predicate_generator_is_specific_character('+'),
            predicate_generator_is_specific_character('-')
        )
    )


def cond_g_is_date_separator():
    return cond(
        predicate_g_union(
            predicate_generator_is_specific_character('/'),
            predicate_generator_is_specific_character('-')
        )
    )


def cond_g_is_exp_mantisa():
    return cond(
        predicate_g_union(
            predicate_generator_is_specific_character('e'),
            predicate_generator_is_specific_character('E')
        )
    )


def cond_any():
    return cond(lambda value: True)
