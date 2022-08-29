import click

__all__ = ["train", "train_group"]

from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from model.steps.get_train_dataset import get_train_dataset
from model.steps.run_training import run_training

@click.group()
def train_group():
    pass

@train_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--dataset", "-d", help="Train dataset")
@subcommand([
    process_parameter('model'),
    process_parameter('dataset'),
    get_train_dataset,
    run_training,
])
def train(model: str, dataset: str):
    pass

if __name__ == '__main__':
    train()