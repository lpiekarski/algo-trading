import click

from core.steps.conditional import Conditional
from core.steps.get_dataset import get_dataset
from core.subcommand_execution.execution_flow import execution_flow
from model.steps.finalize_clearml import finalize_clearml
from model.steps.generate_predictions import generate_predictions
from model.steps.generate_trades import generate_trades
from model.steps.initialize_model import initialize_model
from model.steps.initialize_strategy import initialize_strategy
from model.steps.load_strategy_state import load_strategy_state
from model.steps.run_backtesting import run_backtesting
from model.steps.get_model_module import get_model_module
from model.steps.get_strategy_module import get_strategy_module
from model.steps.initialize_clearml import initialize_clearml
from model.steps.load_weights import load_weights

__all__ = ["backtest_group"]

from model.steps.save_strategy_state import save_strategy_state


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
@click.option("--label", "-l", help="Names of the label column within the dataset (comma separated list without spaces)")
@click.option("--clearml-access-key", "-cak", help="ClearML access key")
@click.option("--clearml-secret-key", "-csk", help="ClearML secret key")
@click.option("--clearml-project", "-cp", help="ClearML project name")
@click.option("--commission",
              "-bcm",
              help="Backtest comission fee percentage for each transaction",
              default=0.00015)
@click.option("--leverage", "-bm",
              help="Backtest leverage", default=20)
@click.option("--starting-cash",
              "-bcs",
              help="Backtest starting cash amount",
              default=10000)
@click.option("--trade-every-n", help="Trade every n steps", default=1)
@execution_flow(
    get_dataset,
    Conditional(get_model_module, "model"),
    Conditional(initialize_model, "model"),
    Conditional(load_weights, "model"),
    Conditional(generate_predictions, "model"),
    get_strategy_module,
    initialize_strategy,
    load_strategy_state,
    Conditional(initialize_clearml, "clearml_access_key"),
    generate_trades,
    run_backtesting,
    save_strategy_state,
    Conditional(finalize_clearml, "clearml_access_key")
)
def backtest(*args, **kwargs):
    """
    Backtest a strategy and a model
    """
