from commons.configparams import Config
import commons.git as git
from commons.testing import mocks
from drive.steps.delete import delete
from drive.steps.upload import upload


def test_delete():
    dataset = mocks.dataset(1010)
    df = dataset.df
    Config.set_param("DRIVER", "git")
    Config.set_param("GIT_DRIVE_REPO_URL", "https://github.com/S-P-2137/Data_test")
    start_path = ".tmp/tests/test_delete"
    end_path = "dataset/test_delete"
    df.to_csv(start_path)
    upload(start_path, end_path)
    delete(end_path)
    branches = git.remote_branch(end_path)
    assert branches.find(f"origin/{end_path}") == -1

