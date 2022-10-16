import time

import collector.technical_indicators.technical_indicators as ti
import pandas as pd
import logging
import numpy as np

LOGGER = logging.getLogger(__name__)

OHLC_RESAMPLE_MAP = {
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last'
}

def resample_technical_indicators(dataset, time_tag="1h"):
    result_rows = []
    max_lookback = get_max_lookback()
    resampler = Resampler()
    progress_bar = ProgressBar(dataset.df.shape[0])

    for index, row in dataset.df.iterrows():
        resampled_df = resampler.get_resampled_df(dataset.df, index, time_tag)
        if resampled_df.shape[0] < max_lookback:
            progress_bar.update()
            continue
        resampled_df = resampled_df.tail(max_lookback).copy()

        ti.add_technical_indicators(resampled_df, time_tag)

        last_record = resampled_df.iloc[-1]
        last_record.name = index
        result_rows.append(last_record)

        progress_bar.update()

    return pd.DataFrame(result_rows)

class Resampler:
    def __init__(self):
        self.bucket_time = None
        self.past_resampled_df = None

    def get_resampled_df(self, df, index, time_tag):
        current_time = index.floor(time_tag)
        if self.bucket_time != current_time:
            self.bucket_time = current_time
            past_supp_df = df.loc[df.index <= self.bucket_time]
            self.past_resampled_df = past_supp_df.resample(time_tag).apply(OHLC_RESAMPLE_MAP)
        current_bucket_df = df.loc[(df.index > self.bucket_time) & (df.index <= index)]
        if current_bucket_df.empty:
            return self.past_resampled_df
        return pd.concat([self.past_resampled_df, current_bucket_df.tail(1)])

class ProgressBar:
    def __init__(self, num_updates, bar_length=50, update_frequency=500):
        self.count = 0
        self.length = num_updates
        self.bar_length = bar_length
        self.update_frequency = update_frequency
        self.last_completed_num = None
        self.first_update_time = None

    def update(self, count=1):
        if self.first_update_time is None:
            self.first_update_time = time.time()
        self.count += count
        completed_percent = self.count / self.length
        completed_num = int(np.ceil(self.bar_length * completed_percent))
        remaining_num = int(np.floor(self.bar_length * (1 - completed_percent)))
        if self.last_completed_num != completed_num or self.count == self.length:
            self.last_completed_num = completed_num
            elapsed = time.time() - self.first_update_time
            estimated = elapsed / completed_percent * (1 - completed_percent)
            LOGGER.info(f"|{completed_num * '='}{remaining_num * '-'}| {100 * completed_percent:.2f}%, Estimated: {estimated:.2f} seconds left")

def get_max_lookback():
    result = 0
    for indicator, params in ti.INDICATORS.items():
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
    LOGGER.info(f"Max lookback for indicators is {result}")
    return result