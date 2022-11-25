import shutil
import os

from commons.configparams import Config
from commons.exceptions import NotFoundError

__all__ = ["upload", "download"]


def upload(local_path: str, cloud_path: str) -> None:
    test_workspace = Config.require_param('test_workspace')
    cloud_path = os.path.join(test_workspace, cloud_path)
    if os.path.normpath(local_path) != os.path.normpath(cloud_path):
        if os.path.dirname(cloud_path) != '':
            os.makedirs(os.path.dirname(cloud_path), exist_ok=True)
        shutil.copy(local_path, cloud_path)


def download(cloud_path: str, local_path: str) -> None:
    test_workspace = Config.require_param('test_workspace')
    cloud_path = os.path.join(test_workspace, cloud_path)
    if not os.path.exists(cloud_path):
        raise NotFoundError(
            f"Cannot find file in location: '{cloud_path}'")
    if os.path.normpath(local_path) != os.path.normpath(cloud_path):
        if os.path.dirname(local_path) != '':
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
        shutil.copy(cloud_path, local_path)


def delete(cloud_path: str) -> None:
    test_workspace = Config.require_param('test_workspace')
    cloud_path = os.path.join(test_workspace, cloud_path)
    if not os.path.exists(cloud_path):
        raise NotFoundError(
            f"Cannot find file in location: '{cloud_path}'")
    os.remove(cloud_path)
