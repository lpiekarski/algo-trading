import logging
import os

from commons.drive import get_drive_module
from commons.env import getenv
import pandas as pd

__all__ = ["download_prediction", "upload_prediction"]

LOGGER = logging.getLogger(__name__)

def download_prediction(name: str):
    if ':' in name:
        drive_type, name = name.split(':', maxsplit=2)
        drive = get_drive_module(drive_type)
    else:
        drive = get_drive_module()
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, 'predictions', name)
    if not os.path.exists(local_path):
        LOGGER.debug(f"Prediction '{name}' is not cached, downloading using drive '{drive.__name__}'")
        drive.download(os.path.join('predictions', name), local_path)
    return pd.read_csv(local_path)

def upload_prediction(name: str, df: pd.DataFrame):
    if ':' in name:
        drive_type, name = name.split(':', maxsplit=2)
        drive = get_drive_module(drive_type)
    else:
        drive = get_drive_module()
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, 'predictions', name)
    LOGGER.debug(f"Saving prediction '{name}' to local file '{local_path}'")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    df.to_csv(local_path)
    drive.upload(local_path, os.path.join('predictions', name))