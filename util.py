from typing import Sequence, TypeVar

T = TypeVar("T")


def rotate(l: Sequence[T]) -> Sequence[T]:
    return l[1:] + l[:1]


class MaxIterationsReached(Exception):
    pass


class InvalidConfiguration(Exception):
    pass
