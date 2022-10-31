import logging
import os

from commons.data.dataset import Dataset
from commons.drive import get_drive_module
from commons.drive_utils import split_pathname
from commons.env import getenv

__all__ = ["download_dataset", "upload_dataset"]

from commons.exceptions import CloudFileNotFoundError
from commons.string import formpath

LOGGER = logging.getLogger(__name__)

def download_dataset(name: str):
    LOGGER.debug(f"Download dataset '{name}'")
    drive_type, name = split_pathname(name)
    drive = get_drive_module(drive_type)
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, 'datasets', name)
    if not os.path.exists(local_path):
        LOGGER.debug(f"Dataset '{name}' is not cached, downloading using drive '{drive.__name__}'")
        drive.download(os.path.join('datasets', name), local_path)
    LOGGER.debug(f"Loading dataset from '{formpath(local_path)}'")
    return Dataset.load(local_path)

def upload_dataset(name: str, dataset: Dataset, append: bool=False):
    LOGGER.debug(f'Upload dataset "{name}", append={append}')
    drive_type, name = split_pathname(name)
    drive = get_drive_module(drive_type)
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, 'datasets', name)
    if append:
        try:
            drive.download(os.path.join('datasets', name), local_path)
            result_dataset = Dataset.load(local_path)
            result_dataset.concat(dataset)
            drive.delete(os.path.join('datasets', name))
        except CloudFileNotFoundError:
            LOGGER.debug(f"Dataset not found on the drive, creating (append=True)")
            result_dataset = dataset
    else:
        result_dataset = dataset
    LOGGER.debug(f"Saving dataset '{name}' to local file '{formpath(local_path)}'")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    result_dataset.save(local_path)
    drive.upload(local_path, os.path.join('datasets', name))