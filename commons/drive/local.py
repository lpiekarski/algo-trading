import logging
import shutil
import os

from commons.env import getenv
from commons.exceptions import CloudFileNotFoundError

__all__ = ["upload", "download"]

from commons.string import formpath

LOGGER = logging.getLogger(__name__)

def upload(local_path: str, cloud_path: str) -> None:
	LOCAL_STORE = getenv("LOCAL_DRIVE_STORE")
	target = os.path.join(LOCAL_STORE, cloud_path)
	LOGGER.debug(f"Local drive uploading file from '{formpath(local_path)}' to '{formpath(target)}'")
	if os.path.normpath(local_path) != os.path.normpath(target):
		os.makedirs(os.path.dirname(target), exist_ok=True)
		shutil.copy(local_path, target)

def download(cloud_path: str, local_path: str) -> None:
	LOCAL_STORE = getenv("LOCAL_DRIVE_STORE")
	source = os.path.join(LOCAL_STORE, cloud_path)
	if not os.path.exists(source):
		raise CloudFileNotFoundError(f"Cannot find file in remote location: '{source}'")
	LOGGER.debug(f"Local drive downloading file from '{formpath(source)}' to '{formpath(local_path)}'")
	if os.path.normpath(local_path) != os.path.normpath(source):
		os.makedirs(os.path.dirname(local_path), exist_ok=True)
		shutil.copy(source, local_path)

def delete(cloud_path: str) -> None:
	LOCAL_STORE = getenv("LOCAL_DRIVE_STORE")
	full_path = os.path.join(LOCAL_STORE, cloud_path)
	if not os.path.exists(full_path):
		raise CloudFileNotFoundError(f"Cannot find file in remote location: '{full_path}'")
	LOGGER.debug(f"Local drive deleting file from '{os.path.normpath(full_path)}'")
	os.remove(full_path)
