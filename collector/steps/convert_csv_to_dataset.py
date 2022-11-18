import logging
import os

from commons.data.dataset import Dataset
from commons.drivepath import copy
from commons.tempdir import TempDir
from commons.timing import step
import pandas as pd

LOGGER = logging.getLogger(__name__)


@step
def convert_csv_to_dataset(source, target, **kwargs):
    with TempDir() as tempdir:
        local_source_path = os.path.join(tempdir, 'source')
        local_target_path = os.path.join(tempdir, 'target')
        copy(source, f"local:{local_source_path}")
        df = pd.read_csv(local_source_path, parse_dates=True, index_col='Date')
        dataset = Dataset(df)
        dataset.save(local_target_path)
        copy(f"local:{local_target_path}", target)
