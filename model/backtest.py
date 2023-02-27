import click

from core.steps.conditional import Conditional
from core.steps.get_dataset import get_dataset
from core.subcommand_execution.execution_flow import execution_flow
from model.steps.generate_predictions import generate_predictions
from model.steps.initialize_model import initialize_model
from model.steps.run_backtesting import run_backtesting
from model.steps.get_model_module import get_model_module
from model.steps.get_strategy_module import get_strategy_module
from model.steps.initialize_clearml import initialize_clearml
from model.steps.load_weights import load_weights
from model.benchmark import benchmark_time_tags

__all__ = ["backtest_group"]


@click.group()
def backtest_group():
    pass


@backtest_group.command()
@click.option("--strategy",
              "-s",
              help="Strategy used in backtesting")
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--model-config", "-mc", help="Drivepath of the model's configuration file (in JSON format)")
@click.option("--strategy-config", "-sc", help="Drivepath of the strategy configuration file (in JSON format)")
@click.option("--dataset", "-trd", help="Dataset to use for training")
@click.option("--clearml-access-key", "-cak", help="ClearML access key")
@click.option("--clearml-secret-key", "-csk", help="ClearML secret key")
@click.option("--clearml-project", "-cp", help="ClearML project name")
@click.option("--commission",
              "-bcm",
              help="Backtest comission fee percentage for each transaction",
              default=0.0002)
@click.option("--leverage", "-bm",
              help="Backtest leverage", default=30)
@click.option("--starting-cash",
              "-bcs",
              help="Backtest starting cash amount",
              default=200000)
@execution_flow(
    Conditional(initialize_clearml, "clearml_access_key"),
    get_dataset,
    Conditional(get_model_module, "model"),
    Conditional(initialize_model, "model"),
    Conditional(load_weights, "model"),
    Conditional(generate_predictions, "model"),
    get_strategy_module,
    run_backtesting,
    benchmark_time_tags
)
def backtest(*args, **kwargs):
    """
    Backtest a strategy and a model
    """
