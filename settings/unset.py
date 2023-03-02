import click

from core.subcommand_execution.execution_flow import execution_flow
from settings.steps.unset_var import unset_var

__all__ = ["unset_group"]


@click.group()
def unset_group():
    pass


@unset_group.command()
@click.argument("key")
@execution_flow(
    unset_var
)
def unset(*args, **kwargs):
    """Reset value of the global variable"""
