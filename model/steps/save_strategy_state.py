import logging
import os
import zipfile

from core.drive_utils.strategies import upload_strategy_state
from core.drivepath import clear_cache, from_string
from core.string import formpath
from core.tempdir import TempDir

LOGGER = logging.getLogger(__name__)


def save_strategy_state(strategy, strategy_module, **kwargs):
    strategy = from_string(strategy)
    with TempDir() as td1:
        with TempDir() as td2:
            data_path = os.path.join(td2, 'strategy')
            LOGGER.info(
                f"Saving state of '{strategy}' in location: '{formpath(data_path)}'")
            strategy_module.save_state(td1)
            os.makedirs(os.path.dirname(data_path), exist_ok=True)
            with zipfile.ZipFile(file=data_path, mode='w') as zf:
                for root, _, files in os.walk(td1):
                    for file in files:
                        path = os.path.join(root, file)
                        zf.write(path, os.path.relpath(path, td1))
            upload_strategy_state(data_path, strategy)
            clear_cache(data_path)
