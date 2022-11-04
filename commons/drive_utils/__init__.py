import logging
import os

from commons.drive import get_drive_module
from commons.env import getenv, require_env
from commons.tempdir import TempDir

LOGGER = logging.getLogger(__name__)

def split_pathname(pathname):
    if ':' in pathname:
        drive, name = pathname.split(':', maxsplit=2)
        if name.startswith('/'):
            name = name[1:]
        return drive, name
    else:
        return require_env('drive'), pathname

def join_pathname(path, pathname):
    drive, name = split_pathname(pathname)
    return f"{drive}:{os.path.join(path, name)}"

def download_file_to_cache(path):
    drive_type, path = split_pathname(path)
    drive = get_drive_module(drive_type)
    cache_dir = getenv("CACHE_DIR")
    local_path = os.path.join(cache_dir, path)
    if not os.path.exists(local_path):
        LOGGER.debug(f"File '{path}' is not cached, downloading using drive '{drive.__name__}'")
        drive.download(path, local_path)
    return local_path

def copy_file(source_path, target_path):
    LOGGER.debug(f'Upload file "{source_path}" to "{target_path}"')
    source_drive, source_path = split_pathname(source_path)
    target_drive, target_path = split_pathname(target_path)
    with TempDir() as tempdir:
        local_path = os.path.join(tempdir, os.path.basename(source_path))
        source_drive = get_drive_module(source_drive)
        source_drive.download(source_path, local_path)
        target_drive = get_drive_module(target_drive)
        target_drive.upload(local_path, target_path)