import pytest

import collector.technical_indicators.labels as labels
from commons.dataset import Dataset
import pandas as pd

def test_add_best_decision():
    dataset = Dataset(pd.DataFrame({
        'Open': [1, 2, 3, 4, 5, 6, 7],
        'High': [1, 2, 3, 4, 5, 6, 7],
        'Low': [1, 2, 3, 4, 5, 6, 7],
        'Close': [1, 2, 3, 4, 5, 6, 7]
    }, index=pd.DatetimeIndex([
        pd.Timestamp('2010-01-01 00:00'),
        pd.Timestamp('2010-01-01 00:01'),
        pd.Timestamp('2010-01-01 00:02'),
        pd.Timestamp('2010-01-01 00:03'),
        pd.Timestamp('2010-01-01 00:04'),
        pd.Timestamp('2010-01-01 00:05'),
        pd.Timestamp('2010-01-01 00:06'),
    ], name='Date')))

    labels.add_best_decision(dataset, 1)
    print(dataset.df['Best_decision_1'])
    assert dataset.df['Best_decision_1'].equals([1, 1, 1, 1, 1, 1, 0])