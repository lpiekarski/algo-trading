import click
import os
import sys
import logging

from collector.collect import collect_group
from commons.logging import init_logging
from commons.exceptions import ArgumentError, BotErrorWithStacktrace, BotErrorWithoutStacktrace
from commons.string import ENDLINE, TAB
from commons.timing import command_failure
from evaluator.evaluate import evaluate_group
from model.predict import predict_group
from model.train import train_group
from testing.test import test_group

LOGGER = logging.getLogger(__name__)

@click.command(cls=click.CommandCollection, sources=[evaluate_group, collect_group, predict_group, train_group,
                                                     test_group])
@click.option("-D", "env", multiple=True, help="Set environment variable e.g. -Dvar=value")
def bot(env):
    for entry in env:
        entry_split = entry.split("=")
        if len(entry_split) != 2:
            raise ArgumentError(f"Invalid argument '{entry}'")
        var, value = entry_split
        os.environ[var] = value
    init_logging()
    LOGGER.debug(f"env:\n\t{(ENDLINE + TAB).join(env)}")

if __name__ == '__main__':
    try:
        bot()
    except BotErrorWithStacktrace as e:
        LOGGER.error(f"Error during command execution: {e}", exc_info=e)
        command_failure(LOGGER)
        sys.exit(-1)
    except BotErrorWithoutStacktrace as e:
        LOGGER.error(f"Error during command execution: {e}")
        command_failure(LOGGER)
        sys.exit(-1)