import click

from commons.timing import subcommand
from drive.steps.upload import upload

__all__ = ["upload_group"]


@click.group()
def upload_group():
    pass


@upload_group.command()
@click.argument("local_path")
@click.argument("remote_path")
@subcommand([
    upload
])
def upload(*args, **kwargs):
    pass
