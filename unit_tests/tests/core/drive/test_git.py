from core.env import TempEnv
import core.drive.git as drive
import os


def test_download(tmpdir):
    with TempEnv(GIT_DRIVE_REPO_URL="./unit_tests/resources/test_drive"):
        remote_path = "test.txt"
        local_path = os.path.join(tmpdir, "test.txt")
        drive.download(remote_path, local_path)
        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "Test file content\n"
