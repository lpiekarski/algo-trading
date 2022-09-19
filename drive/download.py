import click

from commons.timing import subcommand
from drive.steps.download import download

__all__ = ["download_group"]

@click.group()
def download_group(): pass

@download_group.command()
@click.argument("remote_path")
@click.argument("local_path")
@subcommand([
    download
])
def download(*args, **kwargs): pass
