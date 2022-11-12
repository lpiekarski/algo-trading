import click

from commons.steps.conditional import conditional
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.steps.rename_parameters import rename_parameters
from commons.timing import subcommand
from model.steps.download_model import download_model
from model.steps.evaluate_predictions import evaluate_predictions
from model.steps.backtest_predictions import backtest_predictions
from commons.steps.generate_predictions import generate_predictions
from model.steps.get_model_module import get_model_module
from model.steps.initialize_clearml import initialize_clearml
from model.steps.run_training import run_training
from model.steps.save_model import save_model
from model.steps.submit_to_drive import submit_to_drive

__all__ = ["evaluate_group"]


@click.group()
def evaluate_group():
    pass


@evaluate_group.command()
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--train-dataset", "-trd", help="Dataset to use for training")
@click.option("--train-label", "-trl",
              help="Name of the label column within the train dataset")
@click.option("--test-dataset", "-tsd",
              help="Labelled dataset to use for evaluation")
@click.option("--test-label", "-tsl",
              help="Name of the label column within the test dataset")
@click.option("--skip-save",
              "-ss",
              help="Do not save the results of the training",
              is_flag=True)
@click.option("--clearml-access-key", "-cak", help="ClearML access key")
@click.option("--clearml-secret-key", "-csk", help="ClearML secret key")
@click.option("--clearml-project", "-cp", help="ClearML project name")
@click.option("--skip-backtest",
              "-sb",
              help="Skip backtesting",
              is_flag=True,
              default=False)
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
    process_parameter("model"),
    process_parameter("train_dataset", optional=True),
    conditional(process_parameter("train_label",
                optional=True), "train_dataset"),
    process_parameter("test_dataset"),
    process_parameter("test_label", optional=True),
    process_parameter("skip_save"),
    process_parameter("clearml_access_key", optional=True),
    process_parameter("clearml_secret_key", optional=True),
    process_parameter("clearml_project", optional=True),
    process_parameter("backtest_threshold"),
    process_parameter("backtest_volume"),
    process_parameter("backtest_tpsl_pct"),
    process_parameter("backtest_commission"),
    process_parameter("backtest_leverage"),
    process_parameter("backtest_cash"),
    process_parameter("skip_backtest"),
    conditional(rename_parameters(
        {"train_dataset": "dataset", "train_label": "label"}, keep_old=True), "train_dataset"),
    conditional(initialize_clearml, "clearml_access_key"),
    get_model_module,
    conditional(get_dataset, "train_dataset"),
    conditional(run_training, "train_dataset"),
    conditional(conditional(save_model, "skip_save",
                negation=True), "train_dataset"),
    conditional(download_model, "train_dataset", negation=True),
    rename_parameters({"test_dataset": "dataset",
                      "test_label": "label"}, keep_old=True),
    get_dataset,
    generate_predictions,
    evaluate_predictions,
    conditional(backtest_predictions, "skip_backtest", negation=True),
    submit_to_drive
])
def evaluate(*args, **kwargs):
    pass
