import logging
import os

from commons.drive import get_drive_module
from commons.drive_utils import split_pathname
from commons.env import getenv
import pandas as pd

__all__ = ["download_prediction", "upload_prediction"]

from commons.string import formpath

LOGGER = logging.getLogger(__name__)

def download_prediction(name: str):
    drive_type, name = split_pathname(name)
    drive = get_drive_module(drive_type)
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, 'predictions', name)
    if not os.path.exists(local_path):
        LOGGER.debug(f"Prediction '{name}' is not cached, downloading using drive '{drive.__name__}'")
        drive.download(os.path.join('predictions', name), local_path)
    return pd.read_csv(local_path)

def upload_prediction(name: str, df: pd.DataFrame):
    drive_type, name = split_pathname(name)
    drive = get_drive_module(drive_type)
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, 'predictions', name)
    LOGGER.debug(f"Saving prediction '{name}' to local file '{formpath(local_path)}'")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    df.to_csv(local_path)
    drive.upload(local_path, os.path.join('predictions', name))