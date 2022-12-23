import os

from commons.configparams import Config
import commons.drive.git as git
from commons.testing import mocks
from drive.steps.upload import upload
from drive.steps.delete import delete


def test_upload():
    try:
        os.makedirs(".tmp/tests/")
    except Exception:
        pass
    dataset = mocks.dataset(1010)
    df = dataset.df
    Config.set_param("DRIVE", "git")
    Config.set_param("GIT_DRIVE_REPO_URL", "https://github.com/S-P-2137/Data_test")
    start_path = os.path.abspath(".tmp/tests/test_upload")
    end_path = "dataset/test_upload"
    df.to_csv(start_path)
    delete(f"git:{end_path}")

    upload(start_path, end_path)
    assert git.is_branch_exist(end_path)

    delete(f"git:{end_path}")

