import logging
from types import SimpleNamespace

from commons.exceptions import NonInterruptingError
from commons.timing import step
import os
import autopep8

LOGGER = logging.getLogger(__name__)


@step
def format_tests(*args, **kwargs):
    diffs = autopep8.fix_multiple_files(
        [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))],
        options=SimpleNamespace(
            recursive=True,
            exclude=['**/venv'],
            aggressive=3,
            diff=True,
            ignore_local_config=True,
            jobs=1,
            verbose=0,
            in_place=False,
            max_line_length=120,
            line_range=None,
            ignore=None,
            select=None,
            hang_closing=False,
            indent_size=4,
            pep8_passes=-1,
            experimental=False
        )
    )
    if len(diffs) > 0:
        LOGGER.error(f"Diffs from autopep8:\n{''.join(diffs)}")
        raise AssertionError(
            "Code is not formatted properly, run 'python -m autopep8 .' to fix")
    else:
        LOGGER.info("Code is formatted properly")
