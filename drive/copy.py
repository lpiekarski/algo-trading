import click

from commons.timing import subcommand
from drive.steps.copy import copy

__all__ = ["copy_group"]


@click.group()
def copy_group():
    pass


@copy_group.command()
@click.argument("source")
@click.argument("target")
@subcommand([
    copy
])
def copy(*args, **kwargs):
    pass
