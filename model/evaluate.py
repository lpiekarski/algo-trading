import click

from core.steps.conditional import Conditional
from core.steps.get_dataset import get_dataset
from core.subcommand_execution.execution_flow import execution_flow
from model.steps.finalize_clearml import finalize_clearml
from model.steps.generate_predictions import generate_predictions
from model.steps.initialize_model import initialize_model
from model.steps.evaluate_predictions import evaluate_predictions
from model.steps.get_model_module import get_model_module
from model.steps.initialize_clearml import initialize_clearml
from model.steps.load_weights import load_weights
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
@execution_flow(
    Conditional(initialize_clearml, "clearml_access_key"),
    get_dataset,
    get_model_module,
    initialize_model,
    load_weights,
    generate_predictions,
    evaluate_predictions,
    submit_to_drive,
    Conditional(finalize_clearml, "clearml_access_key")
)
def evaluate(*args, **kwargs):
    """
    Evaluate a model using given dataset
    """
