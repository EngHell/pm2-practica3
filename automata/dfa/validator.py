from __future__ import annotations
from typing import TypeVar, Tuple, Callable, Union
from monads import Monad

T = TypeVar('T')
P = TypeVar('P')

ValidatorPayload = Tuple[T, bool]


class Validator(Monad[ValidatorPayload]):
    def __init__(self, value: ValidatorPayload):
        val, valid = value
        self.valid = valid
        super().__init__(val)

    @staticmethod
    def of(value: T):
        return Validator((value, False))

    def __repr__(self):
        return 'Validator(' + repr((self.value, self.valid)) + ')'

    def map(self, fn: Callable[[T], ValidatorPayload]) -> Validator[ValidatorPayload]:
        return Validator(fn(self.value))

    def chain(self, fn: Union[Callable[[T], Validator[ValidatorPayload]], Callable[[T], ValidatorPayload]]) -> Union[
        Validator[ValidatorPayload], ValidatorPayload]:
        return fn(self.value) if self.valid else self