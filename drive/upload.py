import click

from core.subcommand_execution.execution_flow import execution_flow
from drive.steps.upload import upload

__all__ = ["upload_group"]


@click.group()
def upload_group():
    pass


@upload_group.command()
@click.argument("local_path")
@click.argument("remote_path")
@execution_flow(
    upload
)
def upload(*args, **kwargs):
    """Upload a file to the default drive"""
