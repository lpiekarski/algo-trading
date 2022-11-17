#!/usr/bin/env python

import click
import os
import sys
import logging

from collector.collect import collect_group
from collector.csv2dataset import csv2dataset_group
from collector.dataset2csv import dataset2csv_group
from collector.extract import extract_group
from commons.logging import init_logging
from commons.exceptions import ArgumentError, BotError
from commons.string import ENDLINE, TAB
from commons.timing import command_failure
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
def atf(env):
    for entry in env:
        entry_split = entry.split("=", 1)
        if len(entry_split) != 2:
            raise ArgumentError(f"Invalid argument '{entry}'")
        var, value = entry_split
        os.environ[var] = value
    init_logging()
    LOGGER.debug(f"env:\n\t{(ENDLINE + TAB).join(env)}")


if __name__ == '__main__':
    try:
        atf()
    except BotError as e:
        sys.exit(1)
    except Exception as e:
        sys.exit(-1)
