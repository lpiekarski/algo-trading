import click

from core.subcommand_execution.execution_flow import execution_flow
from drive.steps.copy import copy

__all__ = ["copy_group"]


@click.group()
def copy_group():
    pass


@copy_group.command()
@click.argument("source")
@click.argument("target")
@execution_flow(
    copy
)
def copy(*args, **kwargs):
    """
    Copy file between local or remote locations
    """
