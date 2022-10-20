import logging
import os

from commons.drive import get_drive_module
from commons.env import getenv

__all__ = ["download_model_data", "upload_model_data", "get_model_cache_path"]

LOGGER = logging.getLogger(__name__)

def get_model_cache_path(name: str):
    cache_dir = getenv("CACHE_DIR")
    return os.path.join(cache_dir, 'models', name)

def download_model_data(name: str):
    if ':' in name:
        drive_type, name = name.split(':', maxsplit=2)
        drive = get_drive_module(drive_type)
    else:
        drive = get_drive_module()
    local_path = get_model_cache_path(name)
    if not os.path.exists(local_path):
        LOGGER.debug(f"Model data '{name}' is not cached, downloading using drive '{drive.__name__}'")
        drive.download(os.path.join('models', name), local_path)
    return os.path.abspath(os.path.normpath(local_path))

def upload_model_data(name: str):
    if ':' in name:
        drive_type, name = name.split(':', maxsplit=2)
        drive = get_drive_module(drive_type)
    else:
        drive = get_drive_module()
    local_path = get_model_cache_path(name)
    if os.path.exists(local_path):
        drive.upload(local_path, os.path.join('models', name))
