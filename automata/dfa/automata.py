from functools import reduce
from typing import Dict, Callable

from .conditionals import cond_g_is_digit, cond, cond_g_is_dot, cond_any, cond_g_is_alpha, cond_g_is_plus_or_minus, \
    cond_g_is_exp_mantisa, cond_g_is_date_separator, cond_g_is_i
from .predicates import predicate_g_union, predicate_generator_is_specific_character
from .state import convert_validator_to_state, state_g_if_single
from .validator import Validator


def state0(c: str) -> Callable:
    a = Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state2)) \
        .map(cond_g_is_plus_or_minus()) \
        .chain(convert_validator_to_state(state1)) \
        .map(cond_g_is_dot()) \
        .chain(convert_validator_to_state(state18)) \
        .map(cond_g_is_alpha()) \
        .chain(convert_validator_to_state(state11)) \
        .map(cond_any()) \
        .chain(convert_validator_to_state(state20)) \
        .value

    return a


def state1(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state3_1)) \
        .map(cond_g_is_dot()) \
        .chain(convert_validator_to_state(state18)) \
        .map(cond_any()) \
        .chain(convert_validator_to_state(state21)) \
        .value


def state2(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state3)) \
        .map(cond_g_is_dot()) \
        .chain(convert_validator_to_state(state4)) \
        .map(cond_g_is_exp_mantisa()) \
        .chain(convert_validator_to_state(state5)) \
        .map(cond_g_is_plus_or_minus())\
        .chain(convert_validator_to_state(state8))\
        .map(cond_any()) \
        .chain(convert_validator_to_state(state3)) \
        .value


def state3(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state3_1)) \
        .map(cond_g_is_dot()) \
        .chain(convert_validator_to_state(state4)) \
        .map(cond_g_is_exp_mantisa()) \
        .chain(convert_validator_to_state(state5)) \
        .map(cond_g_is_date_separator()) \
        .chain(convert_validator_to_state(state12)) \
        .map(cond_g_is_plus_or_minus())\
        .chain(convert_validator_to_state(state8))\
        .map(cond_any()) \
        .chain(convert_validator_to_state(state22)) \
        .value


def state3_1(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_exp_mantisa()) \
        .chain(convert_validator_to_state(state5)) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state3_1)) \
        .map(cond_g_is_dot()) \
        .chain(convert_validator_to_state(state4)) \
        .map(cond_g_is_plus_or_minus())\
        .chain(convert_validator_to_state(state8))\
        .map(cond_any()) \
        .chain(convert_validator_to_state(state22)) \
        .value


def state4(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state4)) \
        .map(cond_g_is_exp_mantisa()) \
        .chain(convert_validator_to_state(state5)) \
        .map(cond_g_is_plus_or_minus()) \
        .chain(convert_validator_to_state(state8)) \
        .map(cond_any()) \
        .chain(convert_validator_to_state(state21)) \
        .value


def state5(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state7)) \
        .map(cond_g_is_plus_or_minus()) \
        .chain(convert_validator_to_state(state6)) \
        .map(cond_any()) \
        .chain(convert_validator_to_state(state29)) \
        .value


def state6(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state7)) \
        .map(cond_any()) \
        .chain(state29) \
        .value


def state7(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state7)) \
        .map(cond_any()) \
        .chain(state29) \
        .value


def state8(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state14)) \
        .map(cond_g_is_dot()) \
        .chain(convert_validator_to_state(state16)) \
        .map(cond_g_is_i()) \
        .chain(convert_validator_to_state(state17)) \
        .map(cond_any()) \
        .chain(state31) \
        .value


def state9(c) -> Callable:
    return state_g_if_single(cond_g_is_digit, state27, state28)(c)


def state10(c) -> Callable:
    return state28


def state11(c) -> Callable:
    return state_g_if_single(cond_g_is_alpha, state11, state20)(c)


def state12(c) -> Callable:
    return state_g_if_single(cond_g_is_digit, state13, state28)(c)


def state13(c) -> Callable:
    return state_g_if_single(cond_g_is_digit, state24, state28)(c)


def state14(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state14)) \
        .map(cond_g_is_dot()) \
        .chain(convert_validator_to_state(state15)) \
        .map(cond_g_is_i())\
        .chain(convert_validator_to_state(state17)) \
        .map(cond_any()) \
        .chain(convert_validator_to_state(state30)) \
        .value


def state15(c) -> Callable:
    return Validator.of(c) \
        .map(cond_g_is_digit()) \
        .chain(convert_validator_to_state(state15)) \
        .map(cond(
            predicate_generator_is_specific_character('i')
        )) \
        .chain(convert_validator_to_state(state17)) \
        .map(cond_any()) \
        .chain(convert_validator_to_state(state30))\
        .value


def state16(c) -> Callable:
    return state_g_if_single(cond_g_is_digit, state15, state31)(c)


def state17(c)-> Callable:
    return state30


def state18(c) -> Callable:
    return state_g_if_single(cond_g_is_digit, state4, state21)(c)


def state20(c) -> Callable:
    return state20


def state21(c) -> Callable:
    return state21


def state22(c) -> Callable:
    return state22


def state24(c) -> Callable:
    return state_g_if_single(cond_g_is_date_separator, state25, state28)(c)


def state25(c):
    return state_g_if_single(cond_g_is_digit, state26, state28)(c)


def state26(c):
    return state_g_if_single(cond_g_is_digit, state9, state28)(c)


def state27(c):
    return state_g_if_single(cond_g_is_digit, state10, state28)(c)


def state28(c):
    return state28


def state29(c) -> Callable:
    return state29


def state30(c):
    return state30


def state31(c):
    return state31


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
    state2: 'entero',
    state3: 'entero',
    state3_1: 'entero',
    state4: 'decimal',
    state7: 'cientifica',
    state9: 'fecha',
    state10: 'fecha',
    state11: 'palabra',
    state17: 'complejo'
}


def compute(word: str):
    return reduce(transition, word, state0)
