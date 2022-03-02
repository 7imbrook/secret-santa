from typing import Sequence, TypeVar

T = TypeVar("T")


def rotate(l: Sequence[T]) -> Sequence[T]:
    return l[1:] + l[:1]


class MaxIterationsReached(Exception):
    pass


class InvalidConfiguration(Exception):
    pass


INTRO = "Hi, get ready for Timbrook Secret Santa!"
MESSAGE = "{giver}, you'll be buying for {reciever} this year."
FOLLOWUP = "No house rules have been set yet, follow up with the family. I've fixed Johns issue so this is the real deal now."
