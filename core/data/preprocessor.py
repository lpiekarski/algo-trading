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
            rolling_window: int = None):
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
        self.std = None
        self.mean = None
        self.range_min = None
        self.range_max = None
        self.standardized_columns = None
        self.normalized_columns = None
        self.log_change_columns = None
        self.num_features = num_features
        self.standardization_regexes = init_list(standardization_regexes, [".*"])
        self.normalization_regexes = init_list(normalization_regexes, [])
        self.log_change_regexes = init_list(log_change_regexes, [])
        self.rolling_window = rolling_window

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
        for col in x:
            if col_matches_any(col, self.log_change_regexes):
                self.log_change_columns.append(col)
            elif col_matches_any(col, self.normalization_regexes):
                self.normalized_columns.append(col)
            elif col_matches_any(col, self.standardization_regexes):
                self.standardized_columns.append(col)
        x_std = x[self.standardized_columns]
        self.mean = x_std.mean(axis=0)
        self.std = x_std.std(axis=0)
        x_norm = x[self.normalized_columns]
        self.range_min = x_norm.min(axis=0)
        self.range_max = x_norm.max(axis=0)

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
        x_std = x[self.standardized_columns]
        x_norm = x[self.normalized_columns]
        x_log_change = x[self.log_change_columns]
        x.update((x_std - self.mean) / self.std)
        x.update((x_norm - self.range_min) / (self.range_max - self.range_min + 1e-8))
        x.update(log_change(x_log_change))
        x = x.fillna(0)
        if y is None:
            if self.rolling_window is not None and apply_rolling_window:
                x = rolling_window(self.rolling_window, x)
                return x
            return x.to_numpy()
        if self.rolling_window is not None and apply_rolling_window:
            x, y = rolling_window(self.rolling_window, x, y)
            return x, y
        return x.to_numpy(), y.to_numpy()

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
