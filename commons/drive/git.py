import logging
import shutil
import os
import commons.git as git
from commons.env import getenv

__all__ = ["upload", "download"]


LOGGER = logging.getLogger(__name__)
REPO_PATH = "./.git-drive"

def initialize():
    if not os.path.exists(REPO_PATH):
        REPO_URL = f"https://{getenv('GIT_PASSWORD')}@github.com/S-P-2137/Data"
        git.clone(REPO_URL, REPO_PATH)

def upload(local_path: str, cloud_path: str) -> None:
    initialize()
    add_path = os.path.join(REPO_PATH, cloud_path)
    if os.path.normpath(local_path) != os.path.normpath(add_path):
        os.makedirs(os.path.dirname(add_path), exist_ok=True)
        shutil.copy(local_path, add_path)
    git.add(os.path.abspath(add_path), cwd=REPO_PATH)
    git.commit(f"Automated: add '{cloud_path}' to the storage", cwd=REPO_PATH)
    git.push(cwd=REPO_PATH)

def download(cloud_path: str, local_path: str) -> None:
    initialize()
    checked_out_path = os.path.join(REPO_PATH, cloud_path)
    if not os.path.exists(checked_out_path):
        git.fetch(cwd=REPO_PATH)
        git.checkout(cloud_path, cwd=REPO_PATH)
    if os.path.normpath(local_path) != os.path.normpath(checked_out_path):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        shutil.copy(checked_out_path, local_path)