import shutil
import os

from commons.env import getenv
from commons.exceptions import CloudFileNotFoundError

__all__ = ["upload", "download"]


def upload(local_path: str, cloud_path: str):
	LOCAL_STORE = getenv("DATA_STORAGE_DIR", './data')
	target = os.path.join(LOCAL_STORE, cloud_path)
	if os.path.normpath(local_path) != os.path.normpath(target):
		shutil.copy(local_path, target)

def download(cloud_path: str, local_path: str):
	LOCAL_STORE = getenv("DATA_STORAGE_DIR", './data')
	source = os.path.join(LOCAL_STORE, cloud_path)
	if not os.path.exists(source):
		raise CloudFileNotFoundError(f"Cannot find file in remote location: '{source}'")
	if os.path.normpath(local_path) != os.path.normpath(source):
		shutil.copy(source, local_path)