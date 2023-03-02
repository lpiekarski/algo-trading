import yaml
import logging
import os
from typing import Union
from core.drivepath import Drivepath, cache, copy

LOGGER = logging.getLogger(__name__)


def download_strategy_state(drivepath: Union[Drivepath, str]):
    file, _ = cache(drivepath)
    return os.path.abspath(os.path.normpath(file))


def upload_strategy_state(local_path: str, drivepath: Union[Drivepath, str]):
    if os.path.exists(local_path):
        copy(local_path, drivepath)


def download_strategy_config(drivepath: Union[Drivepath, str]):
    file, _ = cache(drivepath)
    with open(file, 'r') as f:
        return yaml.load(f, yaml.CLoader)
