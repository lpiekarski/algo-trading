import click

from collector.steps.download_data import download_data
from collector.steps.save_dataset import save_dataset
from commons.timing import subcommand

__all__ = ["collect_group"]

@click.group()
def collect_group():
    pass

@collect_group.command()
@click.option("--date", "-d", default="latest", help="Date for which to collect the data (can be 'latest' for last available hour)")
@click.option("--name", "-n", help="Name of the created dataset. If none is provided defaults to the YYYY-mm-dd-HH-MM date")
def collect(*args, **kwargs):
    collect_subcommand(*args, **kwargs)

@subcommand("collector:collect", [download_data, save_dataset])
def collect_subcommand(*args, **kwargs):
    pass

if __name__ == '__main__':
    collect()