from os import P_NOWAITO
import sqlite3
from typing import Sequence
from dataclasses import dataclass
from util import InvalidConfiguration, MaxIterationsReached, rotate


@dataclass
class Person:
    name: str
    number: str  # Yeah sure doesn't matter
    household: str


def load_people() -> Sequence[Person]:
    """Loadiing a random ordering of people

    Returns:
        Sequence[Person]: Get a random order of people from the DB
    """
    with sqlite3.connect("db.sqlite") as db:
        return [
            Person(
                name=p[0],
                household=p[1],
                number=p[2],
            )
            for p in db.execute(
                "select name, household, number from people order by random();"
            )
        ]


def get_shuffled(people: Sequence[Person], max_iterations: int):
    while True:
        if len(people) == 0:
            raise InvalidConfiguration()

        pairs = list(zip(people, rotate(people)))
        for give, recieve in pairs:
            if give.household == recieve.household:
                # Break skips the else block the breaks the while true
                max_iterations -= 1
                if max_iterations <= 0:
                    raise MaxIterationsReached()
                break
        else:
            # Break out of the while true
            break
    return pairs
