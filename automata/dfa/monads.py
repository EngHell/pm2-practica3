from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union

T = TypeVar('T')


class Unit(Generic[T]):
    # as for our unit we care for to be identical if its of the same type
    # and holds the same value.
    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.value == other.value
        return False

    def __init__(self, value: T):
        self.value = value

    def emit(self) -> T:
        return self.value


FunctorCallable = Callable[[T], T]


class Functor(ABC, Unit[T]):
    def __rshift__(self, other: MonoidCallable) -> Union[Monad[T], T]:
        return self.map(other)

    @abstractmethod
    def map(self, fn: FunctorCallable) -> Functor[T]:
        pass


class Monad(Functor[T]):
    def __ge__(self, other):
        return self.chain(other)

    def chain(self, fn: MonoidCallable) -> Union[Monad[T], T]:
        return fn(self.value)

    @abstractmethod
    def __repr__(self):
        pass


MonoidCallable = Union[Callable[[T], Monad[T]], Callable[[T], T]]


class Identity(Monad[T]):

    def map(self, fn: Callable[[T], T]) -> Identity[T]:
        return Identity(fn(self.value))

    def __repr__(self):
        return 'Identity(' + repr(self.value) + ')'


class Either(Monad[T]):
    @abstractmethod
    def map(self, fn: FunctorCallable) -> Either[T]:
        pass

    def flatten(self):
        return self.value

    @abstractmethod
    def __repr__(self):
        return 'Either(' + repr(self.value) + ')'

    @abstractmethod
    def chain(self, fn: MonoidCallable) -> Union[Either[T], T]:
        pass

    @abstractmethod
    def chain_catch(self, fn: MonoidCallable) -> Union[Either[T], T]:
        pass

    @abstractmethod
    def catch(self, fn: FunctorCallable) -> Either[T]:
        pass


class Left(Either[T]):

    def __repr__(self):
        return 'Left(' + repr(self.value) + ')'

    def flatten(self):
        return self

    def map(self, fn: FunctorCallable) -> Either[T]:
        return self

    def chain(self, fn: MonoidCallable) -> Union[Either[T], T]:
        return self.map(fn).flatten()

    def catch(self, fn: FunctorCallable) -> Right[T]:
        return Right(fn(self.value))

    def chain_catch(self, fn: MonoidCallable) -> Union[Either[T], T]:
        return self.catch(fn).flatten()


class Right(Either[T]):

    def map(self, fn: FunctorCallable) -> Right[T]:
        return Right(fn(self.value))

    def __repr__(self):
        return 'Right(' + repr(self.value) + ')'

    def chain(self, fn: MonoidCallable) -> Union[Right[T], T]:
        return self.map(fn).flatten()

    def catch(self, fn: FunctorCallable) -> Right[T]:
        return self

    def chain_catch(self, fn: MonoidCallable) -> Union[Either[T], T]:
        return Left(self.value)

class IO:
    def __init__(self, action):
        self.action = action

    def __rshift__(self, other):
        return other(self.action())

    @staticmethod
    def lift(self, value):
        return IO(lambda: value)

    @staticmethod
    def put_str_ln(text):
        return IO(lambda: print(text))


IO.get_line = IO(lambda: input())


def main():
    one = Identity(1)

    two = one.map(lambda v: v * 2)
    print(one)
    print(two)

    # test on monad laws
    # left identity
    def f(value: int) -> Identity[int]:
        return Identity(value * 2)

    def g(value: int) -> Identity[int]:
        return Identity(value * 3)

    a = Identity(3).chain(f)
    b = f(3)

    if a == b:
        print('Equal o:')

    # right identity
    m = Identity(4)
    print('chaining')
    m >> f >> g >> print
    print('not chaining')

    def h(value: int) -> int:
        return value + 1

    print(m.chain(h))

    print(m.chain(Identity) == m)

    print(m.chain(f).chain(g) == m.chain(lambda x: f(x).chain(g)))

    v = IO.put_str_ln('holis bitch')

    def dummy(x):
        pass

    v >> dummy

    IO.get_line >> IO.put_str_ln >> dummy


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
