import collector.technical_indicators.technical_indicators as ti
import pandas as pd
import logging

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
            LOGGER.debug(f"Processing datetime '{current_time}'")
            self.bucket_time = current_time
            past_supp_df = df.loc[df.index <= self.bucket_time]
            self.past_resampled_df = past_supp_df.resample(time_tag).apply(OHLC_RESAMPLE_MAP)
        current_bucket_df = df.loc[(df.index > self.bucket_time) & (df.index <= index)]
        if current_bucket_df.empty:
            return self.past_resampled_df
        return pd.concat([self.past_resampled_df, current_bucket_df.tail(1)])

class ProgressBar:
    def __init__(self, num_updates):
        self.count = 0
        self.length = num_updates

    def update(self, count=1):
        self.count += count
        completed_percent = 100 * self.count / self.length
        if self.count % 500 == 0 or self.count == self.length:
            LOGGER.info(f"{self.count}/{self.length} = {completed_percent:.2f}%")
            LOGGER.info("----")

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