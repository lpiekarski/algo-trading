import os
import click
import logging

from commons.exceptions import TestsFailedError
from commons.import_utils import module_from_file
from commons.string import BREAK
from commons.timing import command_failure, command_success

__all__ = ["test", "test_group"]

from testing.drive_tests import run_drive_tests
from testing.shape_tests import run_shape_tests

LOGGER = logging.getLogger(__name__)

@click.group()
def test_group():
    pass

@test_group.command()
@click.option("--skip_shapes", "-s", is_flag=True)
@click.option("--skip_drives", "-d", is_flag=True)
def test(skip_shapes: bool, skip_drives: bool):
    results = {
        'shape_tests': 'SUCCESS',
        'drive_tests': 'SUCCESS'
    }
    failed = False
    if not skip_shapes:
        try:
            run_shape_tests()
        except Exception as e:
            results['shape_tests'] = f'FAILURE: {e}'
            failed = True
    if not skip_drives:
        try:
            run_drive_tests()
        except Exception as e:
            results['drive_tests'] = f'FAILURE: {e}'
            failed = True
    LOGGER.info(f"{BREAK}")
    LOGGER.info(f"Test results:")
    LOGGER.info(f"{BREAK}")
    for test_name, status in results.items():
        LOGGER.info(f"{test_name}: {status}")
    if failed:
        raise TestsFailedError(results)
    else:
        command_success(LOGGER)


if __name__ == '__main__':
    test()