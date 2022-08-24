import os
import click
import logging

from commons.exceptions import TestsFailedError
from commons.import_utils import module_from_file
from commons.string import BREAK, break_padded
from commons.timing import command_failure, command_success, subcommand

__all__ = ["test", "test_group"]

from testing.drive_tests import drive_tests
from testing.shape_tests import shape_tests

LOGGER = logging.getLogger(__name__)

@click.group()
def test_group():
    pass

@test_group.command()
@click.option("--skip_shapes", "-s", is_flag=True)
@click.option("--skip_drives", "-d", is_flag=True)
def test(*args, **kwargs):
    test_subcommand(*args, **kwargs)

@subcommand("testing:test", [shape_tests, drive_tests])
def test_subcommand(*args, **kwargs):
    pass

if __name__ == '__main__':
    test()