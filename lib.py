import sqlite3
from random import shuffle
from typing import Sequence, Tuple
from util import InvalidConfiguration, MaxIterationsReached, rotate
from type import Person


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


def _household_rule(give: Person, recieve: Person) -> bool:
    return give.household is not recieve.household


def _post_validate_rule(pairs: Sequence[Tuple[Person, Person]]) -> bool:
    households = set()
    givings = set()
    for g, r in pairs:
        households.add(g.household)
        givings.add(f"{g.household}{r.household}")
    return (len(households) * 2) == len(givings)


def get_shuffled(people: Sequence[Person], max_iterations: int):
    while True:
        if len(people) == 0:
            raise InvalidConfiguration()

        pairs = list(zip(people, rotate(people)))
        for give, recieve in pairs:
            max_iterations -= 1
            if max_iterations <= 0:
                raise MaxIterationsReached()
            # Validations
            if not all([_household_rule(give, recieve)]):
                # break to else break
                break
        else:
            # Break out of the while true if all pairs validated
            if _post_validate_rule(pairs):
                break
        shuffle(people)

    return pairs
