import click

from commons.steps.get_labeled_dataset import get_labeled_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from model.steps.download_model import download_model
from model.steps.evaluate_predictions import evaluate_predictions
from commons.steps.generate_predictions import generate_predictions
from model.steps.get_model_module import get_model_module
from model.steps.submit_to_drive import submit_to_drive

__all__ = ["evaluate_group"]

@click.group()
def evaluate_group(): pass

@evaluate_group.command()
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--dataset", "-d", help="Labelled dataset to use for evaluation")
@click.option("--label", "-l", help="Name of the label column within the dataset", default="y")
@subcommand([
    process_parameter("model"),
    process_parameter("dataset"),
    process_parameter("label"),
    get_model_module,
    get_labeled_dataset,
    download_model,
    generate_predictions,
    evaluate_predictions,
    submit_to_drive
])
def evaluate(*args, **kwargs): pass
