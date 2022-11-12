import logging
import os
from typing import Union

from commons.drivepath import Drivepath, cache, clear_cache, copy
import pandas as pd

__all__ = ["download_prediction", "upload_prediction"]

from commons.string import formpath
from commons.tempdir import TempDir

LOGGER = logging.getLogger(__name__)


def download_prediction(drivepath: Union[Drivepath, str]):
    local_path, _ = cache(drivepath)
    return pd.read_csv(local_path)


def upload_prediction(drivepath: Union[Drivepath, str], df: pd.DataFrame):
    with TempDir() as tempdir:
        tempfile = os.path.join(tempdir, 'prediction')
        LOGGER.debug(
            f"Saving prediction '{drivepath}' to local file '{formpath(tempfile)}'")
        df.to_csv(tempfile)
        copy(tempfile, drivepath)
        clear_cache(tempfile)
