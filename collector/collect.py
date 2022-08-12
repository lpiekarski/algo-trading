import click
import logging

__all__ = ["collect", "collect_group"]

from commons.timing import command_success

LOGGER = logging.getLogger(__name__)

@click.group()
def collect_group():
    pass

@collect_group.command()
def collect():
    command_success(LOGGER)

if __name__ == '__main__':
    collect()