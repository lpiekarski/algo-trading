#!/usr/bin/env python

import click
import os
import sys
import logging

from collector.collect import collect_group
from collector.csv2dataset import csv2dataset_group
from collector.dataset2csv import dataset2csv_group
from collector.extract import extract_group
from core.env import set_env_from_file
from core.logging import init_logging
from core.exceptions import ArgumentError, AtfError
from core.string import TAB
from drive.copy import copy_group
from drive.delete import delete_group
from drive.download import download_group
from drive.upload import upload_group
from model.backtest import backtest_group
from model.evaluate import evaluate_group
from model.predict import predict_group
from model.train import train_group
from testing.test import test_group
from trader.trade import trade_group

LOGGER = logging.getLogger(__name__)


@click.command(
    cls=click.CommandCollection,
    sources=[
        evaluate_group,
        collect_group,
        extract_group,
        predict_group,
        train_group,
        test_group,
        trade_group,
        download_group,
        upload_group,
        delete_group,
        copy_group,
        csv2dataset_group,
        dataset2csv_group,
        backtest_group
    ]
)
@click.option("-D", "env", multiple=True,
              help="Set environment variable e.g. -Dvar=value")
@click.option("-E", "--envfile", help="Path to the file with environmental variables' definition", default=None)
def atf(env, envfile):
    collected_env = {}
    if envfile is not None:
        collected_env |= set_env_from_file(envfile)
    collected_env |= set_env_from_options(env)
    init_logging()
    LOGGER.debug(f"env:\n\t{TAB.join([f'{k}={v}' for k, v in collected_env.items()])}")


def set_env_from_options(env):
    result = {}
    for entry in env:
        entry_split = entry.split("=", 1)
        if len(entry_split) != 2:
            raise ArgumentError(f"Invalid argument '{entry}'")
        var, value = entry_split
        os.environ[var] = value
        result[var] = value
    return result


if __name__ == '__main__':
    try:
        atf()
    except AtfError as e:
        sys.exit(1)
    except RuntimeError as e:
        sys.exit(-1)
