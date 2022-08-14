import os

import click
import logging

from commons.dataset import get_dataset, put_dataset
from commons.exceptions import ArgumentError, CloudFileNotFoundError
from commons.timing import command_success

__all__ = ["predict", "predict_group"]

from model.predictors import get_model_module

LOGGER = logging.getLogger(__name__)

@click.group()
def predict_group():
    pass

@predict_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--dataset", "-d", help="Dataset to generate a prediction for")
@click.option("--output", "-o", help="Name of the results file")
def predict(model: str, dataset: str, output: str):
    if model is None:
        model = os.getenv("model")
        if model is None:
            raise ArgumentError("Provide model using '-m', '--model' or through environment variable 'model'")

    if dataset is None:
        dataset = os.getenv("dataset")
        if dataset is None:
            raise ArgumentError("Provide dataset using '-d', '--dataset' or through environment variable 'dataset'")

    LOGGER.info(f"Getting dataset '{dataset}'")
    try:
        X = get_dataset(dataset)
    except CloudFileNotFoundError as e:
        LOGGER.error(f"Cannot find dataset '{dataset}'")
        raise e
    # Generate predictions
    LOGGER.info(f"Generating predictions from model '{model}'")
    model_module = get_model_module(model)
    y_pred = model_module.predict(X)
    if output is None:
        output = f"{dataset}_results_{model}"
    LOGGER.info(f"Saving results as {output}")
    put_dataset(output, y_pred)
    command_success(LOGGER)

if __name__ == '__main__':
    predict()