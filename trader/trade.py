import click

__all__ = ["trade_group"]

from core.subcommand_execution.execution_flow import execution_flow


@click.group()
def trade_group():
    pass


@trade_group.command()
@click.option("--broker", "-b", help="Broker backend name")
@click.option("--input", "-i", help="Input file to base the decisions from")
@execution_flow()
def trade(*args, **kwargs):
    """
    Trade based on a given input
    """
