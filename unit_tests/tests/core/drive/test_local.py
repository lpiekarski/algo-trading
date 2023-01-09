from core.env import TempEnv
from drive.steps.download import download
import core.drive.local as drive
import os


def test_download(tmpdir):
    with TempEnv(drive="local"):
        remote_path = "./unit_tests/resources/test_local.txt"
        local_path = os.path.join(tmpdir, "test.txt")
        drive.download(remote_path, local_path)
        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "Local file content"
