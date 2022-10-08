import logging
import shutil
import os
import zipfile
from subprocess import CalledProcessError
from split_file_reader import SplitFileReader
from split_file_reader.split_file_writer.split_file_writer import SplitFileWriter
import commons.git as git
from commons.env import getenv

__all__ = ["upload", "download"]

from commons.exceptions import CloudFileNotFoundError

LOGGER = logging.getLogger(__name__)
REPO_PATH = "./.git-drive"

def initialize():
    if not os.path.exists(REPO_PATH):
        git_password = getenv('GIT_PASSWORD')
        if git_password is not None:
            REPO_URL = f"https://{getenv('GIT_PASSWORD')}@github.com/S-P-2137/Data"
        else:
            REPO_URL = f"https://github.com/S-P-2137/Data"
        git.clone_no_checkout(REPO_URL, REPO_PATH)

def upload(local_path: str, cloud_path: str) -> None:
    initialize()
    cloud_path = os.path.normpath(cloud_path).replace('\\', '/')
    max_file_size = int(getenv('GIT_DRIVE_MAX_FILE_SIZE'))
    add_path = os.path.join(REPO_PATH, os.path.basename(cloud_path))
    git.reset_hard("main", cwd=REPO_PATH)
    git.checkout("main", cwd=REPO_PATH)
    git.checkout_create(cloud_path, cwd=REPO_PATH)
    try:
        git.fetch(cloud_path, cwd=REPO_PATH)
        git.reset_soft(cloud_path, cwd=REPO_PATH)
        git.restore_staged('.', cwd=REPO_PATH)
    except CalledProcessError as e:
        LOGGER.debug(f"Error on fetch: {e}")
    os.makedirs(os.path.dirname(add_path), exist_ok=True)
    with SplitFileWriter(f"{add_path}.zip.", max_file_size) as sfw:
        with zipfile.ZipFile(file=sfw, mode='w') as zf:
            zf.write(local_path, os.path.basename(cloud_path))
    for file in split_filenames(f"{add_path}.zip."):
        git.add(os.path.abspath(file), cwd=REPO_PATH)
        git.commit(f"Automated: add '{file}' to the storage", cwd=REPO_PATH)
        git.push(cloud_path, cwd=REPO_PATH)

def download(cloud_path: str, local_path: str) -> None:
    initialize()
    cloud_path = os.path.normpath(cloud_path).replace('\\', '/')
    checked_out_path = os.path.join(REPO_PATH, f"{os.path.basename(cloud_path)}.zip.")
    git.reset_hard("main", cwd=REPO_PATH)
    git.checkout(cloud_path, cwd=REPO_PATH)
    try:
        git.fetch(cloud_path, cwd=REPO_PATH)
    except CalledProcessError as e:
        raise CloudFileNotFoundError(f"File not found in the repository. {e}")
    git.reset_soft(cloud_path, cwd=REPO_PATH)
    try:
        git.restore_staged('.', cwd=REPO_PATH)
    except CalledProcessError:
        pass
    i = 0
    while True:
        try:
            git.checkout_file(f"{os.path.basename(cloud_path)}.zip.{i:03}", branch=cloud_path, cwd=REPO_PATH)
            i += 1
        except CalledProcessError as e:
            if i == 0:
                raise CloudFileNotFoundError(f"File not found in the repository. {e}")
            else:
                break
    local_dirname = os.path.dirname(os.path.abspath(local_path))
    os.makedirs(local_dirname, exist_ok=True)
    with SplitFileReader(list(split_filenames(checked_out_path))) as sfr:
        with zipfile.ZipFile(file=sfr, mode='r') as zf:
            LOGGER.debug(f"Extracting to {local_dirname}")
            zf.extractall(local_dirname)
    LOGGER.debug(f"Directory after extraction: {os.listdir(local_dirname)}")
    shutil.move(os.path.join(local_dirname, os.path.basename(cloud_path)), local_path)

def delete(cloud_path: str) -> None:
    initialize()
    cloud_path = os.path.normpath(cloud_path).replace('\\', '/')
    git.delete_branch(cloud_path, cwd=REPO_PATH)

def split_filenames(path: str):
    i = 0
    while os.path.exists(f"{path}{i:03}"):
        yield f"{path}{i:03}"
        i += 1
