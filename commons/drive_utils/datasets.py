import logging
import os

from commons.drive import get_drive_module
from commons.env import getenv
import pandas as pd

__all__ = ["download_dataset", "upload_dataset"]

from commons.exceptions import CloudFileNotFoundError

LOGGER = logging.getLogger(__name__)

def download_dataset(name: str):
    LOGGER.debug(f"Download dataset '{name}'")
    drive = get_drive_module()
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, name)
    if not os.path.exists(local_path):
        LOGGER.debug(f"Dataset '{name}' is not cached, downloading using drive '{drive.__name__}'")
        drive.download(os.path.join('datasets', name), local_path)
    LOGGER.debug(f"Reading CSV from '{local_path}'")
    return pd.read_csv(local_path, parse_dates=True, index_col='Date')

def upload_dataset(name: str, df: pd.DataFrame, append: bool=False):
    LOGGER.debug(f'Upload dataset "{name}", append={append}')
    drive = get_drive_module()
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, name)
    if append:
        try:
            drive.download(os.path.join('datasets', name), local_path)
            dataset = pd.concat([pd.read_csv(local_path, parse_dates=True), df])
            drive.delete(os.path.join('datasets', name))
        except CloudFileNotFoundError:
            LOGGER.debug(f"Dataset not found on the drive, creating (append=True)")
            dataset = df
    else:
        dataset = df
    LOGGER.debug(f"Saving dataset '{name}' to local file '{local_path}'")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    dataset.to_csv(local_path)
    drive.upload(local_path, os.path.join('datasets', name))