import click
import logging

from commons.broker_api import get_broker_module
from commons.string import BREAK, break_padded
from commons.timing import command_success

__all__ = ["trade", "trade_group"]


LOGGER = logging.getLogger(__name__)

@click.group()
def trade_group():
    pass

@trade_group.command()
@click.option("--broker", "-b", help="Broker backend name")
@click.option("--input", "-i", help="Input file to base the decisions from")
def trade(broker: str, input: str):
    LOGGER.info(break_padded(f"trader:trade"))
    LOGGER.info("")
    broker_module = get_broker_module(broker)
    command_success(LOGGER)

if __name__ == '__main__':
    trade()