import click

from commons.timing import subcommand

__all__ = ["trade_group"]


@click.group()
def trade_group():
    pass


@trade_group.command()
@click.option("--broker", "-b", help="Broker backend name")
@click.option("--input", "-i", help="Input file to base the decisions from")
@subcommand([])
def trade(*args, **kwargs):
    pass
