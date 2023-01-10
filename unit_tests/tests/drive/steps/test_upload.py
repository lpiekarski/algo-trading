import subprocess

from core.env import TempEnv
from core.testing.files import create_file
from drive.steps.download import download
from drive.steps.upload import upload
import os


def test_upload_git(tmpdir):
    git_drive_dir = "./unit_tests/resources/test_drive"
    with TempEnv(drive="git",
                 GIT_DRIVE_REPO_URL=git_drive_dir):
        remote_path = "unit_test_upload_git.txt"
        local_path = os.path.join(tmpdir, "test_upload_git.txt")
        create_file(local_path, "This is a git upload test!")

        upload(local_path, remote_path)

        # assert subprocess.run("git show-branch remotes/origin/test_upload_git.txt",
        #                      encoding='utf-8', cwd=git_drive_dir).returncode == 0
        # assert subprocess.run("git show-branch remotes/origin/test_upload_git.txt.md5",
        #                      encoding='utf-8', cwd=git_drive_dir).returncode == 0
        os.remove(local_path)
        assert not os.path.exists(local_path)
        download(remote_path, local_path)
        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "This is a git upload test!"


def test_upload_local(tmpdir):
    with TempEnv(drive="local"):
        remote_path = os.path.join(tmpdir, "test_upload_local_uploaded.txt")
        local_path = os.path.join(tmpdir, "test_upload_local.txt")
        create_file(local_path, "This is a local upload test!")

        upload(local_path, remote_path)

        assert os.path.exists(remote_path)
        assert open(remote_path, "r").read() == "This is a local upload test!"

        # assert os.path.exists(remote_path + ".md5")
