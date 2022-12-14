import os

from collector.steps.convert_csv_to_dataset import convert_csv_to_dataset
from core.data.dataset import Dataset
import core.testing.mocks as mocks


def test_convert_csv_to_dataset(tmpdir):
    df = mocks.ohlc_dataframe()
    source = os.path.relpath(os.path.join(tmpdir, 'source'), ".")
    target = os.path.relpath(os.path.join(tmpdir, 'target'), ".")
    df.to_csv(source, index_label="Date")
    convert_csv_to_dataset(f"local:{source}", f"local:{target}")
    dataset = Dataset.load(target)
    assert df.to_string() == dataset.df.to_string()
