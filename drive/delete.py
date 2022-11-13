import click

from commons.timing import subcommand
from drive.steps.delete import delete

__all__ = ["delete_group"]


@click.group()
def delete_group():
    pass


@delete_group.command()
@click.argument("path")
@subcommand([
    delete
])
def delete(*args, **kwargs):
    pass
