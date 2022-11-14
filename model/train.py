import click

from commons.steps.conditional import conditional
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
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
@click.option("--model", "-m", help="Drivepath of the model's weights file. The name of the file must match the name of the model module")
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
@subcommand([
    process_parameter('model'),
    process_parameter('model_config', optional=True),
    process_parameter('dataset'),
    process_parameter('no_save'),
    process_parameter("clearml_access_key", optional=True),
    process_parameter("clearml_secret_key", optional=True),
    process_parameter("clearml_project", optional=True),
    process_parameter('label', optional=True),
    conditional(initialize_clearml, "clearml_access_key"),
    get_dataset,
    get_model_module,
    initialize_model,
    load_weights,
    run_training,
    conditional(save_weights, "no_save", negation=True)
])
def train(*args, **kwargs):
    pass
