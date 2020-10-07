#!/usr/bin/env python3.8

import click
import sqlite3
from sms import send_message
from util import rotate


@click.group()
def main():
    """
    Run the secret santa app
    """
    pass


@main.command()
@click.option('--dry-run', is_flag=True, default=False)
@click.option('--max-iterations', default=10)
def shuffle(dry_run, max_iterations):
    with sqlite3.connect("db.sqlite") as db:
        while True:
            random_ordering = list(
                db.execute("select name, household, number from people order by random();")
            )
            if len(random_ordering) == 0:
                raise click.UsageError("You'll need to add people first. see add-people command.")

            pairs = list(zip(random_ordering, rotate(random_ordering)))
            for give, recieve in pairs:
                if give[1] == recieve[1]:
                    # Break skips the else block the breaks the while true
                    max_iterations -= 1
                    if max_iterations <= 0:
                        raise click.UsageError("Spent too long looking for matching, may be imposible. Try setting --max-iterations higher.")
                    break
            else:
                click.secho("Found valid matches", fg="green")
                # Break out of the while true
                break
        
        for (giver, _, send_to_number), (recipient, __, ___) in pairs:
            message = f"Shhhhhhhhhhhh 🤫🎅🏽  {giver}. We've picked your recipient for the Timbrook secret santa. This year you'll be getting a gift for {recipient}."
            if dry_run:
                click.echo(f"{giver} [{send_to_number}] -> {recipient}")
            else:
                send_message(message, send_to_number)


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