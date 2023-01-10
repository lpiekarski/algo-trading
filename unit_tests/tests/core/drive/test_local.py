from core.env import TempEnv
import core.drive.local as drive
import os
from core.testing.files import create_file


def test_download(tmpdir):
    with TempEnv(drive="local"):
        remote_path = "./unit_tests/resources/test_local.txt"
        local_path = os.path.join(tmpdir, "test.txt")
        drive.download(remote_path, local_path)
        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "Local file content"


def test_upload_local(tmpdir):
    with TempEnv(drive="local"):
        remote_path = os.path.join(tmpdir, "test_upload_local_uploaded.txt")
        local_path = os.path.join(tmpdir, "test_upload_local.txt")
        create_file(local_path, "This is a local upload test!")

        drive.upload(local_path, remote_path)

        assert os.path.exists(remote_path)
        assert open(remote_path, "r").read() == "This is a local upload test!"

        # assert os.path.exists(remote_path + ".md5")
