import os

from collector.steps.convert_csv_to_dataset import convert_csv_to_dataset
from commons.data.dataset import Dataset
from commons.tempdir import TempDir
import commons.testing.mocks as mocks


def test_convert_csv_to_dataset():
    with TempDir() as tempdir:
        source = os.path.join(tempdir, 'source')
        target = os.path.join(tempdir, 'target')
        df = mocks.ohlc_dataframe()
        df.to_csv(source, index_label="Date")
        convert_csv_to_dataset(source, target)
        dataset = Dataset.load(target)
        assert df.to_string() == dataset.df.to_string()
