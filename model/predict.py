import click
import logging

__all__ = ["predict", "predict_group"]

from commons.timing import command_success

LOGGER = logging.getLogger(__name__)

@click.group()
def predict_group():
    pass

@predict_group.command()
def predict():
    command_success(LOGGER)

if __name__ == '__main__':
    predict()