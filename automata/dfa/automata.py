from functools import reduce
from typing import Dict, Callable

from conditionals import cond_g_is_digit, cond, cond_g_is_dot, cond_any
from predicates import predicate_g_union, predicate_generator_is_specific_character
from state import convert_validator_to_state
from validator import Validator


def state0(c: str) -> Callable:
    a = Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state1)) \
        .map(cond(
            predicate_g_union(
                predicate_generator_is_specific_character('+'),
                predicate_generator_is_specific_character('-')
            )
        )) \
        .chain(convert_validator_to_state(state2)) \
        .map(cond_g_is_dot())\
        .chain(convert_validator_to_state(state4))\
        .map(cond_any()) \
        .chain(convert_validator_to_state(state3)) \
        .value

    return a


def state1(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state1)) \
        .map(cond_g_is_dot())\
        .chain(convert_validator_to_state(state5))\
        .map(cond_any()) \
        .chain(convert_validator_to_state(state3)) \
        .value


def state2(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit())\
        .chain(convert_validator_to_state(state1))\
        .map(cond_any())\
        .chain(convert_validator_to_state(state3))\
        .value


def state3(c) -> Callable:
    return state3


def state4(c) -> Callable:
    return Validator.of(c)\
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state5)) \
        .map(cond_any()) \
        .chain(convert_validator_to_state(state3)) \
        .value


def state5(c) -> Callable:
    return Validator.of(c) \
            .map(cond_g_is_digit()) \
            .chain(convert_validator_to_state(state5)) \
            .map(cond_any()) \
            .chain(convert_validator_to_state(state3)) \
            .value


def transition(q, c):
    return q(c)


def get_accept_test(states: Dict):
    def test(fn):
        return fn in states

    return test


def check_accepted_type(states: Dict):
    def accepted_type(fn):
        if get_accept_test(states)(fn):
            return states[fn]
        return ':::UNIDENTIFIED:::'

    return accepted_type


accepts = {
    state1: 'entero',
    state5: 'decimal'
}


def compute(word:str):
    return reduce(transition, word, state0)
