import importlib

import commons.drive as drive
import neptune.new as neptune
import os
import click

from commons.dataset import get_dataset
from commons.env import getenv
from commons.exceptions import ArgumentError
import logging

__all__ = ["evaluate", "evaluate_group"]

from commons.string import BREAK, break_padded
from commons.timing import command_success
from model.predictors import get_model_module

LOGGER = logging.getLogger(__name__)

@click.group()
def evaluate_group():
    pass

@evaluate_group.command()
@click.option("--model", "-m", help="Name of the model to evaluate")
@click.option("--dataset", "-d", help="Labelled dataset to use for evaluation")
def evaluate(model: str, dataset: str):
    LOGGER.info(break_padded(f"evaluator:evaluate"))
    LOGGER.info("")
    if model is None:
        model = getenv("model")
        if model is None:
            raise ArgumentError("Provide model using '-m', '--model' or through environment variable 'model'")

    if dataset is None:
        dataset = getenv("dataset")
        if dataset is None:
            raise ArgumentError("Provide dataset using '-d', '--dataset' or through environment variable 'dataset'")

    NEPTUNE_API_TOKEN = getenv("NEPTUNE_API_TOKEN")
    if NEPTUNE_API_TOKEN is None:
        LOGGER.warning(f"'NEPTUNE_API_TOKEN' is not set, evaluation results will not be stored.")
    # Download test dataset
    LOGGER.info("Getting test dataset")
    X = get_dataset(dataset)
    # Generate predictions
    LOGGER.info("Generating predictions from model")
    model_module = get_model_module(model)
    y_pred = model_module.predict(X)
    # Compare predictions to labels
    LOGGER.info("Comparing predictions to labels")

    LOGGER.info("Storing results in Neptune")
    command_success(LOGGER)
    #run = neptune.init(
    #    name=model_name,
    #    project="lpiekarski/S-P-2137",
    #    api_token
    #
    #    ="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzMTQ4NTdmMy00OWRkLTQ2MmUtYWIwNC03MWVhZmM2MDQxNDMifQ==", #os.getenv("NEPTUNE_API_TOKEN")
    #)

    #params = {"learning_rate": 0.001, "optimizer": "Adam"}
    #run["parameters"] = params

    #for epoch in range(10):
    #    run["train/loss"].log(0.9 ** epoch)

    #run["eval/f1_score"] = 0.66

    #run.stop()



if __name__ == '__main__':
    evaluate()