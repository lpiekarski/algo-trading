import pickle
import re
import pandas as pd
import numpy as np

from core.data.series import rolling_window
from core.data.utils import log_change


class Preprocessor:
    def __init__(
            self,
            num_features=None,
            standardization_regexes=None,
            normalization_regexes=None,
            log_change_regexes=None,
            rolling_window=None):
        self.std = None
        self.mean = None
        self.range_min = None
        self.range_max = None
        self.standardized_columns = None
        self.normalized_columns = None
        self.log_change_columns = None
        self.num_features = num_features
        self.standardization_regexes = init_list(standardization_regexes, [".*"])
        self.normalization_regexes = init_list(normalization_regexes, [".*"])
        self.log_change_regexes = init_list(log_change_regexes, [".*"])
        self.rolling_window = rolling_window

    def fit(self, x):
        x_ = x.copy()
        clamp(x_)
        self.num_features = x_.shape[1]
        self.normalized_columns = []
        self.standardized_columns = []
        self.log_change_columns = []
        for col in x_:
            if col_matches_any(col, self.standardization_regexes):
                self.standardized_columns.append(col)
            elif col_matches_any(col, self.normalization_regexes):
                self.normalized_columns.append(col)
            elif col_matches_any(col, self.log_change_regexes):
                self.log_change_columns.append(col)
        xstd = x_[self.standardized_columns]
        self.mean = xstd.mean()
        self.std = xstd.std()
        xnorm = x_[self.normalized_columns]
        self.range_min = xnorm.min()
        self.range_max = xnorm.max()

    def apply(self, x, y=None):
        x_ = x.copy()
        clamp(x_)
        xstd = x_[self.standardized_columns]
        xnorm = x_[self.normalized_columns]
        xlog_change = x_[self.log_change_columns]
        x_.update((xstd - self.mean) / self.std)
        x_.update((xnorm - self.range_min) /
                  (self.range_max - self.range_min + 1e-8))
        x_.update(log_change(xlog_change))
        x_ = x_.fillna(0)
        if y is None:
            if self.rolling_window is not None:
                x_ = rolling_window(self.rolling_window, x_)
            return x_
        if self.rolling_window is not None:
            x_, y = rolling_window(self.rolling_window, x_, y)
        return x_, y

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'rb') as file:
            return pickle.load(file)


def init_list(lst, default):
    if lst is not None:
        return lst
    return default


def col_matches_any(col, regexes):
    return any([bool(re.match(r, col)) for r in regexes])


def clamp(x: pd.DataFrame):
    x.replace(np.inf, 1e12, inplace=True)
    x.replace(-np.inf, -1e12, inplace=True)
