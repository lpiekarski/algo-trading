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
def evaluate_group(): pass

@evaluate_group.command()
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--train-dataset", "-t", help="Dataset to use for training")
@click.option("--train-label", "-k", help="Name of the label column within the train dataset")
@click.option("--test-dataset", "-e", help="Labelled dataset to use for evaluation")
@click.option("--test-label", "-l", help="Name of the label column within the test dataset")
@click.option("--skip-save", "-s", help="Do not save the results of the training", is_flag=True)
@click.option("--clearml-access-key", help="ClearML access key")
@click.option("--clearml-secret-key", help="ClearML secret key")
@click.option("--clearml-project", help="ClearML project name")
@click.option("--backtest-threshold", help="Minimum confidence to make a decision during backtesting", default=0.05)
@click.option("--backtest-volume", help="Backtest trade volume", default=0.01)
@click.option("--backtest-tpsl-pct", help="Backtest take profit/stop loss price change percentage", default=0.01)
@click.option("--backtest-commission", help="Backtest comission fee percentage for each transaction", default=0.0002)
@click.option("--backtest-margin", help="Backtest leverage", default=30)
@click.option("--backtest-cash", help="Backtest starting cash amount", default=10000)
@subcommand([
    process_parameter("model"),
    process_parameter("train_dataset", optional=True),
    conditional(process_parameter("train_label", optional=True), "train_dataset"),
    process_parameter("test_dataset"),
    process_parameter("test_label", optional=True),
    process_parameter("skip_save"),
    process_parameter("clearml_access_key"),
    process_parameter("clearml_secret_key"),
    process_parameter("clearml_project"),
    process_parameter("backtest_threshold"),
    process_parameter("backtest_volume"),
    process_parameter("backtest_tpsl_pct"),
    process_parameter("backtest_commission"),
    process_parameter("backtest_margin"),
    process_parameter("backtest_cash"),
    conditional(rename_parameters({"train_dataset": "dataset", "train_label": "label"}, keep_old=True), "train_dataset"),
    initialize_clearml,
    get_model_module,
    conditional(get_dataset, "train_dataset"),
    conditional(run_training, "train_dataset"),
    conditional(conditional(save_model, "skip_save", negation=True), "train_dataset"),
    conditional(download_model, "train_dataset", negation=True),
    rename_parameters({"test_dataset": "dataset", "test_label": "label"}, keep_old=True),
    get_dataset,
    generate_predictions,
    evaluate_predictions,
    backtest_predictions,
    submit_to_drive
])
def evaluate(*args, **kwargs): pass
