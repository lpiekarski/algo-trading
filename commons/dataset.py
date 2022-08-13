import importlib
import os
from commons.env import getenv, require_env
import pandas as pd

__all__ = ["get_dataset"]


def get_dataset(name: str):
    drive = importlib.import_module(f"commons.drive.{require_env('drive')}")
    DATA_STORAGE_DIR = getenv("DATA_STORAGE_DIR", './data')
    local_path = os.path.join(DATA_STORAGE_DIR, name)
    if not os.path.exists(local_path):
        drive.download(name, local_path)
    return pd.read_csv(local_path)

