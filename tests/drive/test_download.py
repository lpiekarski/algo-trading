from commons.configparams import Config
from drive.steps.download import download
import commons.testing.mocks as mocks
import os


def test_download_git():
    Config.set_param("DRIVER", "git")
    Config.set_param("GIT_DRIVE_REPO_URL", "https://github.com/S-P-2137/Data")
    remote_path = "datasets/train/M30_H1"
    local_path = ".tmp/tests/test_download_git"
    download(remote_path, local_path, drive_name="git")
    assert os.path.exists(".tmp/tests/test_download_git")
    os.remove(local_path)


def test_download_local():
    Config.set_param("DRIVER", "local")

    remote_path = ".tmp/tests/test.csv"
    local_path = ".tmp/tests/test_download_git"
    dataset = mocks.dataset(1010)
    df = dataset.df
    with open(remote_path, 'w') as f:
        df.to_csv(f)
    download(remote_path, local_path, drive_name="local")
    assert os.path.exists(".tmp/tests/test_download_git")
    os.remove(local_path)
    os.remove(remote_path)
