import click

from core.subcommand_execution.execution_flow import execution_flow
from drive.steps.delete import delete

__all__ = ["delete_group"]


@click.group()
def delete_group():
    pass


@delete_group.command()
@click.argument("path")
@execution_flow(
    delete
)
def delete(*args, **kwargs):
    """Delete file from local or remote location"""
