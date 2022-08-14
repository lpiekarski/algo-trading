import click
import logging

__all__ = ["collect", "collect_group"]

from commons.timing import command_success

LOGGER = logging.getLogger(__name__)

@click.group()
def collect_group():
    pass

@collect_group.command()
@click.option("--date", "-d", help="Date for which to collect the data (can be 'latest' for last available hour)")
@click.option("--name", "-n", help="Name of the created dataset. If none is provided defaults to the yyyy-MM-dd-HH date")
def collect(date: str, name: str):
    command_success(LOGGER)

if __name__ == '__main__':
    collect()