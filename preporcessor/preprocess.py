import click

from core.subcommand_execution.execution_flow import execution_flow
from preporcessor.steps.preprocess_data import preprocess_data
from preporcessor.steps.read_config import read_config
from preporcessor.steps.save_data import save_data

__all__ = ["preprocess_group"]


@click.group()
def preprocess_group():
    pass


@preprocess_group.command()
@click.option("--config_path", "-cf", help="Drivepath to the preprocessing configuration YAML file", default="...")
@click.option("--dataset", "-ds", help="Drivepath to the dataset file to be preprocessed")
@execution_flow(
    read_config,
    preprocess_data,
    save_data
)
def preprocess(*args, **kwargs):
    """
    Copy file between local or remote locations
    """
