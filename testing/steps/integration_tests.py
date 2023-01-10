import logging
import zipfile
from core.logging import TempFileLogger
from core.tempdir import TempDir
import pytest
import os

LOGGER = logging.getLogger(__name__)


def integration_tests(*args, **kwargs):
    log_dir = os.path.dirname(os.path.abspath(os.getenv("LOG_FILE", "./logs/atf.log")))
    with zipfile.ZipFile(file="integration_tests/resources.zip", mode='r') as zf:
        zf.extractall("integration_tests/resources/")
    with TempDir("integration_tests/resources"), TempFileLogger(os.path.join(log_dir, "integration_tests.log"), "DEBUG"):
        exit_code = pytest.main([
            "integration_tests/tests/",
            "--basetemp",
            os.getenv("TEMP_DIR")
        ])
    if exit_code != 0:
        raise AssertionError("Integration test failure")
