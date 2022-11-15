from commons.data.dataset import Dataset
import numpy as np
import pandas as pd


def dataset(size=1500):
    return Dataset(ohlc_dataframe(size))


def ohlc_dataframe(size=1500):
    sequence = np.random.randint(100, 201, size)
    return pd.DataFrame({
        'Open': sequence + 0.25 + 0.1 * np.random.randn(sequence.shape[0]),
        'High': sequence + 0.5 + 0.1 * np.random.randn(sequence.shape[0]),
        "Low": sequence + 0.1 + 0.1 * np.random.randn(sequence.shape[0]),
        'Close': sequence + 0.25 + 0.1 * np.random.randn(sequence.shape[0]),
        'Volume': ([200.] * len(sequence)) + 10. * np.random.randn(sequence.shape[0])
    }, index=pd.DatetimeIndex(
        [pd.Timestamp('2010-01-01 00:00') + pd.Timedelta(minutes=i) for i in range(len(sequence))], name="Date"))
