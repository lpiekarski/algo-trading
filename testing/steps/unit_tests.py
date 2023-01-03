import logging
import zipfile

from commons.env import TempEnv
from commons.tempdir import TempDir
import pytest
import os

LOGGER = logging.getLogger(__name__)


def unit_tests(*args, **kwargs):
    with zipfile.ZipFile(file="unit_tests/resources.zip", mode='r') as zf:
        zf.extractall("unit_tests/resources/")
    with TempDir("unit_tests/resources"), TempEnv(UNIT_TESTING="True"):
        exit_code = pytest.main([
            "--cov-report=term-missing",
            "--cov=.",
            "unit_tests/tests/",
            "--basetemp",
            os.getenv("TEMP_DIR")
        ])

    if exit_code != 0:
        raise AssertionError("Unit test failure")
