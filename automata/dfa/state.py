from __future__ import annotations
from functools import reduce
from typing import Union, Callable, TypeVar, Tuple, Any, Dict
import sys

from monads import Functor, FunctorCallable, Monad, MonoidCallable, Right, Left, Either

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
