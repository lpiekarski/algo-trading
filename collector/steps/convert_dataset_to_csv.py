import logging
import os

from commons.data.dataset import Dataset
from commons.drivepath import copy
from commons.tempdir import TempDir

LOGGER = logging.getLogger(__name__)


def convert_dataset_to_csv(source, target, **kwargs):
    with TempDir() as tempdir:
        local_source_path = os.path.join(tempdir, 'source')
        local_target_path = os.path.join(tempdir, 'target')
        copy(source, f"local:{local_source_path}")
        dataset = Dataset.load(local_source_path)
        dataset.df.to_csv(local_target_path, index_label='Date')
        copy(f"local:{local_target_path}", target)
