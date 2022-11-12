import click

from commons.steps.generate_predictions import generate_predictions
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from model.steps.download_model import download_model
from model.steps.get_model_module import get_model_module
from model.steps.save_prediction_result import save_prediction_result

__all__ = ["predict_group"]


@click.group()
def predict_group():
    pass


@predict_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--dataset", "-d", help="Dataset to generate a prediction for")
@click.option("--output", "-o", help="Name of the results file")
@subcommand([
    process_parameter('model'),
    process_parameter('dataset'),
    process_parameter('output', optional=True),
    get_model_module,
    get_dataset,
    download_model,
    generate_predictions,
    save_prediction_result
])
def predict(*args, **kwargs):
    pass
