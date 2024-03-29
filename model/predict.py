import click

from core.steps.get_dataset import get_dataset
from core.subcommand_execution.execution_flow import execution_flow
from model.steps.generate_predictions import generate_predictions
from model.steps.get_model_module import get_model_module
from model.steps.initialize_model import initialize_model
from model.steps.load_weights import load_weights
from model.steps.save_prediction_result import save_prediction_result

__all__ = ["predict_group"]


@click.group()
def predict_group():
    pass


@predict_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--model-config", "-mc", help="Drivepath of the model's configuration file (in JSON format)")
@click.option("--dataset", "-d", help="Dataset to generate a prediction for")
@click.option("--output", "-o", help="Name of the results file")
@click.option("--label", "-l",
              help="Name of the label column within the dataset (required for transformer models)")
@execution_flow(
    get_dataset,
    get_model_module,
    initialize_model,
    load_weights,
    generate_predictions,
    save_prediction_result
)
def predict(*args, **kwargs):
    """
    Generate model predictions for given data
    """
