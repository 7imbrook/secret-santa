#!/usr/bin/env python

import click
import sqlite3
from lib import get_shuffled, load_people
from sms import send_message
from util import FOLLOWUP, INTRO, MESSAGE, InvalidConfiguration, MaxIterationsReached
from tabulate import tabulate


@click.group()
def main():
    """
    Run the secret santa app
    """
    pass


@main.command()
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--max-iterations", default=100)
def shuffle(dry_run, max_iterations):
    people = load_people()
    try:
        pairs = get_shuffled(people, max_iterations)
    except MaxIterationsReached:
        raise click.UsageError(
            f"Failed to find valid pair in {max_iterations} iterations"
        )
    except InvalidConfiguration:
        raise click.UsageError(
            "Please make sure to add at least 2 people via add-people"
        )
    if dry_run:
        pairs = sorted(pairs, key=lambda p: p[0].household)
        print(tabulate(pairs))
    else:
        for give, recieve in pairs:
            send_message(INTRO, give.number)
            send_message(
                MESSAGE.format(giver=give.name, reciever=recieve.name), give.number
            )
            send_message(FOLLOWUP, give.number)


@main.command()
@click.argument("name", nargs=1)
@click.argument("number", nargs=1)
@click.argument("household", nargs=1)
def add_person(name, number, household):
    with sqlite3.connect("db.sqlite") as db:
        db.execute(
            "insert into people (name, number, household) values (?, ?, ?)",
            (name, number, household),
        )


@main.command()
def new():
    with sqlite3.connect("db.sqlite") as db:
        db.execute("drop table if exists people;")
        db.execute(
            "create table people (name TEXT PRIMARY KEY, number TEXT, household TEXT);"
        )


if __name__ == "__main__":
    main()
