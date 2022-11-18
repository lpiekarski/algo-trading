import os

from collector.steps.convert_csv_to_dataset import convert_csv_to_dataset
from commons.data.dataset import Dataset
import commons.testing.mocks as mocks


def test_convert_csv_to_dataset(workspace):
    df = mocks.ohlc_dataframe()
    df.to_csv(os.path.join(workspace, 'source'), index_label="Date")
    convert_csv_to_dataset("source", "target")
    dataset = Dataset.load(os.path.join(workspace, 'target'))
    assert df.to_string() == dataset.df.to_string()
