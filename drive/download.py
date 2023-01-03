import click

from commons.subcommand_execution.execution_flow import execution_flow
from drive.steps.download import download

__all__ = ["download_group"]


@click.group()
def download_group():
    pass


@download_group.command()
@click.argument("remote_path")
@click.argument("local_path")
@execution_flow(
    download
)
def download(*args, **kwargs):
    """Download a file from the default drive"""
