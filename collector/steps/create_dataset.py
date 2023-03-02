import importlib
import logging
import pandas as pd

from core.data.dataset import Dataset

LOGGER = logging.getLogger(__name__)


def create_dataset(amount, interval, source, start_date, **kwargs):
    dfs = []
    for module in source:
        LOGGER.info(f"Collecting data from source '{module}'")
        data_source = importlib.import_module(f"collector.data_sources.{module}")
        df = data_source.get_data(amount, interval, start_date)
        dfs.append(df)
    df = pd.concat(dfs, axis=1)
    df = df.asfreq(interval)
    return dict(dataset=Dataset(df))
