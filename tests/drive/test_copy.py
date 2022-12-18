import filecmp

from commons.configparams import Config
from commons.testing import mocks
from drive.steps.copy import copy
from drive.steps.upload import upload


def test_copy_local():
    dataset = mocks.dataset(1010)
    df = dataset.df
    start_path = ".tmp/tests/test_copy_local"
    end_path = ".tmp/tests/test_copy_local_END"
    df.to_csv(start_path)
    copy(f"local:{start_path}", f"local:{end_path}")
    assert filecmp.cmp(start_path, end_path)


def test_copy_git():
    dataset = mocks.dataset(1010)
    df = dataset.df
    Config.set_param("DRIVER", "git")
    Config.set_param("GIT_DRIVE_REPO_URL", "https://github.com/S-P-2137/Data_test")

    start_path = ".tmp/tests/test_copy"
    git_path = "dataset/test_copy"
    end_path = ".tmp/tests/test_copy_git"

    df.to_csv(start_path)
    copy(f"local:{start_path}", f"git:{git_path}")
    copy(f"git:{git_path}", f"local:{end_path}")
    assert filecmp.cmp(start_path, end_path)
