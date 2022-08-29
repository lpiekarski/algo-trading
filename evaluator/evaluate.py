import click

import logging

__all__ = ["evaluate_group"]

from commons.dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from evaluator.steps.evaluate_predictions import evaluate_predictions
from commons.steps.generate_predictions import generate_predictions
from evaluator.steps.submit_to_neptune import submit_to_neptune

LOGGER = logging.getLogger(__name__)

@click.group()
def evaluate_group():
    pass

@evaluate_group.command()
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--dataset", "-d", help="Labelled dataset to use for evaluation")
@click.option("--NEPTUNE_API_KEY", "-N", help="Neptune api key")
@subcommand([
    process_parameter("model"),
    process_parameter("dataset"),
    process_parameter("NEPTUNE_API_KEY", optional=True),
    get_dataset,
    generate_predictions,
    evaluate_predictions,
    submit_to_neptune
])
def evaluate(*args, **kwargs):
    pass

if __name__ == '__main__':
    evaluate()