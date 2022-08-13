import shutil
import os
from commons.exceptions import CloudFileNotFoundError

__all__ = ["upload", "download"]

LOCAL_STORE = './data'

def upload(local_path: str, cloud_path: str):
	shutil.copy(local_path, cloud_path)

def download(cloud_path: str, local_path: str):
	source = os.path.join(LOCAL_STORE, cloud_path)
	if not os.path.exists(source):
		raise CloudFileNotFoundError(f"Cannot find file in remote location: '{source}'")
	shutil.copy(local_path, source)