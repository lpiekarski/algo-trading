import yaml
import logging
import os
from typing import Union

from commons.drivepath import Drivepath, cache, copy

__all__ = ["download_model_weights", "upload_model_weights", "download_model_config"]

LOGGER = logging.getLogger(__name__)


def download_model_weights(drivepath: Union[Drivepath, str]):
    file, _ = cache(drivepath)
    return os.path.abspath(os.path.normpath(file))


def upload_model_weights(local_path: str, drivepath: Union[Drivepath, str]):
    if os.path.exists(local_path):
        copy(local_path, drivepath)


def download_model_config(drivepath: Union[Drivepath, str]):
    file, _ = cache(drivepath)
    with open(file, 'r') as f:
        return yaml.load(f, yaml.CLoader)
