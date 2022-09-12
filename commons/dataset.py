import logging
import os

from commons.drive import get_drive_module
from commons.env import getenv
import pandas as pd

__all__ = ["get_dataset", "put_dataset"]

LOGGER = logging.getLogger(__name__)

def get_dataset(name: str):
    drive = get_drive_module()
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, name)
    if not os.path.exists(local_path):
        LOGGER.debug(f"Dataset '{name}' is not cached, downloading using drive '{drive.__name__}'")
        drive.download(os.path.join('datasets', name), local_path)
    return pd.read_csv(local_path)

def put_dataset(name: str, df: pd.DataFrame):
    drive = get_drive_module()
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, name)
    LOGGER.debug(f"Saving dataset '{name}' to local file '{local_path}'")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    df.to_csv(local_path)
    drive.upload(local_path, os.path.join('datasets', name))