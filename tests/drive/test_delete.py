import os

from commons.configparams import Config
from commons.testing import mocks
from drive.steps.delete import delete
from drive.steps.upload import upload
import commons.drive.git as git


def test_delete():
    try:
        os.makedirs(".tmp/tests/")
    except Exception:
        pass
    dataset = mocks.dataset(1010)
    df = dataset.df
    Config.set_param("DRIVE", "git")
    Config.set_param("GIT_DRIVE_REPO_URL", "https://github.com/S-P-2137/Data_test")
    start_path = os.path.abspath(".tmp/tests/test_delete")
    end_path = "dataset/test_delete"
    df.to_csv(start_path)
    delete(f"git:{end_path}")

    upload(start_path, end_path)
    assert git.is_branch_exist(end_path)

    delete(f"git:{end_path}")
    assert not git.is_branch_exist(end_path)
