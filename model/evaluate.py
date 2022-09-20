import click

from commons.steps.get_labeled_dataset import get_labeled_dataset
from commons.steps.conditional import conditional
from commons.steps.process_parameter import process_parameter
from commons.steps.rename_parameters import rename_parameters
from commons.timing import subcommand
from model.steps.download_model import download_model
from model.steps.evaluate_predictions import evaluate_predictions
from commons.steps.generate_predictions import generate_predictions
from model.steps.get_model_module import get_model_module
from model.steps.run_training import run_training
from model.steps.save_model import save_model
from model.steps.submit_to_drive import submit_to_drive

__all__ = ["evaluate_group"]

@click.group()
def evaluate_group(): pass

@evaluate_group.command()
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--train", "-r", help="Run training?", is_flag=True)
@click.option("--train_dataset", "-t", help="Dataset to use for training")
@click.option("--train_label", "-k", help="Name of the label column within the train dataset", default="y")
@click.option("--test_dataset", "-e", help="Labelled dataset to use for evaluation")
@click.option("--test_label", "-l", help="Name of the label column within the test dataset", default="y")
@subcommand([
    process_parameter("model"),
    conditional(process_parameter("train_dataset"), "train"),
    process_parameter("test_dataset"),
    conditional(process_parameter("train_label"), "train"),
    process_parameter("test_label"),
    conditional(rename_parameters({"train_dataset": "dataset", "train_label": "label"}, keep_old=True), "train"),
    get_model_module,
    conditional(get_labeled_dataset, "train"),
    conditional(run_training, "train"),
    conditional(save_model, "train"),
    conditional(download_model, "train", negation=True),
    rename_parameters({"test_dataset": "dataset", "test_label": "label"}, keep_old=True),
    get_labeled_dataset,
    generate_predictions,
    evaluate_predictions,
    submit_to_drive
])
def evaluate(*args, **kwargs): pass
