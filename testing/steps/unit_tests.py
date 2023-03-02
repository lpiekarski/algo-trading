import logging
import zipfile
from core.logging import TempFileLogger
from core.tempdir import TempDir
import pytest
import os

LOGGER = logging.getLogger(__name__)


def unit_tests(*args, **kwargs):
    log_dir = os.path.dirname(os.path.abspath(os.getenv("LOG_FILE", "./logs/atf.log")))
    with zipfile.ZipFile(file="unit_tests/resources.zip", mode='r') as zf:
        zf.extractall("unit_tests/resources/")
    with TempDir("unit_tests/resources"), TempFileLogger(os.path.join(log_dir, "unit_tests.log"), "DEBUG"):
        exit_code = pytest.main([
            "--cov-report=term-missing",
            "--cov=.",
            "unit_tests/tests/",
            "--basetemp",
            os.getenv("TEMP_DIR"),
            "-vv"
        ])
    if exit_code != 0:
        raise AssertionError("Unit test failure")
