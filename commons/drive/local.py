import logging
import shutil
import os

from commons.exceptions import NotFoundError

__all__ = ["upload", "download"]

from commons.string import formpath

LOGGER = logging.getLogger(__name__)


def upload(local_path: str, cloud_path: str) -> None:
    LOGGER.debug(
        f"Local drive uploading file from '{formpath(local_path)}' to '{formpath(cloud_path)}'")
    if os.path.normpath(local_path) != os.path.normpath(cloud_path):
        if os.path.dirname(cloud_path) != '':
            os.makedirs(os.path.dirname(cloud_path), exist_ok=True)
        shutil.copy(local_path, cloud_path)


def download(cloud_path: str, local_path: str) -> None:
    if not os.path.exists(cloud_path):
        raise NotFoundError(
            f"Cannot find file in location: '{cloud_path}'")
    LOGGER.debug(
        f"Local drive copying file from '{formpath(cloud_path)}' to '{formpath(local_path)}'")
    if os.path.normpath(local_path) != os.path.normpath(cloud_path):
        if os.path.dirname(local_path) != '':
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
        shutil.copy(cloud_path, local_path)


def delete(cloud_path: str) -> None:
    if not os.path.exists(cloud_path):
        raise NotFoundError(
            f"Cannot find file in location: '{cloud_path}'")
    LOGGER.debug(
        f"Local drive deleting file from '{os.path.normpath(cloud_path)}'")
    os.remove(cloud_path)
