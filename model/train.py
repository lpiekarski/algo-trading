import click
from commons.steps.get_labeled_dataset import get_labeled_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from model.steps.download_model import download_model
from model.steps.get_model_module import get_model_module
from model.steps.run_training import run_training
from model.steps.save_model import save_model

__all__ = ["train_group"]


@click.group()
def train_group(): pass

@train_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--dataset", "-d", help="Train dataset")
@click.option("--skip_save", "-s", help="Do not save the results of the training", is_flag=True)
@click.option("--label", "-l", help="Name of the label column within the dataset", default="y")
@subcommand([
    process_parameter('model'),
    process_parameter('dataset'),
    process_parameter('skip_save'),
    get_model_module,
    get_labeled_dataset,
    download_model,
    run_training,
    save_model
])
def train(*args, **kwargs): pass
