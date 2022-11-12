import logging

from commons.exceptions import NotInterruptingError
from commons.timing import step
import subprocess

LOGGER = logging.getLogger(__name__)


@step
def format_tests(*args, **kwargs):
    sp = subprocess.run(['autopep8',
                         '--ignore-local-config',
                         '--aggressive',
                         '--aggressive',
                         '--aggressive',
                         '--diff',
                         '--exit-code',
                         '--recursive',
                         '--exclude',
                         'venv',
                         '.'],
                        capture_output=True,
                        encoding='utf-8')
    if sp.stdout != "":
        LOGGER.info('autopep8 stdout output:\n' + sp.stdout)
    if sp.stderr != "":
        LOGGER.warning('autopep8 stderr output:\n' + sp.stderr)
    if sp.returncode == 2:
        raise NotInterruptingError(
            "Code is not formatted properly, run 'autopep8 .' to fix")
    elif sp.returncode != 0:
        raise NotInterruptingError(
            f"autopep8 finished with code: {sp.returncode}")
