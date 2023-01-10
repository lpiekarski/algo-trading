from core.env import TempEnv
from core.subcommand_execution.execution_flow import execute_subcommand
import os


def test_download_git(tmpdir):
    with TempEnv(drive="git",
                 GIT_DRIVE_REPO_URL="./integration_tests/resources/test_drive"):
        remote_path = "test.txt"
        local_path = os.path.join(tmpdir, "test.txt")

        execute_subcommand("download", remote_path, local_path)

        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "Test file content\n"


def test_download_local(tmpdir):
    with TempEnv(drive="local"):
        remote_path = "./integration_tests/resources/test_local.txt"
        local_path = os.path.join(tmpdir, "test.txt")

        execute_subcommand("download", remote_path, local_path)

        assert os.path.exists(local_path)
        assert open(local_path, "r").read() == "Local file content"
