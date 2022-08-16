import os

import click
import logging

__all__ = ["train", "train_group"]

from commons.dataset import get_dataset
from commons.exceptions import ArgumentError, CloudFileNotFoundError
from commons.timing import command_success
from model.predictors import get_model_module

LOGGER = logging.getLogger(__name__)

@click.group()
def train_group():
    pass

@train_group.command()
@click.option("--model", "-m", help="Name of the model")
@click.option("--dataset", "-d", help="Train dataset")
def train(model: str, dataset: str):
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
        y = X["y"].copy()
        X.drop('y', axis=1, inplace=True)
    except CloudFileNotFoundError as e:
        LOGGER.error(f"Cannot find dataset '{dataset}'")
        raise e

    # Train
    LOGGER.info(f"Train model '{model}'")
    model_module = get_model_module(model)
    model_module.train(X, y)
    command_success(LOGGER)

if __name__ == '__main__':
    train()