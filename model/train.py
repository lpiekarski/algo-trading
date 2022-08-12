import click
import logging

__all__ = ["train", "train_group"]

from commons.timing import command_success

LOGGER = logging.getLogger(__name__)

@click.group()
def train_group():
    pass

@train_group.command()
def train():
    command_success(LOGGER)

if __name__ == '__main__':
    train()