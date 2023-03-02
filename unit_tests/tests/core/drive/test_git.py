from core.env import TempEnv
import core.drive.git as drive
import os
from core.testing.files import create_file


def test_download(tmpdir):
    with TempEnv(GIT_DRIVE_REPO_URL="./unit_tests/resources/test_drive"):
        remote_path = "test.txt"
        local_path = os.path.join(tmpdir, "test.txt")
        drive.download(remote_path, local_path)
        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "Test file content\n"


def test_upload_git(tmpdir):
    git_drive_dir = "./unit_tests/resources/test_drive"
    with TempEnv(drive="git",
                 GIT_DRIVE_REPO_URL=git_drive_dir):
        remote_path = "test_upload_git.txt"
        local_path = os.path.join(tmpdir, "test_upload_git.txt")
        create_file(local_path, "This is a git upload test!")

        drive.upload(local_path, remote_path)

        # assert subprocess.run("git show-branch remotes/origin/test_upload_git.txt",
        #                      encoding='utf-8', cwd=git_drive_dir).returncode == 0
        # assert subprocess.run("git show-branch remotes/origin/test_upload_git.txt.md5",
        #                      encoding='utf-8', cwd=git_drive_dir).returncode == 0
        os.remove(local_path)
        assert not os.path.exists(local_path)
        drive.download(remote_path, local_path)
        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "This is a git upload test!"
