import importlib
import logging
import os

from commons.drive import get_drive_module
from commons.env import getenv, require_env
import pandas as pd

__all__ = ["get_dataset"]

LOGGER = logging.getLogger(__name__)

def get_dataset(name: str):
    LOGGER.debug(f"Getting dataset {name}")
    drive = get_drive_module()
    DATA_STORAGE_DIR = getenv("DATA_STORAGE_DIR", './data')
    local_path = os.path.join(DATA_STORAGE_DIR, name)
    if not os.path.exists(local_path):
        drive.download(name, local_path)
    return pd.read_csv(local_path)

def put_dataset(name: str, df: pd.DataFrame):
    drive = get_drive_module()
    DATA_STORAGE_DIR = getenv("DATA_STORAGE_DIR", './data')
    local_path = os.path.join(DATA_STORAGE_DIR, name)
    df.to_csv(local_path)
    drive.upload(local_path, name)