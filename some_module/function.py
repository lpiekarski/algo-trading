import click

from core.subcommand_execution.execution_flow import execution_flow
from some_module.steps.function_x import function_x

__all__ = ["function_group"]


@click.group()
def function_group():
    pass


@function_group.command()
@execution_flow(
    function_x
)
def function(*args, **kwargs):
    """
    Function for tests
    """
