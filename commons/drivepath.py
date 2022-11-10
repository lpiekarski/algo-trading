import hashlib
import logging
import os
from typing import Union

from commons.drive import get_drive_module
from commons.drive_utils import get_cache_dir
from commons.env import require_env
from commons.exceptions import CloudFileNotFoundError
from commons.tempdir import TempDir

LOGGER = logging.getLogger(__name__)

class Drivepath:
    def __init__(self, drivepath: str):
        drive_type, path = split(drivepath)
        self.drive_type = drive_type
        self.path = path

    def __str__(self):
        return f"{self.drive_type}:{self.path}"

def cache(p: Union[Drivepath, str]):
    p = from_string(p)
    LOGGER.debug(f"Caching file '{p}'")
    drive = get_drive_module(p.drive_type)
    cached, local_path, md5_path = is_cached(p)
    if not cached:
        LOGGER.debug(f"File is not previously cached, downloading")
        drive.download(p.path, local_path)
        try:
            drive.download(p.path + '.md5', md5_path)
        except CloudFileNotFoundError:
            LOGGER.warning(f'Cannot download md5 for "{p.path}", generating checksum')
            save_md5(local_path, md5_path)
    return local_path, md5_path

def is_cached(p: Union[Drivepath, str]):
    p = from_string(p)
    LOGGER.debug(f"Checking if '{p}' is cached")
    drive = get_drive_module(p.drive_type)
    cache_dir, md5_dir = get_cache_dir(p.drive_type)
    local_path = os.path.join(cache_dir, p.path)
    md5_path = os.path.join(md5_dir, p.path)
    if not os.path.exists(local_path) or not os.path.exists(md5_path):
        LOGGER.debug(f"File is not cached: file or md5 is not present in cache directory")
        return False, local_path, md5_path
    else:
        with TempDir() as tempdir:
            new_checksum_path = os.path.join(tempdir, 'md5')
            try:
                drive.download(p.path + '.md5', new_checksum_path)
            except CloudFileNotFoundError:
                LOGGER.warning(f'There is no checksum file for "{p}"')
            if not os.path.exists(new_checksum_path):
                LOGGER.debug("File is not cached: cannot download md5 file for source")
                return False, local_path, md5_path
            else:
                old_checksum = read_md5(md5_path)
                new_checksum = read_md5(new_checksum_path)
                if new_checksum != old_checksum:
                    LOGGER.debug(f"File is not cached: checksums differ")
                    return False, local_path, md5_path
    LOGGER.debug("File is cached")
    return True, local_path, md5_path

def copy(p1: Union[Drivepath, str], p2: Union[Drivepath, str]):
    p1 = from_string(p1)
    p2 = from_string(p2)
    p1_file, p1_md5 = cache(p1)
    target_drive = get_drive_module(p2.drive_type)
    target_drive.upload(p1_file, p2.path)
    target_drive.upload(p1_md5, p2.path + '.md5')

def delete(p: Union[Drivepath, str]):
    p = from_string(p)
    drive = get_drive_module(p.drive_type)
    try:
        drive.delete(p.path)
        drive.delete(p.path + '.md5')
    except CloudFileNotFoundError:
        LOGGER.warning(f"Couldn't delete file")
    clear_cache(p)

def clear_cache(p: Union[Drivepath, str]):
    p = from_string(p)
    files_dir, md5_dir = get_cache_dir(p.drive_type)
    file = os.path.join(files_dir, p.path)
    md5 = os.path.join(md5_dir, p.path)
    if os.path.exists(file):
        os.remove(file)
        try:
            os.removedirs(os.path.dirname(file))
        except OSError:
            pass
    if os.path.exists(md5):
        os.remove(md5)
        try:
            os.removedirs(os.path.dirname(md5))
        except OSError:
            pass


def split(p: str):
    if ':' in p:
        drive, name = p.split(':', maxsplit=1)
        if name.startswith('/'):
            name = name[1:]
        return drive, name
    else:
        return require_env('drive'), p

def from_string(drivepath):
    if isinstance(drivepath, str):
        return Drivepath(drivepath)
    else:
        return drivepath

def join(path: Union[os.PathLike, str], drivepath: Union[Drivepath, str]):
    drivepath = from_string(drivepath)
    return f"{drivepath.drive_type}:{os.path.join(path, drivepath.path)}"

def save_md5(path_to_hash, target):
    hash_md5 = hashlib.md5()
    with open(path_to_hash, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'wb') as f:
        f.write(hash_md5.digest())

def read_md5(path):
    with open(path, 'rb') as f:
        return f.read()