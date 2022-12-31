import logging
from multiprocessing import Process
from commons.env import Env
from commons.tempdir import TempDir
from commons.timing import step
import pytest
import os

LOGGER = logging.getLogger(__name__)


@step
def unit_tests(*args, **kwargs):
    with TempDir() as td:
        with Env(UNIT_TESTING="True", drive='test', test_workspace=os.path.abspath(os.path.normpath(td))):
            exit_code = pytest.main(["--cov-report=term-missing", "--cov=.", "tests/"])
    if exit_code != 0:
        raise AssertionError("Unit test failure")
