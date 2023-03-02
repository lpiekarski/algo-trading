import logging
import zipfile

from core.drive_utils.strategies import download_strategy_state
from core.exceptions import NotFoundError
from core.tempdir import TempDir

LOGGER = logging.getLogger(__name__)


def load_strategy_state(strategy, strategy_module, **kwargs):
    LOGGER.info(f"Loading saved state of strategy '{strategy}'")
    try:
        strategy_state_file = download_strategy_state(strategy)
        with TempDir() as td:
            with zipfile.ZipFile(file=strategy_state_file, mode='r') as zf:
                zf.extractall(td)
            strategy_module.load_state(td)
    except NotFoundError:
        LOGGER.info(f"Strategy state file not found")
