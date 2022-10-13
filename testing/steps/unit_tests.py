import logging
from commons.timing import step
import pytest

LOGGER = logging.getLogger(__name__)

@step
def unit_tests(*args, **kwargs):
    exit_code = pytest.main(["--pyargs", "tests"])
    if exit_code != 0:
        raise AssertionError("Unit test failure")
