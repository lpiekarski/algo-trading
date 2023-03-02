import click

from core.steps.conditional import Conditional
from core.steps.get_dataset import get_dataset
from core.subcommand_execution.execution_flow import execution_flow
from model.steps.generate_predictions import generate_predictions
from model.steps.generate_trades import generate_trades
from model.steps.get_model_module import get_model_module
from model.steps.get_strategy_module import get_strategy_module
from model.steps.initialize_model import initialize_model
from model.steps.initialize_strategy import initialize_strategy
from model.steps.load_strategy_state import load_strategy_state
from model.steps.load_weights import load_weights
from model.steps.save_strategy_state import save_strategy_state
from trader.steps.dispose_broker import dispose_broker
from trader.steps.get_broker_module import get_broker_module
from trader.steps.initialize_broker import initialize_broker
from trader.steps.perform_trade import perform_trade

__all__ = ["trade_group"]


@click.group()
def trade_group():
    pass


@trade_group.command()
@click.option("--strategy",
              "-s",
              help="Strategy used in backtesting")
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--model-config", "-mc", help="Drivepath of the model's configuration file (in JSON format)")
@click.option("--strategy-config", "-sc", help="Drivepath of the strategy configuration file (in JSON format)")
@click.option("--dataset", "-trd", help="Dataset to use for training")
@click.option("--label", "-l", help="Name of the label column within the dataset")
@click.option("--broker", "-b", help="Broker backend name")
@click.option("--broker-config", "-bc", help="Broker backend specific configuration yaml file")
@execution_flow(
    get_dataset,
    Conditional(get_model_module, "model"),
    Conditional(initialize_model, "model"),
    Conditional(load_weights, "model"),
    Conditional(generate_predictions, "model"),
    get_strategy_module,
    initialize_strategy,
    load_strategy_state,
    generate_trades,
    get_broker_module,
    initialize_broker,
    perform_trade,
    dispose_broker,
    save_strategy_state
)
def trade(*args, **kwargs):
    """
    Trade based on a given input
    """
