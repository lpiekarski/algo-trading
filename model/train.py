import click

from core.steps.conditional import Conditional
from core.steps.get_dataset import get_dataset
from core.subcommand_execution.execution_flow import execution_flow
from model.steps.finalize_clearml import finalize_clearml
from model.steps.get_model_module import get_model_module
from model.steps.initialize_clearml import initialize_clearml
from model.steps.initialize_model import initialize_model
from model.steps.load_weights import load_weights
from model.steps.run_training import run_training

__all__ = ["train_group"]

from model.steps.save_weights import save_weights


@click.group()
def train_group():
    pass


@train_group.command()
@click.option("--model", "-m",
              help="Drivepath of the model's weights file. The name of the file must match the name of the model module")
@click.option("--model-config", "-mc", help="Drivepath of the model's configuration file (in JSON format)")
@click.option("--dataset", "-d", help="Drivepath of the training dataset")
@click.option("--no-save",
              "-s",
              help="Do not save the results of the training",
              is_flag=True)
@click.option("--label", "-l",
              help="Name of the label column within the training dataset")
@click.option("--clearml-access-key", "-cak", help="ClearML access key")
@click.option("--clearml-secret-key", "-csk", help="ClearML secret key")
@click.option("--clearml-project", "-cp", help="ClearML project name")
@click.option("--new-weights", "-nw", help="Initialize weights randomly", is_flag=True, default=None)
@click.option("--output", "-nw", help="Output path for model weights", default=None)
@execution_flow(
    get_dataset,
    get_model_module,
    Conditional(initialize_clearml, "clearml_access_key"),
    initialize_model,
    Conditional(load_weights, "new_weights", False),
    run_training,
    Conditional(save_weights, "no_save", False),
    Conditional(finalize_clearml, "clearml_access_key")
)
def train(*args, **kwargs):
    """
    Train a model on a given dataset
    """
