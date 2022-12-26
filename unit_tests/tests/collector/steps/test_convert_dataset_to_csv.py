import os

import pandas as pd

from collector.steps.convert_dataset_to_csv import convert_dataset_to_csv
from commons.tempdir import TempDir
from commons.testing import mocks


def test_convert_dataset_to_csv():
    with TempDir() as workspace:
        dataset = mocks.dataset()
        dataset.save(os.path.join(workspace, 'source'))
        convert_dataset_to_csv("source", "target")
        df = pd.read_csv(os.path.join(workspace, 'target'), index_col="Date", parse_dates=True)
        assert df.to_string() == dataset.df.to_string()
