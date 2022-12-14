import yaml

from collector.steps.add_indicators import add_indicators, DEFAULT_INDICATOR_CONFIG
import pandas as pd
import logging
from tqdm import tqdm

from core.data.dataset import Dataset

LOGGER = logging.getLogger(__name__)
OHLC_RESAMPLE_MAP = {
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum'
}


def add_resample_indicators(dataset, time_tag, indicators=None, *args, **kwargs):
    indicator_config = None
    if indicators is not None:
        with open(indicators, 'r') as f:
            indicator_config = yaml.load(f, yaml.CLoader)
    if indicator_config is None:
        indicator_config = DEFAULT_INDICATOR_CONFIG
    LOGGER.info(f"reshape to time unit '{time_tag}'")
    dataset.concat(resample_technical_indicators(
        dataset, indicator_config, time_tag=time_tag), axis=1, join='inner')


def resample_technical_indicators(dataset, indicator_config, time_tag="1h"):
    result_rows = []
    max_lookback = get_max_lookback(indicator_config)
    resampler = Resampler()

    for index, row in tqdm(dataset.df.iterrows(), total=dataset.df.shape[0]):
        resampled_df = resampler.get_resampled_df(dataset.df, index, time_tag)
        if resampled_df.shape[0] < max_lookback:
            continue
        resampled_df = resampled_df.tail(max_lookback).copy()
        resampled_dataset = Dataset(resampled_df)
        add_indicators(resampled_dataset, indicator_config=indicator_config, show_progress=False)

        last_record = resampled_dataset.df.iloc[-1].copy()
        last_record.name = index
        last_record.drop(
            ['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
        result_rows.append(last_record)

    return pd.concat(result_rows, axis=1).transpose()


class Resampler:
    def __init__(self):
        self.bucket_time = None
        self.past_resampled_df = None

    def get_resampled_df(self, df, index, time_tag):
        current_time = index.floor(time_tag)
        if self.bucket_time != current_time:
            self.bucket_time = current_time
            past_supp_df = df.loc[df.index <= self.bucket_time]
            self.past_resampled_df = past_supp_df.resample(
                time_tag).apply(OHLC_RESAMPLE_MAP).dropna(axis=0)
        current_bucket_df = df.loc[(
            df.index > self.bucket_time) & (df.index <= index)]
        current_bucket_df = current_bucket_df.resample(
            time_tag, label='right').apply(OHLC_RESAMPLE_MAP)
        if current_bucket_df.empty:
            return self.past_resampled_df
        return pd.concat([self.past_resampled_df, current_bucket_df.tail(1)])


def get_max_lookback(indicator_config):
    result = 0
    for indicator, params in indicator_config.items():
        if params is None:
            pass
        else:
            for param in params:
                if isinstance(param, list):
                    result = max(result, param[0])
                elif isinstance(param, dict):
                    result = max(result, param['length'])
                else:
                    result = max(result, param)
    # Account for log_change resulting in 1 extra nan
    result += 1
    LOGGER.info(f"Max lookback for indicators is {result}")
    return result
