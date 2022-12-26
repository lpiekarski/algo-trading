import os

import pandas as pd

from collector.steps.convert_dataset_to_csv import convert_dataset_to_csv
from commons.testing import mocks


def test_convert_dataset_to_csv(tmpdir):
    dataset = mocks.dataset()
    source = os.path.relpath(os.path.join(tmpdir, 'source'), ".")
    target = os.path.relpath(os.path.join(tmpdir, 'target'), ".")
    dataset.save(source)
    convert_dataset_to_csv(f"local:{source}", f"local:{target}")
    df = pd.read_csv(target, index_col="Date", parse_dates=True)
    assert df.to_string() == dataset.df.to_string()
