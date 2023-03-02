import click

from core.subcommand_execution.execution_flow import execution_flow
from settings.steps.set_var import set_var

__all__ = ["set_group"]


@click.group()
def set_group():
    pass


@set_group.command()
@click.argument("key")
@click.argument("value")
@execution_flow(
    set_var
)
def set(*args, **kwargs):
    """
    Set global value for a variable
    """
