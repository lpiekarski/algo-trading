import logging
import os
from typing import Union

from commons.drive_utils import get_cache_dir
from commons.drivepath import Drivepath, cache, copy, from_string

__all__ = ["download_model_data", "upload_model_data"]

LOGGER = logging.getLogger(__name__)


def download_model_data(drivepath: Union[Drivepath, str]):
    file, _ = cache(drivepath)
    return os.path.abspath(os.path.normpath(file))


def upload_model_data(local_path: str, drivepath: Union[Drivepath, str]):
    if os.path.exists(local_path):
        copy(local_path, drivepath)
