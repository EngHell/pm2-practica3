from __future__ import annotations
from functools import reduce
from typing import Union, Callable, TypeVar, Tuple, Any, Dict
import sys

from .conditionals import cond_any
from .validator import Validator
from .monads import Functor, FunctorCallable, Monad, MonoidCallable, Right, Left, Either

T = TypeVar('T')


class State(Monad[T]):
    def chain(self, fn: MonoidCallable) -> Union[State[T], T]:
        return self
        # return fn(self.value)

    def __repr__(self):
        return 'State(' + repr(self.value) + ')'

    def map(self, fn: FunctorCallable) -> State[T]:
        # return State(fn(self.value))
        return self


def convert_validator_to_state(fn) -> Callable:
    def swap(value) -> State:
        return State(fn)

    return swap

def state_g_if_single(cond_generator, if_yes_state, if_not_state):
    def generate_if_single_state(c):
        return Validator.of(c) \
            .map(cond_generator()) \
            .chain(convert_validator_to_state(if_yes_state)) \
            .map(cond_any()) \
            .chain(convert_validator_to_state(if_not_state)) \
            .value

    return generate_if_single_state
