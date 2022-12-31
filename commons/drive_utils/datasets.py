import logging
import os
from typing import Union

from commons.data.dataset import Dataset
from commons.drivepath import Drivepath, cache, clear_cache, copy, delete, from_string

__all__ = ["download_dataset", "upload_dataset"]

from commons.exceptions import NotFoundError
from commons.string import formpath
from commons.tempdir import TempDir

LOGGER = logging.getLogger(__name__)


def download_dataset(drivepath: Union[Drivepath, str]):
    LOGGER.debug(f"Download dataset '{drivepath}'")
    file, _ = cache(drivepath)
    return Dataset.load(file)


def upload_dataset(
        drivepath: Union[Drivepath, str], dataset: Dataset, append: bool = False):
    LOGGER.debug(f'Upload dataset "{drivepath}", append={append}')
    drivepath = from_string(drivepath)
    with TempDir() as tempdir:
        tempfile = os.path.join(tempdir, 'dataset')
        if append:
            try:
                file, _ = cache(drivepath)
                result_dataset = Dataset.load(file)
                result_dataset.concat(dataset)
                delete(drivepath)
            except NotFoundError:
                LOGGER.debug(
                    f"Dataset not found on the drive, creating (append=True)")
                result_dataset = dataset
        else:
            result_dataset = dataset
        LOGGER.debug(
            f"Saving dataset '{drivepath}' to local file '{formpath(tempfile)}'")
        result_dataset.save(tempfile)
        copy(tempfile, drivepath)
        clear_cache(tempfile)
