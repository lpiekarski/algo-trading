import click
from click import group, option

from collector.steps.download_data import download_data
from collector.steps.save_dataset import save_dataset
from commons.timing import subcommand

__all__ = ["collect_group"]

@group()
def collect_group():
    pass

@collect_group.command()
@option("--date", "-d", default="latest", help="Date for which to collect the data (can be 'latest' for last available hour)")
@option("--name", "-n", help="Name of the created dataset. If none is provided defaults to the YYYY-mm-dd-HH-MM date")
@subcommand([
    download_data,
    save_dataset
])
def collect(*args, **kwargs):
    pass

if __name__ == '__main__':
    collect()