import logging

from commons.exceptions import NonInterruptingError
from commons.timing import step
import pytest
import os

LOGGER = logging.getLogger(__name__)


@step
def unit_tests(*args, **kwargs):
    os.environ["UNIT_TESTING"] = "True"
    exit_code = pytest.main(["--pyargs", "tests"])
    os.environ["UNIT_TESTING"] = "False"
    if exit_code != 0:
        raise AssertionError("Unit test failure")
