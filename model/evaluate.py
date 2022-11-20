import click

from commons.steps.conditional import conditional
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.steps.rename_parameters import rename_parameters
from commons.timing import subcommand
from model.steps.initialize_model import initialize_model
from model.steps.evaluate_predictions import evaluate_predictions
from commons.steps.generate_predictions import generate_predictions
from model.steps.get_model_module import get_model_module
from model.steps.get_strategy_module import get_strategy_module
from model.steps.initialize_clearml import initialize_clearml
from model.steps.load_weights import load_weights
from model.steps.run_training import run_training
from model.steps.save_weights import save_weights
from model.steps.submit_to_drive import submit_to_drive

__all__ = ["evaluate_group"]


@click.group()
def evaluate_group():
    pass


@evaluate_group.command()
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--model-config", "-mc", help="Drivepath of the model's configuration file (in JSON format)")
@click.option("--dataset", "-d",
              help="Labelled dataset to use for evaluation")
@click.option("--label", "-l",
              help="Name of the label column within the test dataset")
@click.option("--clearml-access-key", help="ClearML access key")
@click.option("--clearml-secret-key", help="ClearML secret key")
@click.option("--clearml-project", help="ClearML project name")
@subcommand([
    process_parameter("model"),
    process_parameter("model_config", optional=True),
    process_parameter("dataset"),
    process_parameter("label", optional=True),
    process_parameter("clearml_access_key", optional=True),
    process_parameter("clearml_secret_key", optional=True),
    process_parameter("clearml_project", optional=True),
    conditional(initialize_clearml, "clearml_access_key"),
    get_dataset,
    get_model_module,
    initialize_model,
    load_weights,
    generate_predictions,
    evaluate_predictions,
    submit_to_drive
])
def evaluate(*args, **kwargs):
    pass
