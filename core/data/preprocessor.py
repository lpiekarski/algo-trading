import pickle
import re
from typing import List, Any, Tuple, Union

import pandas as pd
import numpy as np

from core.data.series import rolling_window
from core.data.utils import log_change


class Preprocessor:
    """
    This class is responsible for transforming input and targets to the format that is desired by the model.
    """

    def __init__(
            self,
            num_features: int = None,
            standardization_regexes: List[str] = None,
            normalization_regexes: List[str] = None,
            log_change_regexes: List[str] = None,
            text_regexes: List[str] = None,
            rolling_window: int = None,
            rolling_window_interval: int = None,
            drop_nans: bool = False,
            include_timestamp: bool = False):
        """
        Instance initializer.
        :param num_features: Number of input features.
        :param standardization_regexes: List of regex strings describing which columns to standardize.
            If not specified, defaults to [".*"] which matches all columns.
        :param normalization_regexes: List of regex strings describing which columns to normalize.
            If the value is not specified it defaults to an empty list.
        :param log_change_regexes: List of regex string describing for which
            columns should log_change transform be applied to.
            If the value is not specified it defaults to an empty list.
        :param rolling_window: Size of the rolling window or None if rolling_window transformation shouldn't be applied.
        """
        self.include_timestamp = include_timestamp
        self.drop_nans = drop_nans
        self.std = None
        self.mean = None
        self.range_min = None
        self.range_max = None
        self.standardized_columns = None
        self.normalized_columns = None
        self.log_change_columns = None
        self.text_columns = None
        self.num_features = num_features
        self.standardization_regexes = init_list(standardization_regexes, [".*"])
        self.normalization_regexes = init_list(normalization_regexes, [])
        self.log_change_regexes = init_list(log_change_regexes, [])
        self.text_regexes = init_list(text_regexes, [])
        self.rolling_window = rolling_window
        self.rolling_window_interval = rolling_window_interval

    def fit(self, x: pd.DataFrame) -> None:
        """
        Fit the parameters to match means, stds, etc. from the DataFrame.
        :param x: The dataframe from which statistics are extracted.
        """
        x = clamp(x)
        self.num_features = x.shape[1]
        self.normalized_columns = []
        self.standardized_columns = []
        self.log_change_columns = []
        self.text_columns = []
        for col in x:
            if col_matches_any(col, self.log_change_regexes):
                self.log_change_columns.append(col)
            elif col_matches_any(col, self.normalization_regexes):
                self.normalized_columns.append(col)
            elif col_matches_any(col, self.text_regexes):
                self.text_columns.append(col)
            elif col_matches_any(col, self.standardization_regexes):
                self.standardized_columns.append(col)
        x_std = x[self.standardized_columns]
        self.mean = x_std.mean(axis=0, skipna=True)
        self.std = x_std.std(axis=0, skipna=True)
        x_norm = x[self.normalized_columns]
        self.range_min = x_norm.min(axis=0, skipna=True)
        self.range_max = x_norm.max(axis=0, skipna=True)

    def apply(self, x: pd.DataFrame, y: pd.DataFrame = None,
              apply_rolling_window: bool = True) -> Union[Tuple[np.ndarray, np.ndarray], np.ndarray]:
        """
        Apply fitted transformations to the DataFrame "x",
        apply rolling window (if any was specified) for both "x" and "y".
        :param x: Inputs DataFrame.
        :param y: Targets DataFrame.
        :param apply_rolling_window: Whether to apply the rolling window transformation.
            The transformation still won't be applied if self.rolling_window is None.
        :return: Tuple of transformed "x", "y" if "y" was not None, only "x" otherwise.
        """
        x = clamp(x)
        if self.drop_nans:
            np.isnan(x)
        x_std = x[self.standardized_columns]
        x_norm = x[self.normalized_columns]
        x_log_change = x[self.log_change_columns]
        x_std = (x_std - self.mean) / self.std
        x[x_std.columns] = x_std
        x_norm = (x_norm - self.range_min) / (self.range_max - self.range_min + 1e-8)
        x[x_norm.columns] = x_norm
        after_log_change = pd.DataFrame(
            data=log_change(x_log_change),
            columns=x_log_change.columns,
            index=x_log_change.index)
        x[after_log_change.columns] = (after_log_change - after_log_change.mean()) / after_log_change.std()
        if self.include_timestamp:
            x = to_numpy_with_time(x)
        else:
            x = x.to_numpy()
        if y is None:
            if self.rolling_window is not None and apply_rolling_window:
                x = rolling_window(self.rolling_window, x, inter=self.rolling_window_interval)
            return x
        y = y.to_numpy()
        if self.rolling_window is not None and apply_rolling_window:
            x, y = rolling_window(self.rolling_window, x, y, inter=self.rolling_window_interval)
        return x, y

    def save(self, filepath: str) -> None:
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath: str) -> "Preprocessor":
        with open(filepath, 'rb') as file:
            return pickle.load(file)


def init_list(lst: List[Any], default: List[Any]) -> List[Any]:
    if lst is not None:
        return lst
    return default


def col_matches_any(col: str, regexes: List[str]) -> bool:
    return any([bool(re.match(r, col)) for r in regexes])


def clamp(x: pd.DataFrame) -> pd.DataFrame:
    x = x.replace(np.inf, 1e12)
    x = x.replace(-np.inf, -1e12)
    return x


def to_numpy_with_time(x: pd.DataFrame):
    """
    Converts dataframe to numpy array with time index as the first column
    :param x:
    :return:
    """
    time_since = pd.to_datetime("2010-01-01 00:00")
    time = ((x.index - time_since).total_seconds() // 60).values.astype(np.float32)
    return np.concatenate([time[:, np.newaxis], x.to_numpy()], axis=1)
