import logging
import shutil
import os

from commons.env import getenv
from commons.exceptions import CloudFileNotFoundError

__all__ = ["upload", "download"]

LOGGER = logging.getLogger(__name__)

def upload(local_path: str, cloud_path: str) -> None:
	LOCAL_STORE = getenv("DATA_STORAGE_DIR", './data')
	target = os.path.join(LOCAL_STORE, cloud_path)
	LOGGER.debug(f"Local drive uploading file from '{os.path.normpath(local_path)}' to '{os.path.normpath(target)}'")
	if os.path.normpath(local_path) != os.path.normpath(target):
		shutil.copy(local_path, target)

def download(cloud_path: str, local_path: str) -> None:
	LOCAL_STORE = getenv("DATA_STORAGE_DIR", './data')
	source = os.path.join(LOCAL_STORE, cloud_path)
	if not os.path.exists(source):
		raise CloudFileNotFoundError(f"Cannot find file in remote location: '{source}'")
	LOGGER.debug(f"Local drive downloading file from '{os.path.normpath(source)}' to '{os.path.normpath(local_path)}'")
	if os.path.normpath(local_path) != os.path.normpath(source):
		shutil.copy(source, local_path)