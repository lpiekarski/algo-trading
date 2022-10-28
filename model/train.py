import click

from commons.steps.conditional import conditional
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from model.steps.get_model_module import get_model_module
from model.steps.run_training import run_training
from model.steps.save_model import save_model

__all__ = ["train_group"]


@click.group()
def train_group(): pass

@train_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--dataset", "-d", help="Train dataset")
@click.option("--skip-save", "-s", help="Do not save the results of the training", is_flag=True)
@click.option("--label", "-l", help="Name of the label column within the dataset", default="y")
@subcommand([
    process_parameter('model'),
    process_parameter('dataset'),
    process_parameter('skip_save'),
    get_model_module,
    get_dataset,
    run_training,
    conditional(save_model, "skip_save", negation=True)
])
def train(*args, **kwargs): pass
