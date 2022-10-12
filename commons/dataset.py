import zipfile

import pandas as pd
import os
import json
from commons.env import getenv
from commons.exceptions import BotError
from commons.tempdir import TempDir

class Dataset:
    def __init__(self, df: pd.DataFrame, labels=None, interval=None):
        if not isinstance(df.index, pd.DatetimeIndex):
            raise BotError("Dataframe is required to have DatetimeIndex")
        self.df = df
        if labels is not None:
            self.labels = labels
        else:
            self.labels = []
        if interval is not None:
            self.interval = interval
        else:
            self.interval = infer_interval(df)

    def is_labeled(self):
        return len(self.labels) > 0

    def save(self, path):
        with TempDir() as td:
            df_file = os.path.join(td, os.path.basename(path) + '.tmp')
            config_file = os.path.join(td, os.path.basename(path) + '.config.tmp')
            self.df.to_csv(df_file, index_label='Date')
            with open(config_file, "w") as fp:
                json.dump(dict(
                    labels=self.labels,
                    interval=self.interval
                ), fp)
            with zipfile.ZipFile(file=path, mode='w') as zf:
                zf.write(df_file, 'dataframe.csv')
                zf.write(config_file, "config.json")

    @staticmethod
    def load(path):
        with TempDir() as td:
            cache_dir = os.path.join(td, os.path.basename(path) + '.unzip')
            os.makedirs(cache_dir, exist_ok=True)
            with zipfile.ZipFile(file=path, mode='r') as zf:
                zf.extractall(cache_dir)
            df = pd.read_csv(os.path.join(cache_dir, 'dataframe.csv'), parse_dates=True, index_col='Date')
            result = None
            with open(os.path.join(cache_dir, 'config.json'), 'r') as fp:
                config = json.load(fp)
                labels = config['labels']
                result = Dataset(df, labels)
            return result

    def concat(self, other, **kwargs):
        if self.interval != other.interval:
            raise BotError("Cannot concatenate datasets with different intervals")
        self.df = pd.concat([self.df, other.df], **kwargs)
        self.labels = list(dict.fromkeys(self.labels + other.labels))
        self.interval = infer_interval(self.df)

    def copy(self):
        return Dataset(self.df.copy(), self.labels.copy(), self.interval.copy())

    def get_X(self):
        return self.df.drop(self.labels, axis=1)

    def get_y(self):
        return self.df[self.labels]

    def add_label(self, name, series):
        self.labels.append(name)
        self.df[name] = series

def infer_interval(df: pd.DataFrame):
    return pd.Series(df.index[1:] - df.index[:-1]).mode()