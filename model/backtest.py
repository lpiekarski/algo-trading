import click

from commons.steps.conditional import conditional
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.steps.rename_parameters import rename_parameters
from commons.timing import subcommand
from model.steps.initialize_model import initialize_model
from model.steps.evaluate_predictions import evaluate_predictions
from model.steps.backtest_predictions import run_backtesting
from commons.steps.generate_predictions import generate_predictions
from model.steps.get_model_module import get_model_module
from model.steps.get_strategy_module import get_strategy_module
from model.steps.initialize_clearml import initialize_clearml
from model.steps.load_weights import load_weights
from model.steps.run_training import run_training
from model.steps.save_weights import save_weights
from model.steps.submit_to_drive import submit_to_drive

__all__ = ["backtest_group"]


@click.group()
def backtest_group():
    pass


@backtest_group.command()
@click.option("--strategy",
              "-s",
              help="Strategy used in backtesting")
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--model-config", "-mc", help="Model config file")
@click.option("--dataset", "-trd", help="Dataset to use for training")
@click.option("--clearml-access-key", "-cak", help="ClearML access key")
@click.option("--clearml-secret-key", "-csk", help="ClearML secret key")
@click.option("--clearml-project", "-cp", help="ClearML project name")
@click.option("--backtest-threshold",
              "-bt",
              help="Minimum confidence to make a decision during backtesting",
              default=0.01)
@click.option("--backtest-volume", "-bv",
              help="Backtest trade volume", default=1)
@click.option("--backtest-tpsl-pct",
              "-btpsl",
              help="Backtest take profit/stop loss price change percentage",
              default=0.01)
@click.option("--backtest-commission",
              "-bcm",
              help="Backtest comission fee percentage for each transaction",
              default=0.0002)
@click.option("--backtest-leverage", "-bm",
              help="Backtest leverage", default=30)
@click.option("--backtest-cash",
              "-bcs",
              help="Backtest starting cash amount",
              default=200000)
@subcommand([
    process_parameter("model", optional=True),
    process_parameter("model_config", optional=True),
    process_parameter("dataset"),
    process_parameter("strategy"),
    process_parameter("clearml_access_key", optional=True),
    process_parameter("clearml_secret_key", optional=True),
    process_parameter("clearml_project", optional=True),
    process_parameter("backtest_threshold"),
    process_parameter("backtest_volume"),
    process_parameter("backtest_tpsl_pct"),
    process_parameter("backtest_commission"),
    process_parameter("backtest_leverage"),
    process_parameter("backtest_cash"),
    conditional(initialize_clearml, "clearml_access_key"),
    get_dataset,
    conditional(get_model_module, "model"),
    conditional(initialize_model, 'model'),
    conditional(load_weights, 'model'),
    conditional(generate_predictions, 'model'),
    get_strategy_module,
    run_backtesting
])
def backtest(*args, **kwargs):
    pass
