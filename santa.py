#!/usr/bin/env python

import click
import sqlite3
from lib import get_shuffled, load_people
from util import MaxIterationsReached


@click.group()
def main():
    """
    Run the secret santa app
    """
    pass


@main.command()
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--max-iterations", default=25)
def shuffle(dry_run, max_iterations):
    people = load_people()
    pairs = get_shuffled(people, max_iterations)
    print(pairs)


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
