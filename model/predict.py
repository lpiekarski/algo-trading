import importlib
import os

import click
import logging

from commons.dataset import get_dataset
from commons.exceptions import ArgumentError
from commons.timing import command_success

__all__ = ["predict", "predict_group"]


LOGGER = logging.getLogger(__name__)

@click.group()
def predict_group():
    pass

@predict_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--dataset", "-d", help="Dataset to generate a prediction for")
def predict(model: str, dataset: str):
    if model is None:
        model = os.getenv("model")
        if model is None:
            raise ArgumentError("Provide model using '-m', '--model' or through environment variable 'model'")

    if dataset is None:
        dataset = os.getenv("dataset")
        if dataset is None:
            raise ArgumentError("Provide dataset using '-d', '--dataset' or through environment variable 'dataset'")

    LOGGER.info("Getting test dataset")
    X = get_dataset(dataset)
    # Generate predictions
    LOGGER.info("Generating predictions from model")
    model_module = importlib.import_module(f"model.predictors.{model}")
    y_pred = model_module.predict(X)

    command_success(LOGGER)

if __name__ == '__main__':
    predict()